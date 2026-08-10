const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const script = fs.readFileSync(path.join(__dirname, "..", "script.js"), "utf8");
const styles = fs.readFileSync(path.join(__dirname, "..", "styles.css"), "utf8");

function blockAfter(source, marker) {
  const markerIndex = source.indexOf(marker);
  assert.notEqual(markerIndex, -1, `Missing ${marker}`);
  const openingBrace = source.indexOf("{", markerIndex + marker.length);
  assert.notEqual(openingBrace, -1, `Missing block for ${marker}`);
  let depth = 0;
  for (let index = openingBrace; index < source.length; index += 1) {
    if (source[index] === "{") depth += 1;
    if (source[index] === "}") depth -= 1;
    if (depth === 0) return source.slice(openingBrace + 1, index);
  }
  assert.fail(`Unclosed block for ${marker}`);
}

function cssRule(source, selector) {
  const escaped = selector.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const match = source.match(new RegExp(`(?:^|\\n)\\s*${escaped}\\s*\\{([^}]*)\\}`, "m"));
  assert.ok(match, `Missing CSS rule for ${selector}`);
  return match[1];
}

function classList() {
  const values = new Set();
  return {
    add: (...names) => names.forEach((name) => values.add(name)),
    remove: (...names) => names.forEach((name) => values.delete(name)),
    toggle: (name) => (values.has(name) ? values.delete(name) : values.add(name)),
    contains: (name) => values.has(name),
  };
}

function node() {
  const listeners = new Map();
  return {
    classList: classList(),
    listeners,
    style: {},
    addEventListener: (type, listener) => listeners.set(type, listener),
  };
}

function runSiteScript({ cursorDotPresent = false, cursorRingPresent = false, width = 900 }) {
  const documentListeners = new Map();
  const body = node();
  const nav = node();
  const navToggle = node();
  const navLinks = node();
  const cursorDot = cursorDotPresent ? node() : null;
  const cursorRing = cursorRingPresent ? node() : null;
  const elements = { mainNav: nav, navToggle, navLinks, cursorDot, cursorRing };

  const document = {
    body,
    addEventListener: (type, listener) => documentListeners.set(type, listener),
    getElementById: (id) => elements[id] || null,
    querySelector: () => null,
    querySelectorAll: () => [],
  };

  const window = {
    innerWidth: width,
    scrollY: 0,
    addEventListener: () => {},
    scrollTo: () => {},
  };

  class IntersectionObserver {
    observe() {}
    unobserve() {}
  }

  vm.runInNewContext(script, {
    console,
    document,
    window,
    IntersectionObserver,
    performance: { now: () => 0 },
    requestAnimationFrame: () => {},
    setTimeout: () => {},
  });

  return { body, cursorDot, documentListeners, navToggle };
}

test("native cursors remain the default until desktop custom-cursor mode is active", () => {
  assert.match(cssRule(styles, "body"), /cursor:\s*auto/);
  assert.doesNotMatch(cssRule(styles, "body"), /cursor:\s*none/);
  assert.match(cssRule(styles, "a"), /cursor:\s*pointer/);
  assert.match(cssRule(styles, "button"), /cursor:\s*pointer/);
  assert.match(cssRule(styles, ".cursor-dot"), /display:\s*none/);
  assert.match(cssRule(styles, ".cursor-ring"), /display:\s*none/);

  const desktopRules = blockAfter(styles, "@media (min-width: 769px)");
  assert.match(desktopRules, /body\.custom-cursor-active[\s\S]*cursor:\s*none/);
  assert.match(desktopRules, /body\.custom-cursor-active \.cursor-dot[\s\S]*display:\s*block/);
  assert.match(desktopRules, /body\.custom-cursor-active \.cursor-ring[\s\S]*display:\s*block/);
});

test("pages without both custom-cursor elements keep initializing navigation at every breakpoint", () => {
  [600, 768, 769, 1280].forEach((width) => {
    [
      { cursorDotPresent: false, cursorRingPresent: false },
      { cursorDotPresent: true, cursorRingPresent: false },
      { cursorDotPresent: false, cursorRingPresent: true },
    ].forEach((cursorElements) => {
      const page = runSiteScript({ ...cursorElements, width });

      assert.doesNotThrow(() => page.documentListeners.get("DOMContentLoaded")());
      assert.equal(page.body.classList.contains("custom-cursor-active"), false);
      assert.equal(typeof page.navToggle.listeners.get("click"), "function");
    });
  });
});

test("mobile pages retain the native cursor even when custom-cursor elements exist", () => {
  [600, 768].forEach((width) => {
    const page = runSiteScript({ cursorDotPresent: true, cursorRingPresent: true, width });

    page.documentListeners.get("DOMContentLoaded")();

    assert.equal(page.body.classList.contains("custom-cursor-active"), false);
    assert.equal(page.documentListeners.has("mousemove"), false);
    assert.equal(typeof page.navToggle.listeners.get("click"), "function");
  });
});

test("desktop pages with both custom-cursor elements activate and track mouse movement", () => {
  [769, 1280].forEach((width) => {
    const page = runSiteScript({ cursorDotPresent: true, cursorRingPresent: true, width });

    page.documentListeners.get("DOMContentLoaded")();
    page.documentListeners.get("mousemove")({ clientX: 123, clientY: 456 });

    assert.equal(page.body.classList.contains("custom-cursor-active"), true);
    assert.equal(page.cursorDot.style.left, "123px");
    assert.equal(page.cursorDot.style.top, "456px");
  });
});
