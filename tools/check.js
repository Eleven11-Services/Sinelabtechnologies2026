// Site check: serves site/ locally, then for every page on desktop (1440x900) and phone (390x844):
//   - console errors, failed requests (4xx/5xx), broken images, external requests
//   - axe-core accessibility scan (WCAG 2.0/2.1/2.2 A + AA + best practice), with reduced motion on
// Exit code 1 if anything fails.
//
// Setup once:   npm install        (installs playwright + axe-core from package.json)
//               npx playwright install chromium
// Run:          node tools/check.js            (all pages)
//               node tools/check.js about.html  (one page)
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');

const ROOT = path.join(__dirname, '..', 'site');
const PAGES = process.argv.slice(2).length ? process.argv.slice(2)
  : ['index.html', 'about.html', 'solutions.html', 'projects.html', 'gallery.html', 'contact.html'];
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.webp': 'image/webp', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.mp4': 'video/mp4', '.webm': 'video/webm', '.json': 'application/json' };

const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]).replace(/\/$/, '/index.html'));
  if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end('not found'); }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(res);
});

(async () => {
  await new Promise(r => server.listen(0, r));
  const base = `http://localhost:${server.address().port}/`;
  const axePath = require.resolve('axe-core/axe.min.js');
  // Playwright's own Chromium if installed, else the system Edge or Chrome
  const browser = await chromium.launch().catch(() => chromium.launch({ channel: 'msedge' }))
    .catch(() => chromium.launch({ channel: 'chrome' }));
  let failed = 0;
  for (const [w, h, tag] of [[1440, 900, 'desktop'], [390, 844, 'phone']]) {
    for (const page of PAGES) {
      const ctx = await browser.newContext({ viewport: { width: w, height: h }, isMobile: w < 800, hasTouch: w < 800, reducedMotion: 'reduce' });
      const pg = await ctx.newPage(); const problems = [];
      pg.on('pageerror', e => problems.push('script error: ' + e.message));
      pg.on('console', m => { if (m.type() === 'error') problems.push('console: ' + m.text()); });
      pg.on('response', r => { if (r.status() >= 400) problems.push(`HTTP ${r.status()}: ${r.url()}`); });
      pg.on('request', r => { const u = r.url(); if (!u.startsWith(base) && !u.startsWith('data:') && !/formsubmit\.co|google\.com\/maps|wa\.me/.test(u)) problems.push('external request: ' + u); });
      await pg.goto(base + page, { waitUntil: 'load' });
      const H = await pg.evaluate(() => document.documentElement.scrollHeight);
      for (let y = 0; y < H; y += 700) { await pg.evaluate(y => scrollTo(0, y), y); await pg.waitForTimeout(40); }
      await pg.waitForTimeout(600);
      const broken = await pg.evaluate(() => [...document.images].filter(i => i.getAttribute('src') && i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src')));
      broken.forEach(b => problems.push('broken image: ' + b));
      await pg.addScriptTag({ path: axePath });
      const res = await pg.evaluate(async () => await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] }, resultTypes: ['violations'] }));
      res.violations.forEach(v => problems.push(`a11y ${v.id} (${v.impact}): ${v.help} – ${v.nodes.slice(0, 3).map(n => n.target.join(' ')).join(' | ')}`));
      console.log(`${problems.length ? '✗' : '✓'} ${tag.padEnd(7)} ${page}${problems.length ? '' : '  ok'}`);
      problems.forEach(p => console.log('    ' + p));
      failed += problems.length; await ctx.close();
    }
  }
  await browser.close(); server.close();
  console.log(failed ? `\n${failed} problem(s) found` : '\nAll pages clean');
  process.exit(failed ? 1 : 0);
})();
