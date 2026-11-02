// Screenshots of every page (desktop 1440 wide + phone 390 wide) into ./screenshots/, for reviewing changes.
//   node tools/screenshots.js                 full pages
//   node tools/screenshots.js --viewport      first screen only
//   node tools/screenshots.js about.html      one page
// The homepage hero changes from day to night as you scroll; full-page shots show the end state of scroll effects.
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..', 'site'), OUT = path.join(__dirname, '..', 'screenshots');
const args = process.argv.slice(2), viewportOnly = args.includes('--viewport');
const PAGES = args.filter(a => a.endsWith('.html')).length ? args.filter(a => a.endsWith('.html'))
  : ['index.html', 'about.html', 'solutions.html', 'projects.html', 'gallery.html', 'contact.html'];
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.woff2': 'font/woff2', '.mp4': 'video/mp4', '.webm': 'video/webm', '.svg': 'image/svg+xml' };
const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]).replace(/\/$/, '/index.html'));
  if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(res);
});
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  await new Promise(r => server.listen(0, r)); const base = `http://localhost:${server.address().port}/`;
  const browser = await chromium.launch();
  for (const [w, h, tag] of [[1440, 900, 'desktop'], [390, 844, 'phone']]) {
    for (const page of PAGES) {
      const pg = await browser.newPage({ viewport: { width: w, height: h }, isMobile: w < 800, hasTouch: w < 800 });
      await pg.goto(base + page, { waitUntil: 'load' }); await pg.waitForTimeout(800);
      if (!viewportOnly) {   // scroll through once so lazy images load and reveal animations finish
        const H = await pg.evaluate(() => document.documentElement.scrollHeight);
        for (let y = 0; y < H; y += 600) { await pg.evaluate(y => scrollTo(0, y), y); await pg.waitForTimeout(60); }
        await pg.evaluate(() => scrollTo(0, 0)); await pg.waitForTimeout(800);
      }
      const file = path.join(OUT, `${page.replace('.html', '')}-${tag}.png`);
      await pg.screenshot({ path: file, fullPage: !viewportOnly }); console.log(file); await pg.close();
    }
  }
  await browser.close(); server.close();
})();
