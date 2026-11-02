# Gallery page: four categories from the content document, a masonry grid with filters, and a full-screen photo viewer.
# Highlights and the start of the grid are Sinelab's own drone photos (29 Oct); remaining sample photos stay clearly labelled.
# Shares the homepage stylesheet, nav, footer and scripts (from src_draft.html) and the About hero / closing-card styles.
import re, base64, json
d = '/tmp/claude-0/site/'
home = open(d + 'src_draft.html').read()
about_py = open(d + 'about.py').read()
ABOUT_CSS = about_py[about_py.index("CSS = '''") + 9:about_py.index("'''\nhead = head[:head.rindex")]
def cut(a, b, src=home):
    i = src.index(a); j = src.index(b, i + len(a)); return src[i:j]
def rp(s, a, b):
    assert a in s, a[:80]; return s.replace(a, b)

ARR = '<svg class="arr" width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 9h10M10 5l4 4-4 4"/></svg>'
LINKS = [('#team', 'index.html#team'), ('#contact', 'index.html#contact'), ('#blog', 'index.html#blog'), ('#top', 'index.html')]
def relink(html):
    for a, b in LINKS: html = html.replace(f'href="{a}"', f'href="{b}"')
    return html

head = home[:home.index('<!-- ======= NAV ======= -->')]
head = head.replace('<title>Sinelab Website</title>', '<title>Gallery | Sinelab Technologies</title>')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="A glimpse into Sinelab Technologies: solar installations, manufacturing, our people at work and the milestones behind the company.">', head)
nav = relink(cut('<!-- ======= NAV ======= -->', '<main id="top">'))
nav = rp(nav, '<a href="gallery.html">Gallery</a>', '<a href="gallery.html" aria-current="page">Gallery</a>')
nav = rp(nav, '<a href="gallery.html" style="--i:3">Gallery', '<a href="gallery.html" style="--i:3" aria-current="page">Gallery')
foot = relink(home[home.index('<footer'):home.index('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js">')])

js_core = cut('(function(){\nconst reduce', '/* ---------- Solar panel model')
js_nav = cut('/* ---------- Floating glass nav: compact', '/* ---------- Why Sinelab: the reason nearest')
js_nav = rp(js_nav, "['#anatomy','#films','#savings','#faq','footer']", "['#gl-hero','footer']")
js_nav = rp(js_nav, "['#why','#solutions','#projects','#gallery','#faq','#blog','#contact']", "['#photos']")

# ---------- content ----------
CATS = [('installations', 'Solar installations', 'Rooftop, ground-mounted, residential, commercial and industrial.'),
        ('manufacturing', 'Manufacturing &amp; innovation', 'Cables, batteries, inverters, lighting and production facilities.'),
        ('people', 'People at work', 'Engineering, installation, commissioning and team activities.'),
        ('milestones', 'Milestones &amp; recognition', 'Awards, company achievements and significant events.')]
CNAME = {k: n for k, n, _ in CATS}
ICON = {
  'manufacturing': '<svg viewBox="0 0 44 44" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><rect x="12" y="10" width="20" height="28" rx="2"/><path d="M18 6h8v4h-8zM23 17l-4 7h6l-4 7"/></svg>',
  'people': '<svg viewBox="0 0 44 44" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><circle cx="16" cy="15" r="5"/><circle cx="30" cy="17" r="4"/><path d="M6 36c0-6 4.5-10 10-10s10 4 10 10M26 27c5 0 10 3 10 9"/></svg>',
  'milestones': '<svg viewBox="0 0 44 44" fill="none" stroke="currentColor" stroke-width="1.3" aria-hidden="true"><circle cx="22" cy="17" r="10"/><path d="M15 25l-4 14 6-2 3 5 2-10M29 25l4 14-6-2-3 5-2-10"/></svg>'}
# (category, image or None, title, shape) – shapes give the masonry its rhythm: w = landscape, s = square, t = tall
ITEMS = [
  ('installations', 'g_pj_drone.jpg', 'Rooftop array from above', 'w'),
  ('manufacturing', None, 'Lithium battery assembly, Kanjikode', 't'),
  ('installations', 'g_proj3.jpg', 'Family home with rooftop solar at sunset', 's'),
  ('installations', 'g_pj_array.jpg', 'Rooftop panels, close up', 't'),
  ('people', None, 'Installation crew on a rooftop', 'w'),
  ('installations', 'g_proj2.jpg', 'Tiled-roof home with a full array', 'w'),
  ('milestones', None, '2018 Asianet Keerthimudra Award', 's'),
  ('installations', 'g_pj_render.jpg', 'Contemporary home with rooftop solar', 't'),
  ('manufacturing', None, 'Integrated inverter testing', 'w'),
  ('installations', 'g_proj1.jpg', 'Two-storey home with a rooftop array', 's'),
  ('people', None, 'Commissioning a solar plant', 't'),
  ('installations', 'g_blog2.jpg', 'Solar home after sunset', 'w'),
  ('manufacturing', None, 'Industrial lighting production', 's'),
  ('installations', 'g_blog1.jpg', 'Rooftop solar on a modern home', 't'),
  ('milestones', None, 'Flagship 1 MW rooftop installation, 2026', 'w'),
  ('installations', 'g_blog3.jpg', 'Tiled roof, full array', 's'),
  ('people', None, 'Our engineers at work', 'w'),
  ('manufacturing', None, 'Kanjikode manufacturing facility', 't'),
  ('installations', 'g_day.jpg', 'Home with solar, garden view', 'w'),
  ('milestones', None, '20 kW off-grid project, Nelliampathy Hills, 2019', 's'),
]
count = {k: sum(1 for it in ITEMS if it[0] == k) for k, _, _ in CATS}
filters = [f'        <button type="button" class="pf on" data-f="all" aria-pressed="true">All<span>{len(ITEMS)}</span></button>'] + \
          [f'        <button type="button" class="pf" data-f="{k}" aria-pressed="false">{n}<span>{count[k]}</span></button>' for k, n, _ in CATS]

def tile(k, it):
    cat, img, title, shape = it
    if img:
        inner = f'<img src="{{{{L:{img}}}}}" data-g="{img}" alt="" loading="lazy"' + (f' style="object-position:{FOCUS[img]}"' if img in FOCUS else '') + '>' + ('' if img.startswith('real_') else '<span class="hl-ph">Sample photo</span>')
        label = f'Open photo: {title}'
    else:
        inner = f'<span class="gt-ph"><span class="gt-ico">{ICON[cat]}</span><span class="gt-tba">Photo to be added</span></span>'
        label = f'Open: {title}, photo to be added'
    return f'''        <li class="gt {shape}{"" if img else " ph"}" data-cat="{cat}" style="--k:{k % 6}">
          <button type="button" class="gt-open" data-k="{k}" aria-haspopup="dialog" aria-label="{label}">
            <span class="gt-img">{inner}<span class="gt-zoom" aria-hidden="true"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M8 3H3v5M12 3h5v5M8 17H3v-5M12 17h5v-5"/></svg></span></span>
          </button>
          <p class="gt-cap"><span>{CNAME[cat]}</span>{title}</p>
        </li>'''
ITEMS = [it for it in ITEMS if it[1]]          # user: show only the photos we already have (the shot list stays in the notes)
SHAPES = ['w', 's', 't', 'w', 't', 's', 'w', 's', 't', 'w']
ITEMS = [(c, i, t, SHAPES[(k + 4) % len(SHAPES)]) for k, (c, i, t, _) in enumerate(ITEMS)]
REAL = [('installations', 'real_bala.jpg', 'Bala Cinemas, rooftop solar from the air', 't'),
        ('installations', 'real_bava.jpg', 'Bava Metals, panels along the metal roofs', 'w'),
        ('installations', 'real_bajaj.jpg', 'Grand Bajaj Showroom, array on a raised frame over the terrace', 't'),
        ('installations', 'real_jamal.jpg', 'Jamal Sons, rooftop solar on a main road', 's'),
        ('installations', 'real_psurg.jpg', 'Palakkad Surgicals, panels on the side block', 'w'),
        ('installations', 'real_sinicon.jpg', 'Sinicon, panels across the factory roofs', 'w'),
        ('installations', 'real_salim.jpg', 'Salim Hybrid Residence, panels on the flat roofs', 'w')]
REAL_IMGS = {it[1] for it in REAL}
FOCUS = {'real_bava.jpg': '30% 50%', 'real_psurg.jpg': '40% 50%', 'real_sinicon.jpg': '62% 50%'}
ITEMS = REAL + ITEMS
count = {k: sum(1 for it in ITEMS if it[0] == k) for k, _, _ in CATS}
CATS_LIVE = [c for c in CATS if count[c[0]]]
filters = [f'        <button type="button" class="pf on" data-f="all" aria-pressed="true">All<span>{len(ITEMS)}</span></button>'] + \
          [f'        <button type="button" class="pf" data-f="{k}" aria-pressed="false">{n}<span>{count[k]}</span></button>' for k, n, _ in CATS_LIVE]
tiles = '\n'.join(tile(k, it) for k, it in enumerate(ITEMS) if k >= len(REAL))
real_tiles = '\n'.join(tile(k, it) for k, it in enumerate(ITEMS) if k < len(REAL))
DATA = json.dumps([{'cat': CNAME[c].replace('&amp;', '&'), 'title': t, 'img': bool(i), 'real': bool(i and i.startswith('real_')), 'icon': c} for c, i, t, _ in ITEMS], ensure_ascii=False)
cats_html = '\n'.join(f'''        <li><a href="#{k}" class="gc" data-f="{k}"><span class="gc-n">{n_ + 1:02d}</span><b>{n}</b><span class="gc-d">{desc}</span><span class="gc-c">{count[k]} {"item" if count[k] == 1 else "items"}</span></a></li>'''
                      for n_, (k, n, desc) in enumerate(CATS_LIVE))

# highlights deck: Sinelab's four real projects, slid sideways one after another
HL = [('real_bala_card.jpg', 'Bala Cinemas', 'Rooftop solar · Cinema', 'Enphase microinverters handle shading on a challenging roof.'),
      ('real_bajaj_card.jpg', 'Grand Bajaj Showroom', 'Rooftop solar · Showroom', 'Panels on a raised steel frame above the flat terrace.'),
      ('real_bava_card.jpg', 'Bava Metals', 'Rooftop solar · Commercial', 'Panels set along the metal roofs of a busy town-centre building.'),
      ('real_salim_card.jpg', 'Salim Hybrid Residence', 'Hybrid solar · Residential', 'Hybrid solar with battery backup, designed around a family home.'),   # user: replaces Jamal Sons in the highlights
      ('real_psurg_card.jpg', 'Palakkad Surgicals', 'Rooftop solar · Manufacturing', 'Panels on the roof of the block beside the main factory building.'),
      ('real_sinicon_card.jpg', 'Sinicon', 'Rooftop solar · Industrial', 'Rows of panels across the factory’s sloped metal roof and flat roof.')]
NH = len(HL)
hcards = '\n'.join(f'''          <div class="hc" style="--z:{NH - i}">
            <div class="hc-f"><img src="{{{{L:{im}}}}}" alt=""{' loading="lazy"' if i else ''}><i class="hc-shade"></i></div>
          </div>''' for i, (im, *_r) in enumerate(HL))
hsegs = ''.join(f'<i style="--s:{i}"></i>' for i in range(NH))
HL_DATA = json.dumps([{'name': n, 'kind': k, 'line': l} for _, n, k, l in HL], ensure_ascii=False)

CLOSE = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M5 5l10 10M15 5L5 15"/></svg>'
PREV = '<svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M14 9H4M8 5L4 9l4 4"/></svg>'
NEXT = '<svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 9h10M10 5l4 4-4 4"/></svg>'

body = f'''{nav}
<main id="top">

<!-- ======= HIGHLIGHTS: photos slide sideways, one after another, as you scroll ======= -->
<section class="gh" id="gl-hero" aria-labelledby="glTitle" style="--n:{NH}">
  <div class="gh-sticky">
    <div class="wrap gh-in">
      <div class="gh-copy">
        <nav class="ab-crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">Gallery</span></nav>
        <h1 class="ab-h1" id="glTitle"><span class="ln"><span>A glimpse into</span></span><span class="ln"><span><em>our world.</em></span></span></h1>
        <div class="gh-cap" id="ghCap">
          <div class="gh-num"><b id="ghNum">01</b><span>/ {NH:02d}</span></div>
          <p class="gh-kind" id="ghKind"></p>
          <p class="gh-title" id="ghTitle"></p>
          <p class="gh-line" id="ghLine"></p>
        </div>
        <p class="sr-only" id="ghLive" aria-live="polite"></p>
        <div class="gh-ctrl">
          <button type="button" class="gh-arrow" id="ghPrev" aria-label="Previous highlight">{PREV}</button>
          <span class="gh-segs" aria-hidden="true">{hsegs}</span>
          <button type="button" class="gh-arrow" id="ghNext" aria-label="Next highlight">{NEXT}</button>
        </div>
        <a class="gh-skip" href="#photos">Skip to all photos <svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M9 4v10M5 10l4 4 4-4"/></svg></a>
      </div>
      <div class="gh-stage">
        <div class="gh-deck" id="ghDeck">
{hcards}
        </div>
        <p class="gh-hint" aria-hidden="true"><span class="gh-hint-d">Scroll to see the next</span><span class="gh-hint-m">Swipe for the next</span></p>
      </div>
    </div>
  </div>
</section>

<!-- ======= PHOTOS ======= -->
<section class="gl band" id="photos" aria-labelledby="photosTitle">
  <div class="wrap">
    <div class="sec-head">
      <div><div class="eyebrow">All photos</div><h2 id="photosTitle">Our work <em>in pictures</em></h2></div>
      <p>From manufacturing floors to megawatt-scale solar installations, explore the people, engineering and milestones behind Sinelab.</p>
    </div>
{('    <ul class="gcats">' + chr(10) + cats_html + chr(10) + '    </ul>' + chr(10) + '    <div class="pf-bar" role="group" aria-label="Filter the gallery">' + chr(10) + chr(10).join(filters) + chr(10) + '    </div>') if len(CATS_LIVE) > 1 else ''}
    <p class="sr-only" id="gfStatus" role="status" aria-live="polite"></p>
    <h3 class="gm-h">Sinelab projects</h3>
    <ul class="gm gm-real" id="gmReal">
{real_tiles}
    </ul>
    <h3 class="gm-h">Sample photos <span>Placeholders, not Sinelab work. They will be replaced as more of Sinelab’s own photographs arrive.</span></h3>
    <ul class="gm" id="gm">
{tiles}
    </ul>
  </div>
</section>

<!-- ======= CALL TO ACTION ======= -->
<section class="ab-cta" id="cta">
  <div class="wrap">
    <div class="ab-cta-card">
      <div class="ab-cta-img" aria-hidden="true"><img src="{{{{L:cta_night.jpg}}}}" alt=""></div>
      <div class="ab-cta-copy">
        <span class="ab-cta-k">Like what you see?</span>
        <h2>Let’s power <em>your next move</em></h2>
        <p>Planning solar for your home, business or plant? Our team is here to help.</p>
        <div class="ab-cta-btns">
          <a class="btn btn-sun" href="index.html#contact">Get a free quote {ARR}</a>
          <a class="btn ab-btn-ghost" href="projects.html">See our projects</a>
        </div>
      </div>
      <dl class="ab-cta-meta">
        <div><dt>Email</dt><dd><a href="mailto:info@sinelabtechnologies.com">info@sinelabtechnologies.com</a></dd></div>
        <div><dt>Phone</dt><dd><a href="tel:+919946207738">+91 99462 07738</a></dd></div>
        <div><dt>Offices</dt><dd>Palakkad · Kochi, Kerala</dd></div>
      </dl>
    </div>
  </div>
</section>

</main>

<!-- ======= PHOTO VIEWER ======= -->
<dialog class="lb" id="lb" aria-labelledby="lbTitle" data-lenis-prevent>
  <button type="button" class="lb-close" id="lbClose" aria-label="Close viewer">{CLOSE}</button>
  <div class="lb-stage" id="lbStage">
    <img id="lbImg" src="" alt="">
    <div class="lb-ph" id="lbPh"><span class="gt-ico" id="lbIco"></span><span class="gt-tba">Photo to be added</span></div>
    <span class="hl-ph" id="lbSample">Sample photo</span>
  </div>
  <div class="lb-bar">
    <div class="lb-cap"><span id="lbCat"></span><h2 id="lbTitle"></h2></div>
    <div class="lb-nav">
      <button type="button" class="lb-arrow" id="lbPrev" aria-label="Previous photo">{PREV}</button>
      <span class="lb-count" id="lbCount"></span>
      <button type="button" class="lb-arrow" id="lbNext" aria-label="Next photo">{NEXT}</button>
    </div>
  </div>
</dialog>

{foot}'''

CSS = ABOUT_CSS + '''
/* ================= Gallery page ================= */
/* highlights deck (dark). Desktop: a tall section with a sticky inner; scroll progress turns the cards. */
.gh{position:relative;height:calc(100svh + (var(--n) - 1) * 72svh);background:var(--navy-deep);color:#fff}
.gh-sticky{position:sticky;top:0;height:100svh;min-height:640px;display:flex;align-items:center;overflow:hidden;isolation:isolate}
.gh-sticky::before{content:"";position:absolute;inset:0;z-index:-1;background:radial-gradient(60% 70% at 72% 50%,rgba(249,194,46,.10) 0%,rgba(249,194,46,0) 60%),radial-gradient(rgba(255,255,255,.07) 1px,transparent 1.2px) 0 0/24px 24px}
.gh-in{width:100%;display:grid;grid-template-columns:minmax(0,.82fr) minmax(0,1.18fr);gap:clamp(36px,5vw,90px);align-items:center;padding-top:70px}
.gh.in .ab-crumb{opacity:1;transform:none}
.gh.in .ab-h1 .ln:nth-child(1)>span{transform:none;transition-delay:.1s}
.gh.in .ab-h1 .ln:nth-child(2)>span{transform:none;transition-delay:.45s}
.gh .ab-h1{margin-top:18px;font-size:clamp(38px,4.4vw,68px)}
.gh-cap{margin-top:clamp(28px,4vh,48px);padding-top:22px;border-top:1px solid rgba(255,255,255,.14);min-height:170px;transition:opacity .35s ease}
.gh-cap.swap{opacity:0}
.gh-num{display:flex;align-items:baseline;gap:8px;font:500 12px var(--f-mono);letter-spacing:.06em;color:rgba(255,255,255,.7)}
.gh-num b{font:300 44px/1 var(--f-display);letter-spacing:-0.04em;color:var(--sun)}
.gh-kind{margin:14px 0 0;font:500 12px var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.75)}
.gh-title{margin:8px 0 0;font-size:clamp(26px,2.4vw,36px);font-weight:300;letter-spacing:-0.035em;line-height:1.1;color:#fff}
.gh-line{margin:10px 0 0;max-width:40ch;font-size:16px;line-height:1.55;color:var(--on-dark-muted)}
.gh-ctrl{display:flex;align-items:center;gap:14px;margin-top:26px}
.gh-arrow{display:grid;place-items:center;width:48px;height:48px;border:1px solid rgba(255,255,255,.25);border-radius:50%;background:rgba(255,255,255,.05);color:#fff;cursor:pointer;transition:background .3s,border-color .3s,color .3s}
.gh-arrow:hover:not(:disabled){background:var(--sun);border-color:var(--sun);color:var(--ink)}
.gh-arrow:disabled{opacity:.35;cursor:default}
.gh-arrow svg{width:18px;height:18px}
.gh-arrow:focus-visible,.gh-skip:focus-visible{outline:2px solid #fff;outline-offset:3px;box-shadow:0 0 0 3px var(--sun)}
.gh-segs{display:flex;gap:6px}
.gh-segs i{position:relative;display:block;width:28px;height:3px;border-radius:3px;background:rgba(255,255,255,.18);overflow:hidden}
.gh-segs i::after{content:"";position:absolute;inset:0;background:var(--sun);transform:scaleX(var(--f, 0));transform-origin:0 50%}
.gh-skip{display:inline-flex;align-items:center;gap:8px;margin-top:22px;padding-block:8px;font-size:14.5px;color:rgba(255,255,255,.8);text-decoration:underline;text-decoration-color:rgba(249,194,46,.7);text-underline-offset:5px}
.gh-skip svg{width:16px;height:16px}
.gh-stage{position:relative;padding:20px 0 40px;clip-path:inset(-60px -100vw -60px 0)}   /* photos leave on the left edge of the stage, never over the text; the next one peeks in on the right */
.gh-deck{position:relative;width:100%;aspect-ratio:4/3;max-height:calc(100svh - 190px);margin-left:auto}
.hc{position:absolute;inset:0;z-index:var(--z);will-change:transform,opacity}
.hc-f{position:absolute;inset:0;border-radius:22px;overflow:hidden;background:#15151A;box-shadow:0 40px 90px -40px rgba(0,0,0,.8),0 0 0 1px rgba(255,255,255,.06)}
.hc img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.hc-shade{position:absolute;inset:0;background:#000;opacity:0;pointer-events:none}
.hc .hl-ph{top:auto;bottom:14px;left:14px;right:auto}
.gh-hint{position:absolute;left:0;right:0;bottom:4px;margin:0;text-align:center;font:500 11px var(--f-mono);letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.62)}
.gh-hint-m{display:none}
@media (max-width:900px){
  .gh{height:auto}
  .gh-sticky{position:relative;height:auto;min-height:0;padding:110px 0 70px}
  .gh-in{grid-template-columns:1fr;gap:26px;padding-top:0}
  .gh-copy{display:contents}
  .gh .ab-crumb{order:1}.gh .ab-h1{order:2}.gh-stage{order:3}.gh-cap{order:4;margin-top:0;min-height:0}.gh-ctrl{order:5;margin-top:0}.gh-skip{order:6;margin-top:0}
  .gh-stage{padding:6px 0 30px;touch-action:pan-y}
  .gh-deck{max-height:none}
  .gh-hint-d{display:none}.gh-hint-m{display:inline}
}
@media (prefers-reduced-motion: reduce){
  .gh{height:auto}
  .gh-sticky{position:relative;height:auto;min-height:0;padding:130px 0 80px}
  .gh-hint{display:none}
}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.gl{position:relative;isolation:isolate;overflow:clip;padding-block:clamp(90px,11vw,160px) clamp(70px,8vw,120px)}
/* four category cards */
.gcats{list-style:none;margin:0 0 clamp(40px,5vw,70px);padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.gc{position:relative;display:flex;flex-direction:column;height:100%;padding:20px 20px 18px;border-radius:18px;background:var(--paper);color:var(--ink);text-decoration:none;overflow:hidden;isolation:isolate;transition:color .4s}
.gc::before{content:"";position:absolute;inset:0;z-index:-1;background:var(--navy-deep);transform:translateY(101%);transition:transform .55s cubic-bezier(.2,.7,.2,1)}
.gc:hover::before,.gc.on::before{transform:none}
.gc:hover,.gc.on{color:#fff}
.gc-n{font:500 12px var(--f-mono);letter-spacing:.08em;color:var(--accent-ink);transition:color .4s}
.gc:hover .gc-n,.gc.on .gc-n{color:var(--sun)}
.gc b{margin-top:14px;font-size:clamp(19px,1.6vw,23px);font-weight:400;letter-spacing:-0.02em;line-height:1.2}
.gc-d{margin-top:8px;font-size:14.5px;line-height:1.5;color:var(--muted);transition:color .4s}
.gc:hover .gc-d,.gc.on .gc-d{color:var(--on-dark-muted)}
.gc-c{margin-top:auto;padding-top:16px;font:500 11.5px var(--f-mono);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);transition:color .4s}
.gc:hover .gc-c,.gc.on .gc-c{color:rgba(255,255,255,.75)}
/* filter buttons (same as the Projects page) */
.pf-bar{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:clamp(24px,3vw,40px)}
.pf{display:inline-flex;align-items:center;gap:10px;min-height:44px;padding:0 10px 0 18px;border:1px solid var(--line);border-radius:999px;background:#fff;font:inherit;font-size:15px;color:var(--ink);cursor:pointer;transition:background .3s,border-color .3s,color .3s}
.pf span{display:grid;place-items:center;min-width:26px;height:26px;padding:0 6px;border-radius:999px;background:var(--paper);font:500 12px var(--f-mono);color:var(--ink);transition:background .3s}
.pf:hover{border-color:var(--ink)}
.pf.on{background:var(--navy-deep);border-color:var(--navy-deep);color:#fff}
.pf.on span{background:var(--sun);color:var(--ink)}
.pf:focus-visible,.gc:focus-visible{outline:2px solid var(--ink);outline-offset:3px;box-shadow:0 0 0 3px var(--sun)}
/* masonry */
.gm{list-style:none;margin:0;padding:0;columns:3;column-gap:clamp(14px,1.6vw,22px)}
.gt{break-inside:avoid;margin:0 0 clamp(22px,2.4vw,34px)}
.gt.out{display:none}
.gt-open{display:block;width:100%;padding:0;border:0;border-radius:18px;background:none;cursor:zoom-in;font:inherit;color:inherit}
.gt-open:focus-visible{outline:2px solid var(--ink);outline-offset:4px;box-shadow:0 0 0 4px #fff,0 0 0 7px var(--sun)}
.gt-img{position:relative;display:block;overflow:hidden;border-radius:18px;background:var(--paper);clip-path:inset(0 0 100% 0 round 18px);transition:clip-path 1.1s cubic-bezier(.65,0,.25,1) calc(var(--k) * 90ms)}
.gt.in .gt-img{clip-path:inset(0 0 0 0 round 18px)}
.gt.w .gt-img{aspect-ratio:4/3}.gt.s .gt-img{aspect-ratio:1/1}.gt.t .gt-img{aspect-ratio:4/5}
.gt-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:scale(1.15);transition:transform 1.6s cubic-bezier(.2,.7,.2,1) calc(var(--k) * 90ms)}
.gt.in .gt-img img{transform:scale(1.01)}
.gt-open:hover .gt-img img,.gt-open:focus-visible .gt-img img{transform:scale(1.07);transition-delay:0s}
.gt-img .hl-ph{top:auto;bottom:12px;left:12px;right:auto}
.gt-zoom{position:absolute;right:12px;top:12px;display:grid;place-items:center;width:38px;height:38px;border-radius:50%;background:rgba(255,255,255,.92);color:var(--ink);opacity:0;transform:scale(.7);transition:opacity .3s,transform .45s cubic-bezier(.2,.7,.2,1)}
.gt-zoom svg{width:17px;height:17px}
.gt-open:hover .gt-zoom,.gt-open:focus-visible .gt-zoom{opacity:1;transform:none}
.gt-ph{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;background:radial-gradient(90% 80% at 50% 40%,#1C1C22 0%,#0D0D10 75%);color:#fff}
.gt-ph::before{content:"";position:absolute;inset:0;opacity:.5;background-image:radial-gradient(rgba(255,255,255,.09) 1px,transparent 1.2px);background-size:20px 20px}
.gt-ico{position:relative;display:block;width:56px;height:56px;color:var(--sun)}
.gt-ico svg{width:100%;height:100%}
.gt-tba{position:relative;font:500 11px var(--f-mono);letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.75)}
.gt-cap{margin:12px 2px 0;font-size:15px;line-height:1.4;color:var(--ink)}
.gt-cap span{display:block;margin-bottom:3px;font:500 11px var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.gm-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 16px;margin:0 0 clamp(18px,2vw,26px);padding-top:clamp(18px,2vw,26px);border-top:1px solid var(--line);font-size:clamp(20px,1.8vw,24px);font-weight:400;letter-spacing:-0.02em;color:var(--ink)}
.gm-h span{font-size:14.5px;letter-spacing:0;color:var(--muted)}
.gm-real{columns:auto;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(22px,2.4vw,34px) clamp(14px,1.6vw,22px);margin-bottom:clamp(40px,5vw,72px)}
.gm-real .gt{margin:0}
.gm-real .gt .gt-img{aspect-ratio:4/3}
@media (max-width:1100px){.gm-real{grid-template-columns:repeat(2,minmax(0,1fr));row-gap:22px}}
.gl-note{margin:clamp(10px,2vw,24px) 0 0;max-width:70ch;font-size:14.5px;line-height:1.6;color:var(--muted)}

/* photo viewer */
.lb{width:100vw;max-width:100vw;height:100svh;max-height:100svh;margin:0;padding:0;border:0;background:#09090B;color:#fff;overflow:hidden}
.lb::backdrop{background:#09090B}
.lb[open]{display:grid;grid-template-rows:minmax(0,1fr) auto;animation:lbIn .45s ease}
@keyframes lbIn{from{opacity:0}to{opacity:1}}
.lb-stage{position:relative;display:grid;grid-template:minmax(0,1fr)/minmax(0,1fr);place-items:center;padding:clamp(56px,7vh,80px) clamp(16px,6vw,110px) 12px;min-height:0;touch-action:pan-y}
.lb-stage img{max-width:100%;max-height:100%;object-fit:contain;border-radius:12px;transition:opacity .3s ease,transform .45s cubic-bezier(.2,.7,.2,1)}
.lb.swap .lb-stage img,.lb.swap .lb-ph{opacity:0;transform:scale(.98)}
.lb-ph{display:none;flex-direction:column;align-items:center;justify-content:center;gap:16px;width:min(720px,100%);aspect-ratio:4/3;border-radius:16px;background:radial-gradient(90% 80% at 50% 40%,#1C1C22 0%,#0D0D10 75%);border:1px solid rgba(255,255,255,.08);transition:opacity .3s ease,transform .45s}
.lb-ph .gt-ico{width:80px;height:80px}
.lb.is-ph .lb-ph{display:flex}
.lb.is-ph .lb-stage img,.lb.is-ph #lbSample,.lb.is-real #lbSample{display:none}
#lbSample{top:auto;bottom:24px;left:50%;right:auto;transform:translateX(-50%)}
.lb-bar{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:16px clamp(16px,6vw,110px) clamp(18px,3vh,30px)}
.lb-cap span{font:500 11.5px var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--sun)}
.lb-cap h2{margin:6px 0 0;font-size:clamp(18px,1.6vw,24px);font-weight:400;letter-spacing:-0.02em;color:#fff}
.lb-nav{display:flex;align-items:center;gap:12px}
.lb-arrow,.lb-close{display:grid;place-items:center;width:48px;height:48px;border:1px solid rgba(255,255,255,.25);border-radius:50%;background:rgba(255,255,255,.06);color:#fff;cursor:pointer;transition:background .3s,border-color .3s,color .3s}
.lb-arrow:hover,.lb-close:hover{background:var(--sun);border-color:var(--sun);color:var(--ink)}
.lb-arrow svg{width:18px;height:18px}.lb-close svg{width:20px;height:20px}
.lb-close{position:absolute;right:clamp(14px,2vw,28px);top:clamp(14px,2vw,24px);z-index:2}
.lb-arrow:focus-visible,.lb-close:focus-visible{outline:2px solid #fff;outline-offset:3px;box-shadow:0 0 0 3px var(--sun)}
.lb-count{min-width:64px;text-align:center;font:500 12px var(--f-mono);letter-spacing:.06em;color:rgba(255,255,255,.75)}

@media (max-width:1100px){.gcats{grid-template-columns:repeat(2,minmax(0,1fr))}.gm{columns:2}}
@media (max-width:640px){
  .gcats{display:none}
  .pf-bar{flex-wrap:nowrap;overflow-x:auto;margin-inline:-16px;padding:0 16px 4px;scrollbar-width:none}
  .pf-bar::-webkit-scrollbar{display:none}
  .pf{flex:0 0 auto}
  .gm{columns:2;column-gap:12px}
  .gt{margin-bottom:18px}
  .gt-cap{font-size:13.5px}
  .gt-cap span{display:none}
  .gt-ico{width:40px;height:40px}
  .gt-tba{font-size:9.5px;letter-spacing:.06em}
  .lb-bar{flex-direction:column;align-items:flex-start;gap:14px}
  .lb-nav{align-self:stretch;justify-content:space-between}
}
@media (prefers-reduced-motion: reduce){
  .gt-img{clip-path:inset(0 0 0 0 round 18px)!important;transition:none}
  .gt-img img{transform:none!important;transition:none}
  .lb[open]{animation:none}
  .lb-stage img,.lb-ph{transition:none}
}
'''
head = head[:head.rindex('</style>')] + CSS + head[head.rindex('</style>'):]

JS = r'''/* ---------- Highlights: the current photo slides left and the next one slides in from the right ----------
   One render(p) draws every card for a progress p from 0 to n-1. On desktop p follows the scroll (the inner part is sticky);
   on phones, with the arrows or a swipe, p eases to the next whole number. With reduced motion the photos simply cross-fade. */
(function(){
  const sec = document.getElementById('gl-hero'), deck = document.getElementById('ghDeck'); if (!sec || !deck) return;
  requestAnimationFrame(() => setTimeout(() => sec.classList.add('in'), 60));
  deck.querySelectorAll('img[data-g]').forEach(im => { const src = document.querySelector('.gm img[data-g="' + im.dataset.g + '"]'); if (src) im.src = src.getAttribute('src'); });
  const H = HIGHLIGHTS, n = H.length, cards = [...deck.querySelectorAll('.hc')], segs = [...sec.querySelectorAll('.gh-segs i')];
  const $ = id => document.getElementById(id), cap = $('ghCap');
  const smooth = t => t * t * (3 - 2 * t);
  let p = 0, shown = -1, tween = null;
  const caption = k => {
    if (k === shown) return; const first = shown < 0; shown = k;
    const put = () => { $('ghNum').textContent = String(k + 1).padStart(2, '0'); $('ghKind').textContent = H[k].kind; $('ghTitle').textContent = H[k].name; $('ghLine').textContent = H[k].line; cap.classList.remove('swap'); };
    if (first || reduce) put(); else { cap.classList.add('swap'); setTimeout(put, 180); }
    $('ghLive').textContent = first ? '' : 'Highlight ' + (k + 1) + ' of ' + n + ': ' + H[k].name + ', ' + H[k].kind;
    $('ghPrev').disabled = k === 0; $('ghNext').disabled = k === n - 1;
  };
  const render = v => {
    p = Math.max(0, Math.min(n - 1, v));
    cards.forEach((c, i) => {
      const o = i - p, a = Math.abs(o), f = c.querySelector('.hc-shade');     // o > 0: still to come (waits on the right); o < 0: already seen
      c.style.zIndex = String(100 - Math.round(a * 10));
      if (reduce){ c.style.transform = 'none'; c.style.opacity = String(Math.max(0, 1 - a)); c.style.visibility = a >= 1 ? 'hidden' : ''; return; }
      const gone = o < 0 ? a >= .95 : a >= 1.9;
      c.style.visibility = gone ? 'hidden' : '';
      if (gone) return;
      const x = o * 66, sc = 1 - .14 * Math.min(a, 1.4), rot = o * 1.5;
      c.style.transform = `translate3d(${x}%, 0, 0) rotate(${rot}deg) scale(${sc})`;
      c.style.opacity = o < 0 ? String(Math.max(0, 1 - a * 1.15)) : String(a <= 1 ? 1 : Math.max(0, 1 - (a - 1) * 1.1));
      if (f) f.style.opacity = String(Math.min(.62, a * .55));
    });
    segs.forEach((s, i) => s.style.setProperty('--f', Math.max(0, Math.min(1, p - i + 1)).toFixed(3)));
    caption(Math.min(n - 1, Math.round(p)));
  };
  const desktop = () => innerWidth > 900 && !reduce;
  // desktop: progress follows the scroll through the tall section (a short hold at each end)
  const fromScroll = () => { const r = sec.getBoundingClientRect(), span = r.height - innerHeight; if (span <= 0) return null;
    const t = Math.min(1, Math.max(0, (-r.top) / span)); return Math.min(1, Math.max(0, (t - .04) / .9)) * (n - 1); };
  let queued = false;
  const onScroll = () => { queued = false; if (!desktop() || tween) return; const v = fromScroll(); if (v !== null) render(v); };
  addEventListener('scroll', () => { if (!queued){ queued = true; requestAnimationFrame(onScroll); } }, { passive:true });
  addEventListener('resize', () => { if (desktop()) onScroll(); else render(Math.round(p)); });
  // arrows and swipes: on desktop scroll to that card's spot; elsewhere ease p there
  const easeTo = target => {
    target = Math.max(0, Math.min(n - 1, target));
    if (desktop()){ const span = sec.offsetHeight - innerHeight, y = sec.getBoundingClientRect().top + scrollY + (.04 + .9 * target / (n - 1)) * span;
      if (lenis) lenis.scrollTo(y, { duration: 1.1 }); else scrollTo({ top: y, behavior: 'smooth' }); return; }
    if (reduce){ render(target); return; }
    const from = p, t0 = performance.now(), dur = 900 * Math.max(.6, Math.abs(target - from));
    cancelAnimationFrame(tween); const step = now => { const t = Math.min(1, (now - t0) / dur), e = t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      render(from + (target - from) * e); tween = t < 1 ? requestAnimationFrame(step) : null; };
    tween = requestAnimationFrame(step);
  };
  $('ghPrev').addEventListener('click', () => easeTo(Math.round(p) - 1));
  $('ghNext').addEventListener('click', () => easeTo(Math.round(p) + 1));
  let x0 = null;
  deck.addEventListener('pointerdown', e => { x0 = e.clientX; });
  deck.addEventListener('pointerup', e => { if (x0 !== null && Math.abs(e.clientX - x0) > 40) easeTo(Math.round(p) + (e.clientX < x0 ? 1 : -1)); x0 = null; });
  // the "Skip to all photos" link is handled by the shared smooth-scroll code
  if (desktop()){ const v = fromScroll(); render(v === null ? 0 : v); } else render(0);
})();

/* ---------- Masonry: each tile wipes open as it scrolls into view; filters by category ---------- */
(function(){
  const gm = document.getElementById('gm'); if (!gm) return;
  const tiles = [...document.querySelectorAll('.gm .gt')], btns = [...document.querySelectorAll('.pf')], cats = [...document.querySelectorAll('.gc')], status = document.getElementById('gfStatus');
  if (reduce || !('IntersectionObserver' in window)) tiles.forEach(t => t.classList.add('in'));
  else { const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin:'0px 0px -8% 0px' }); tiles.forEach(t => io.observe(t)); }
  if (!btns.length) return;   // a single category: no filters
  const apply = f => {
    let n = 0;
    btns.forEach(x => { const on = x.dataset.f === f; x.classList.toggle('on', on); x.setAttribute('aria-pressed', String(on)); });
    cats.forEach(c => c.classList.toggle('on', c.dataset.f === f));
    tiles.forEach(t => { const show = f === 'all' || t.dataset.cat === f; t.classList.toggle('out', !show); if (show){ n++; t.classList.add('in'); } });
    status.textContent = 'Showing ' + n + (n === 1 ? ' item' : ' items');
    if (window.ScrollTrigger) ScrollTrigger.refresh();
  };
  btns.forEach(b => b.addEventListener('click', () => apply(b.dataset.f)));
  // category cards filter too, then bring the grid into view
  cats.forEach(c => c.addEventListener('click', e => { e.preventDefault(); e.stopImmediatePropagation(); apply(c.dataset.f);
    history.replaceState(null, '', '#' + c.dataset.f);
    const bar = document.querySelector('.pf-bar'); if (lenis) lenis.scrollTo(bar, { offset:-100, duration:1.2 }); else bar.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });
    setTimeout(() => document.querySelector('.pf.on').focus({ preventScroll:true }), 60); }, true));
  // links such as gallery.html#manufacturing open with that category selected
  const h = location.hash.slice(1); if (cats.some(c => c.dataset.f === h)) { apply(h); setTimeout(() => { const bar = document.querySelector('.pf-bar'); scrollTo(0, bar.getBoundingClientRect().top + scrollY - 100); }, 80); }
})();

/* ---------- Photo viewer: full screen; arrows, arrow keys or a swipe move through the visible items ---------- */
(function(){
  const lb = document.getElementById('lb'); if (!lb || !lb.showModal) return;
  const G = GALLERY, $ = id => document.getElementById(id), opens = [...document.querySelectorAll('.gt-open')];
  let cur = 0;
  const visible = () => opens.map((b, i) => i).filter(i => !opens[i].closest('.gt').classList.contains('out'));
  const fill = k => {
    cur = k; const g = G[k], vis = visible();
    lb.classList.toggle('is-ph', !g.img);
    lb.classList.toggle('is-real', !!g.real);
    if (g.img){ const src = opens[k].querySelector('img').src; $('lbImg').src = src; $('lbImg').alt = (g.real ? '' : 'Sample photo: ') + g.title; }
    else { $('lbImg').removeAttribute('src'); $('lbImg').alt = ''; $('lbIco').innerHTML = opens[k].querySelector('.gt-ico').innerHTML; }
    $('lbCat').textContent = g.cat; $('lbTitle').textContent = g.title + (g.img ? '' : ' (photo to be added)');
    $('lbCount').textContent = String(vis.indexOf(k) + 1).padStart(2, '0') + ' / ' + String(vis.length).padStart(2, '0');
  };
  const go = dir => { const vis = visible(), at = vis.indexOf(cur), k = vis[(at + dir + vis.length) % vis.length];
    if (reduce){ fill(k); return; } lb.classList.add('swap'); setTimeout(() => { fill(k); lb.classList.remove('swap'); }, 200); };
  opens.forEach((b, i) => b.addEventListener('click', () => { fill(i); lb.showModal(); if (lenis) lenis.stop(); $('lbClose').focus(); }));
  $('lbPrev').addEventListener('click', () => go(-1)); $('lbNext').addEventListener('click', () => go(1));
  $('lbClose').addEventListener('click', () => lb.close());
  lb.addEventListener('keydown', e => { if (e.key === 'ArrowRight') go(1); if (e.key === 'ArrowLeft') go(-1); });
  let x0 = null;   // swipe on touch screens
  $('lbStage').addEventListener('pointerdown', e => { x0 = e.clientX; });
  $('lbStage').addEventListener('pointerup', e => { if (x0 !== null && Math.abs(e.clientX - x0) > 50) go(e.clientX < x0 ? 1 : -1); x0 = null; });
  $('lbStage').addEventListener('click', e => { if (e.target === $('lbStage')) lb.close(); });
  lb.addEventListener('close', () => { if (lenis) lenis.start(); opens[cur].focus(); });
})();

/* ---------- Closing card ---------- */
(function(){
  const c = document.querySelector('.ab-cta-card'); if (!c) return;
  if (reduce || !('IntersectionObserver' in window)) { c.classList.add('in'); return; }
  const io = new IntersectionObserver(es => { if (es[0].isIntersecting){ c.classList.add('in'); io.disconnect(); } }, { rootMargin:'0px 0px -15% 0px' }); io.observe(c);
})();

'''
script = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>\n'
          '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>\n'
          '<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>\n<script>\n'
          + 'const GALLERY = ' + DATA + ';\nconst HIGHLIGHTS = ' + HL_DATA + ';\n' + js_core + js_nav + JS + '})();\n</script>\n')
src = (head + body + script).replace('index.html#contact', 'contact.html')   # the Contact page now exists
open(d + 'gallery_src.html', 'w').write(src)

mime = {'png':'image/png','jpg':'image/jpeg','webp':'image/webp'}
import sys; sys.path.insert(0, d); from webp_cache import webp   # all images as WebP
def uri(path): path = webp(path); return 'data:' + mime[path.rsplit('.',1)[1]] + ';base64,' + base64.b64encode(open(path,'rb').read()).decode()
out = re.sub(r'\{\{L:([^}]+)\}\}', lambda m: uri(d + 'layers/' + m.group(1)), src)
out = out.replace('{{LOGO_BLACK}}', uri(d + 'logo_black.png')).replace('{{LOGO_WHITE}}', uri(d + 'logo_white.png'))
assert '{{' not in out, re.findall(r'\{\{[^}]+\}\}', out)[:3]
hi = out.index('<!-- ======= NAV ======= -->')
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
       + out[:hi] + '</head>\n<body>\n' + out[hi:] + '</body>\n</html>\n')
open(d + 'gallery.html', 'w').write(doc)
print('gallery.html', len(doc) // 1024, 'KB')
