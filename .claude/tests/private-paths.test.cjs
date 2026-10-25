// Netlify publishes _site/, built by netlify/build-site.cjs from the repo
// checkout. This fails if an internal file (page generators, blog source data,
// agent notes, function source, package/config files) would be published, if a
// real page or asset would be left out, or if the second-layer 404! rules in
// _redirects go missing.
//   node .claude/tests/private-paths.test.cjs
'use strict';
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '../..');
const { isPublic, build, missingRootRefs } = require(path.join(ROOT, 'netlify/build-site.cjs'));

// Netlify builds from a clean clone, so what it sees is the tracked files.
const tracked = execFileSync('/usr/bin/git', ['ls-files', '-z'], { cwd: ROOT, encoding: 'utf8' }).split('\0').filter(Boolean);

// 1. Nothing internal is published.
const INTERNAL = (f) => f.split('/').some((p) => p.startsWith('.')) || /^(docs|scripts|netlify|tools|blog-data|node_modules)\//i.test(f) ||
  (/\.(md|mjs|cjs|py|pyc|sh|json|toml|csv|xlsx?)$/i.test(f) && f !== 'availability.json');
const leaks = tracked.filter((f) => INTERNAL(f) && isPublic(f));
assert.deepStrictEqual(leaks, [], 'internal files that would be published:\n  ' + leaks.join('\n  '));
for (const f of ['tools/generate_blog.py', 'Tools/generate_blog.py', 'tools/__pycache__/generate_core_pages.cpython-314.pyc',
  'blog-data/lumber-prices-2026.json', 'Blog-Data/_backfill_plan.json', 'netlify/functions/submission-created.js',
  'Netlify/functions/_lib/lead-guard.js', 'netlify/build-site.cjs', 'package.json', 'package-lock.json', 'netlify.toml',
  'CLAUDE.md', 'AGENTS.md', '.claude/tests/lead-guard.test.cjs', '.marketing/linkedin-posts-6weeks.md', 'leads/list.csv', 'pasted-tool.js']) {
  assert.ok(!isPublic(f), f + ' would be published');
}

// 2. Every page and asset is still published, including the runtime-fetched banner data.
const WEB = /\.(html?|css|js|jpe?g|png|gif|webp|avif|svg|ico|mov|mp4|webm|pdf|txt|xml|webmanifest|woff2?|ttf|otf)$/i;
const dropped = tracked.filter((f) => !INTERNAL(f) && (WEB.test(f) || f === '_headers' || f === '_redirects' || f === 'availability.json') && !isPublic(f));
assert.deepStrictEqual(dropped, [], 'website files that would be left out:\n  ' + dropped.join('\n  '));
for (const f of ['availability.json', 'script.js', 'careers.js', 'js/human-check.js', 'styles.css', 'careers.css', '_headers', '_redirects']) {
  assert.ok(isPublic(f), f + ' would be left out');
}
const kept = tracked.filter(isPublic);
assert.ok(kept.filter((f) => f.endsWith('.html')).length > 1400, 'too few pages would be published');

// 3. build() on a small tree: private dirs pruned in any letter case, files hard-linked, output not re-copied,
//    and a page that points at a root script the filter left out is reported.
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'build-site-'));
try {
  const put = (rel, body = rel) => { fs.mkdirSync(path.dirname(path.join(tmp, rel)), { recursive: true }); fs.writeFileSync(path.join(tmp, rel), body); };
  ['js/human-check.js', 'blog/a.html', 'images/a.jpg', '_redirects', 'llms.txt', 'availability.json', 'careers.js',
    'Tools/x.py', 'blog-data/y.json', 'NETLIFY/functions/notify.js', 'scripts/z.mjs', '.claude/t.cjs', 'CLAUDE.md', 'package.json', 'a.js'].forEach((f) => put(f));
  put('index.html', '<script src="/script.js"></script><script src="careers.js"></script>');
  put('script.js', "fetch('/availability.json')");
  put('_site/stale.html');
  const out = path.join(tmp, '_site');
  const got = build(tmp, out).sort();
  assert.deepStrictEqual(got, ['_redirects', 'availability.json', 'blog/a.html', 'careers.js', 'images/a.jpg', 'index.html', 'js/human-check.js', 'llms.txt', 'script.js']);
  assert.ok(!fs.existsSync(path.join(out, 'stale.html')), 'old _site contents were kept');
  assert.strictEqual(fs.statSync(path.join(out, 'index.html')).ino, fs.statSync(path.join(tmp, 'index.html')).ino, 'not hard-linked');
  assert.deepStrictEqual(missingRootRefs(out, got), []);
  fs.writeFileSync(path.join(out, 'blog/a.html'), '<script src="/a.js"></script>');
  assert.deepStrictEqual(missingRootRefs(out, got), ['a.js (in blog/a.html)']);
} finally { fs.rmSync(tmp, { recursive: true, force: true }); }

// 4. Second layer: exact-case 404! rules stay in _redirects.
const rules = fs.readFileSync(path.join(ROOT, '_redirects'), 'utf8').split('\n').map((l) => l.trim().split(/\s+/))
  .filter((p) => p.length >= 3 && p[2] === '404!' && !p[0].startsWith('#')).map((p) => p[0]);
for (const r of ['/netlify/*', '/tools/*', '/blog-data/*', '/package.json']) {
  assert.ok(rules.includes(r), '_redirects lost its ' + r + ' 404! rule');
}

// 5. netlify.toml publishes the filtered folder.
const toml = fs.readFileSync(path.join(ROOT, 'netlify.toml'), 'utf8');
assert.match(toml, /^\s*command\s*=\s*"node netlify\/build-site\.cjs"/m);
assert.match(toml, /^\s*publish\s*=\s*"_site"/m);

console.log('ok: ' + tracked.length + ' tracked files, ' + kept.length + ' published, ' + (tracked.length - kept.length) + ' internal left out');
