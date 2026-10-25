// Builds _site/, the folder Netlify publishes (see netlify.toml), from the repo
// checkout: every website file, hard-linked (nothing is copied), and none of
// the internal ones.
//
// Why: the site used to publish the repo root, so the page generators
// (tools/*.py), the blog source data (blog-data/*.json, rendered into blog/ by
// tools/generate_blog.py at authoring time), package.json and the function
// source (netlify/functions/*.js, including the lead guard) were public URLs.
// _redirects 404! rules did not close that: Netlify serves file paths
// case-insensitively but matches redirect rules case-sensitively, so
// /Tools/generate_blog.py and /Netlify/functions/submission-created.js still
// returned the files (found 2026-10-25). A file that is not deployed can't leak.
//
//   node netlify/build-site.cjs                 (what Netlify runs)
//   node netlify/build-site.cjs <src> <out>     (local check against an export)
'use strict';
const fs = require('fs');
const path = require('path');

// Top-level folders that are never part of the website (matched case-insensitively).
const PRIVATE_DIRS = new Set(['netlify', 'tools', 'blog-data', 'docs', 'scripts', 'node_modules', 'marketing', 'outreach', 'leads', '_site']);
// File types that are never pages or assets here: notes, scripts, data, config.
const PRIVATE_EXT = /\.(md|markdown|mjs|cjs|py|pyc|sh|csv|tsv|xlsx?|json|toml|ya?ml|env|log|bak|sql|sqlite|db|zip)$/i;
// Root-level files that match PRIVATE_EXT but ARE public: script.js fetches
// /availability.json at runtime for the sitewide crew-availability banner.
const PUBLIC_ALLOW = new Set(['availability.json']);
// Root-level .js that are page assets. Any other root .js (a tool or a pasted
// script) is left out; the reference check below fails the build if a page
// needs one that was left out.
const ROOT_JS_ALLOW = new Set(['script.js', 'careers.js']);

// rel: path relative to the repo root, with / separators.
function isPublic(rel) {
  const parts = rel.split('/');
  if (parts.some((p) => p.startsWith('.'))) return false; // .claude/, .git/, .marketing/, .netlify/, .env ...
  if (parts.length > 1 && PRIVATE_DIRS.has(parts[0].toLowerCase())) return false;
  if (parts.length === 1 && PUBLIC_ALLOW.has(rel)) return true;
  if (PRIVATE_EXT.test(rel)) return false;
  if (parts.length === 1 && /\.js$/i.test(rel)) return ROOT_JS_ALLOW.has(rel);
  return true;
}

function build(src, out) {
  src = path.resolve(src);
  out = path.resolve(out);
  fs.rmSync(out, { recursive: true, force: true });
  fs.mkdirSync(out, { recursive: true });
  const published = [];
  (function walk(dir) {
    for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
      const abs = path.join(dir, ent.name);
      if (abs === out) continue;
      const rel = path.relative(src, abs).split(path.sep).join('/');
      if (ent.isDirectory()) {
        if (ent.name.startsWith('.') || (dir === src && PRIVATE_DIRS.has(ent.name.toLowerCase()))) continue;
        walk(abs);
        continue;
      }
      if (!ent.isFile() || !isPublic(rel)) continue; // symlinks, sockets: skipped
      const dest = path.join(out, rel);
      fs.mkdirSync(path.dirname(dest), { recursive: true });
      try { fs.linkSync(abs, dest); } catch (e) { fs.copyFileSync(abs, dest); }
      published.push(rel);
    }
  })(src);
  return published;
}

// Root-level .js/.json that a published page or script points at but that is
// not in the output (a page asset the filter would wrongly drop).
function missingRootRefs(out, published) {
  const have = new Set(published);
  const missing = new Set();
  for (const f of published) {
    if (!/\.(html?|js)$/i.test(f)) continue;
    const text = fs.readFileSync(path.join(out, f), 'utf8');
    for (const m of text.matchAll(/["'(]\/?([A-Za-z0-9_-]+\.(?:js|json))(?:[?#][^"')]*)?["')]/g)) {
      if (!have.has(m[1])) missing.add(m[1] + ' (in ' + f + ')');
    }
  }
  return [...missing];
}

if (require.main === module) {
  const root = path.resolve(__dirname, '..');
  const src = process.argv[2] || root;
  const out = process.argv[3] || path.join(src, '_site');
  const published = build(src, out);
  // Fail the build (Netlify then keeps the live deploy) rather than publish a broken site.
  for (const must of ['index.html', 'contact.html', 'estimate.html', 'careers.html', 'for-gcs.html', 'blog.html', '_redirects', '_headers',
    'script.js', 'careers.js', 'js/human-check.js', 'availability.json', 'styles.css', 'sitemap.xml', 'robots.txt']) {
    if (!fs.existsSync(path.join(out, must))) { console.error('build-site: missing ' + must); process.exit(1); }
  }
  const pages = published.filter((f) => /\.html$/i.test(f)).length;
  if (pages < 1400) { console.error('build-site: only ' + pages + ' pages, refusing to publish'); process.exit(1); }
  const bad = published.filter((f) => !isPublic(f));
  if (bad.length) { console.error('build-site: internal files in output: ' + bad.join(', ')); process.exit(1); }
  const missing = missingRootRefs(out, published);
  if (missing.length) { console.error('build-site: pages reference files left out of the site: ' + missing.join(', ')); process.exit(1); }
  console.log('build-site: published ' + published.length + ' files (' + pages + ' pages) to ' + path.relative(process.cwd(), out));
}

module.exports = { isPublic, build, missingRootRefs, PRIVATE_DIRS, PRIVATE_EXT, PUBLIC_ALLOW, ROOT_JS_ALLOW };
