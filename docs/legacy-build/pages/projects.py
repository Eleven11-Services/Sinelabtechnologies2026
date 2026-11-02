# Projects page: four real projects with Sinelab's own drone photos (29 Oct). Capacities to be added once confirmed.
# Shares the homepage stylesheet, nav, footer and scripts (lifted from src_draft.html) and the About page hero / closing card
# styles (lifted from about.py). Adds: a filterable project grid, a case-study dialog (native <dialog>), and a capacity chart.
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
LINKS = [('#gallery', 'index.html#gallery'), ('#team', 'index.html#team'), ('#contact', 'index.html#contact'), ('#blog', 'index.html#blog'), ('#top', 'index.html')]
def relink(html):
    for a, b in LINKS: html = html.replace(f'href="{a}"', f'href="{b}"')
    return html

# ---------- shared pieces ----------
head = home[:home.index('<!-- ======= NAV ======= -->')]
head = head.replace('<title>Sinelab Website</title>', '<title>Projects | Sinelab Technologies</title>')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Rooftop solar projects by Sinelab Technologies for Bava Metals, Grand Bajaj Showroom, Bala Cinemas, Jamal Sons, Palakkad Surgicals, Sinicon and Salim Hybrid Residence.">', head)
nav = relink(cut('<!-- ======= NAV ======= -->', '<main id="top">'))
nav = rp(nav, '<a href="projects.html">Projects</a>', '<a href="projects.html" aria-current="page">Projects</a>')
nav = rp(nav, '<a href="projects.html" style="--i:2">Projects', '<a href="projects.html" style="--i:2" aria-current="page">Projects')
foot = relink(home[home.index('<footer'):home.index('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js">')])

js_core = cut('(function(){\nconst reduce', '/* ---------- Solar panel model')
js_nav = cut('/* ---------- Floating glass nav: compact', '/* ---------- Why Sinelab: the reason nearest')
js_nav = rp(js_nav, "['#anatomy','#films','#savings','#faq','footer']", "['#pj-hero','footer']")
js_nav = rp(js_nav, "['#why','#solutions','#projects','#gallery','#faq','#blog','#contact']", "['#work']")

# ---------- content: real projects, Sinelab's own drone photos ----------
# id, name, sector, card photo, focus (object-position), type, status, summary, note(title, text) or None, alt text
P = [
  ('bava-metals', 'Bava Metals', 'Commercial building', 'real_bava_card.jpg', '55% 50%', 'Rooftop solar', None,
   'Rooftop solar for Bava Metals, with the panels set along the building’s metal roofs on a busy town street.', None,
   'Drone view of the Bava Metals building, with solar panels along its metal roofs'),
  ('grand-bajaj', 'Grand Bajaj Showroom', 'Vehicle showroom', 'real_bajaj_card.jpg', '50% 45%', 'Rooftop solar', None,
   'Rooftop solar above the Grand Bajaj showroom. The panels stand on a raised steel frame over the flat terrace.', None,
   'Solar panels on a raised steel frame above the Grand Bajaj showroom, with the Bajaj and Chetak signs below'),
  ('bala-cinemas', 'Bala Cinemas', 'Cinema', 'real_bala_card.jpg', '50% 50%', 'Rooftop solar', 'Completed',
   'A completed rooftop installation incorporating Enphase microinverters to address site-specific shading conditions on a challenging roof.',
   ('Shading on a challenging roof', 'Enphase microinverters let each panel work on its own, so shade on one part of the roof doesn’t pull down the rest.'),
   'Drone view of the Bala Cinemas building with a solar array on its roof'),
  ('jamal-sons', 'Jamal Sons', 'Commercial building', 'real_jamal_card.jpg', '50% 50%', 'Rooftop solar', None,
   'Rooftop solar for the Jamal Sons building, on a main road lined with shops.', None,
   'Drone view of the Jamal Sons building on a main road, with solar panels on its roof'),
  ('palakkad-surgicals', 'Palakkad Surgicals', 'Manufacturing', 'real_psurg_card.jpg', '50% 50%', 'Rooftop solar', None,
   'Rooftop solar for Palakkad Surgical Industries, with the panels on the roof of the block beside the main building.', None,
   'Drone view of the Palakkad Surgical Industries building, with solar panels on the roof of the smaller block'),
  ('sinicon', 'Sinicon', 'Industrial', 'real_sinicon_card.jpg', '50% 50%', 'Rooftop solar', None,
   'Rooftop solar across the Sinicon factory: rows of panels on the sloped metal roof and more on the flat roof beside it.', None,
   'Drone view of the Sinicon factory, with rows of solar panels on its roofs'),
  ('salim-residence', 'Salim Hybrid Residence', 'Residential', 'real_salim_card.jpg', '50% 50%', 'Hybrid solar', None,
   'A residential hybrid solar solution combining clean generation with battery-backed functionality, designed around the household’s energy needs.', None,
   'Top-down drone view of the Salim residence, with solar panels on two of its flat roofs'),
]
def card(k, p):
    pid, name, sector, img, focus, typ, status, summ, note, alt = p
    st = f'<span class="pc-st">{status}</span>' if status else ''
    return f'''        <li class="pcard{" shift" if k % 2 else ""}" id="{pid}" style="--k:{k}">
          <button type="button" class="pc-open" data-k="{k}" aria-haspopup="dialog" aria-label="{name}, {sector.lower()}, {typ.lower()}{", " + status.lower() if status else ""}. View project">
            <span class="pc-img"><img src="{{{{L:{img}}}}}" alt="" loading="lazy" style="object-position:{focus}"><span class="pc-view" aria-hidden="true">View project {ARR}</span></span>
            <span class="pc-body">
              <span class="pc-top"><span class="pc-n">{k + 1:02d}</span><span class="pc-type">{sector}</span>{st}</span>
              <span class="pc-row"><span class="pc-name">{name}</span><span class="pc-go" aria-hidden="true">{ARR}</span></span>
            </span>
          </button>
        </li>'''
cards = '\n'.join(card(k, p) for k, p in enumerate(P))

DATA = json.dumps([{'id': p[0], 'name': p[1], 'sector': p[2], 'focus': p[4], 'type': p[5], 'status': p[6], 'summary': p[7],
                    'note': p[8], 'alt': p[9]} for p in P], ensure_ascii=False)

CLOSE = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M5 5l10 10M15 5L5 15"/></svg>'
PREV = '<svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M14 9H4M8 5L4 9l4 4"/></svg>'
NEXT = '<svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 9h10M10 5l4 4-4 4"/></svg>'

body = f'''{nav}
<main id="top">

<!-- ======= PROJECTS HERO ======= -->
<section class="ab-hero pj-hero" id="pj-hero" aria-labelledby="pjTitle">
  <div class="ab-hero-bg" aria-hidden="true"><img class="ab-hero-img" src="{{{{L:real_bala_hero.jpg}}}}" alt=""></div>
  <div class="wrap ab-hero-copy">
    <nav class="ab-crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">Projects</span></nav>
    <h1 class="ab-h1" id="pjTitle"><span class="ln"><span>Projects that</span></span><span class="ln"><span><em>power progress.</em></span></span></h1>
    <p class="ab-since"><span>Factories</span><span>Showrooms</span><span>Homes</span></p>
  </div>
  <div class="ab-cue" aria-hidden="true"><span>Scroll</span><i></i></div>
</section>

<!-- ======= THE WORK: filter + grid ======= -->
<section class="pj-work band" id="work" aria-labelledby="workTitle">
  <div class="wrap">
    <div class="sec-head">
      <div><div class="eyebrow">Featured projects</div><h2 id="workTitle">Rooftops we have <em>put to work</em></h2></div>
      <p>Solar Sinelab has built for businesses, factories and homes, photographed from the air. Choose a project to see it up close.</p>
    </div>
    <ul class="pgrid" id="pgrid">
{cards}
    </ul>
  </div>
</section>

<!-- ======= CALL TO ACTION ======= -->
<section class="ab-cta" id="cta">
  <div class="wrap">
    <div class="ab-cta-card">
      <div class="ab-cta-img" aria-hidden="true"><img src="{{{{L:cta_night.jpg}}}}" alt=""></div>
      <div class="ab-cta-copy">
        <span class="ab-cta-k">Planning a project?</span>
        <h2>Let’s build <em>your next one</em></h2>
        <p>From a family home to a commercial rooftop, tell us what you have in mind and our team will take it from there.</p>
        <div class="ab-cta-btns">
          <a class="btn btn-sun" href="index.html#contact">Get a free quote {ARR}</a>
          <a class="btn ab-btn-ghost" href="tel:+919946207738">Call +91 99462 07738</a>
        </div>
      </div>
      <dl class="ab-cta-meta">
        <div><dt>Email</dt><dd><a href="mailto:info@sinelabtechnologies.com">info@sinelabtechnologies.com</a></dd></div>
        <div><dt>Offices</dt><dd>Palakkad · Kochi, Kerala</dd></div>
        <div><dt>Since</dt><dd>1996</dd></div>
      </dl>
    </div>
  </div>
</section>

</main>

<!-- ======= CASE STUDY DIALOG ======= -->
<dialog class="pd" id="pd" aria-labelledby="pdName" data-lenis-prevent>
  <div class="pd-in">
    <button type="button" class="pd-close" id="pdClose" aria-label="Close project">{CLOSE}</button>
    <div class="pd-img"><img id="pdImg" src="" alt=""></div>
    <div class="pd-body">
      <div class="pd-top"><span class="pd-type" id="pdType"></span><span class="pc-st" id="pdStatus"></span></div>
      <h2 id="pdName"></h2>
      <dl class="pd-spec">
        <div><dt>Type</dt><dd id="pdType2"></dd></div>
        <div><dt>Sector</dt><dd id="pdSector"></dd></div>
      </dl>
      <p class="pd-sum" id="pdSum"></p>
      <div class="pd-note" id="pdNote"><span class="pd-note-k">Project note</span><h3 id="pdNoteT"></h3><p id="pdNoteP"></p></div>
      <div class="pd-foot">
        <a class="btn btn-sun" href="index.html#contact">Discuss a similar project {ARR}</a>
        <div class="pd-nav">
          <button type="button" class="pd-arrow" id="pdPrev" aria-label="Previous project">{PREV}</button>
          <span class="pd-count" id="pdCount" aria-hidden="true"></span>
          <button type="button" class="pd-arrow" id="pdNext" aria-label="Next project">{NEXT}</button>
        </div>
      </div>
    </div>
  </div>
</dialog>

{foot}'''

CSS = ABOUT_CSS + '''
/* ================= Projects page ================= */
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.pj-work{position:relative;isolation:isolate;overflow:clip;padding-block:clamp(90px,11vw,160px) clamp(70px,8vw,120px)}
.pf-bar{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:clamp(28px,3vw,44px)}
.pf{display:inline-flex;align-items:center;gap:10px;min-height:44px;padding:0 10px 0 18px;border:1px solid var(--line);border-radius:999px;background:#fff;font:inherit;font-size:15px;color:var(--ink);cursor:pointer;transition:background .3s,border-color .3s,color .3s}
.pf span{display:grid;place-items:center;min-width:26px;height:26px;padding:0 6px;border-radius:999px;background:var(--paper);font:500 12px var(--f-mono);color:var(--ink);transition:background .3s}
.pf:hover{border-color:var(--ink)}
.pf.on{background:var(--navy-deep);border-color:var(--navy-deep);color:#fff}
.pf.on span{background:var(--sun);color:var(--ink)}
.pf:focus-visible{outline:2px solid var(--ink);outline-offset:3px;box-shadow:0 0 0 3px var(--sun)}

/* staggered two-column layout: big photos, a quiet caption, every second card sits lower */
.pgrid{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:clamp(36px,6vw,110px);row-gap:clamp(56px,6vw,96px);align-items:start}
.pcard{--sh:0px;opacity:0;transform:translateY(calc(var(--sh) + 30px));transition:opacity .8s ease calc(var(--k) * 80ms),transform 1s cubic-bezier(.2,.7,.2,1) calc(var(--k) * 80ms)}
.pcard.shift{--sh:clamp(70px,9vw,150px)}
.pgrid.in .pcard{opacity:1;transform:translateY(var(--sh))}
.pgrid{padding-bottom:clamp(70px,9vw,150px)}
.pcard.out{display:none}
.pcard.pop{animation:pcPop .7s cubic-bezier(.2,.7,.2,1) both}
@keyframes pcPop{from{opacity:0;transform:translateY(calc(var(--sh) + 20px))}to{opacity:1;transform:translateY(var(--sh))}}
.pc-open{display:block;width:100%;padding:0;border:0;border-radius:22px;background:none;font:inherit;color:inherit;text-align:left;cursor:pointer}
.pc-open:focus-visible{outline:2px solid var(--ink);outline-offset:6px;box-shadow:0 0 0 6px #fff,0 0 0 9px var(--sun)}
.pc-img{position:relative;display:block;aspect-ratio:5/4;border-radius:22px;overflow:hidden;background:var(--paper);isolation:isolate}
.pc-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:scale(1.02);transition:transform 1.4s cubic-bezier(.2,.7,.2,1)}
.pc-img::after{content:"";position:absolute;inset:0;background:rgba(9,9,11,.18);opacity:0;transition:opacity .5s}
.pc-open:hover .pc-img img,.pc-open:focus-visible .pc-img img{transform:scale(1.07)}
.pc-open:hover .pc-img::after,.pc-open:focus-visible .pc-img::after{opacity:1}
.pc-img .hl-ph{top:auto;bottom:14px;right:14px;z-index:1}
.pc-view{position:absolute;left:50%;top:50%;z-index:1;display:inline-flex;align-items:center;gap:10px;padding:14px 22px;border-radius:999px;background:var(--sun);color:var(--ink);font-size:15px;font-weight:500;white-space:nowrap;opacity:0;transform:translate(-50%,-50%) scale(.85);transition:opacity .4s,transform .6s cubic-bezier(.2,.7,.2,1)}
.pc-view svg{width:16px;height:16px}
.pc-open:hover .pc-view,.pc-open:focus-visible .pc-view{opacity:1;transform:translate(-50%,-50%) scale(1)}
.pc-body{display:block;padding:22px 2px 0}
.pc-top{display:flex;flex-wrap:wrap;align-items:center;gap:10px}
.pc-n{font:500 12px var(--f-mono);letter-spacing:.08em;color:var(--accent-ink)}
.pc-type{font:500 11.5px var(--f-mono);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.pc-st{padding:4px 10px;border-radius:999px;background:var(--paper);font:500 11.5px var(--f-mono);letter-spacing:.02em;color:var(--ink)}
.pc-st:empty{display:none}
.pc-st.pend{background:#FFF4D4}
.pc-row{position:relative;display:flex;align-items:baseline;justify-content:space-between;gap:20px;margin-top:12px;padding-bottom:18px;border-bottom:1px solid var(--line)}
.pc-row::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--sun);transform:scaleX(0);transform-origin:0 50%;transition:transform .7s cubic-bezier(.2,.7,.2,1)}
.pc-open:hover .pc-row::after,.pc-open:focus-visible .pc-row::after{transform:scaleX(1)}
.pc-name{font-size:clamp(26px,2.4vw,36px);font-weight:300;letter-spacing:-0.035em;line-height:1.1;color:var(--ink)}
.pc-go{flex:none;display:grid;place-items:center;width:46px;height:46px;border:1px solid var(--line);border-radius:50%;color:var(--ink);transition:background .4s,border-color .4s,transform .6s cubic-bezier(.2,.7,.2,1)}
.pc-go svg{width:18px;height:18px}
.pc-open:hover .pc-go,.pc-open:focus-visible .pc-go{background:var(--sun);border-color:var(--sun);transform:rotate(-45deg)}
.pc-row{align-items:center}
.pc-cap{flex:none;font:300 clamp(26px,2.4vw,36px)/1 var(--f-display);letter-spacing:-0.04em;color:var(--ink);white-space:nowrap}
.pc-cap small{margin-left:5px;font-size:.45em;letter-spacing:0;color:var(--muted)}
.pc-cap small:only-child{margin-left:0;font:500 12px var(--f-mono);letter-spacing:.04em}

.pj-scale{background:var(--paper);padding-block:clamp(90px,11vw,150px)}
.sc{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.sc li{display:grid;grid-template-columns:minmax(150px,240px) minmax(0,1fr) 90px;align-items:center;gap:20px;padding:14px 0;border-top:1px solid var(--line)}
.sc li:last-child{border-bottom:1px solid var(--line)}
.sc-name{font-size:17px;color:var(--ink)}
.sc-bar{position:relative;height:14px;border-radius:999px;background:#E4E4E7;overflow:hidden}
.sc-bar i{position:absolute;inset:0;width:max(calc(var(--w) * 100%), 10px);border-radius:inherit;background:linear-gradient(90deg,#F9C22E,#FFD866);transform:scaleX(0);transform-origin:0 50%;transition:transform 1.4s cubic-bezier(.2,.7,.2,1) calc(var(--k) * 110ms)}
.sc.in .sc-bar i{transform:scaleX(1)}
.sc-val{font:300 24px/1 var(--f-display);letter-spacing:-0.03em;text-align:right;color:var(--ink)}
.sc-note{margin:18px 0 0;font-size:14.5px;color:var(--muted)}

/* case study dialog */
.pd{width:min(1120px,calc(100vw - 32px));max-height:calc(100svh - 48px);padding:0;border:0;border-radius:24px;background:#fff;color:var(--ink);overflow:hidden;box-shadow:0 40px 120px -30px rgba(9,9,11,.55)}
.pd::backdrop{background:rgba(9,9,11,.62);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.pd[open]{animation:pdIn .55s cubic-bezier(.2,.7,.2,1)}
.pd[open]::backdrop{animation:pdFade .4s ease}
@keyframes pdIn{from{opacity:0;transform:translateY(24px) scale(.98)}to{opacity:1;transform:none}}
@keyframes pdFade{from{opacity:0}to{opacity:1}}
.pd-in{position:relative;display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);min-height:min(620px,calc(100svh - 48px));max-height:calc(100svh - 48px)}
.pd-img{position:relative;min-height:520px;background:var(--paper)}
.pd-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.pd-img{min-height:clamp(420px,62svh,620px)}
.pd-img .hl-ph{top:auto;bottom:14px;left:14px;right:auto}
.pd-body{display:flex;flex-direction:column;padding:clamp(28px,3.4vw,48px);overflow-y:auto}
.pd-top{display:flex;flex-wrap:wrap;align-items:center;gap:10px;padding-right:44px}
.pd-type{font:500 12px var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--accent-ink)}
.pd-top .pc-st{background:var(--paper)}
.pd h2{margin:14px 0 0;font-size:clamp(30px,3vw,44px);font-weight:300;letter-spacing:-0.04em;line-height:1.08;color:var(--ink)}
.pd-spec{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:24px 0 0;padding:18px 0;border-block:1px solid var(--line)}
.pd-spec dt{font:500 11px var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.pd-spec dd{margin:6px 0 0;font-size:17px;color:var(--ink)}
.pd-sum{margin:22px 0 0;font-size:17px;line-height:1.65;color:var(--muted)}
.pd-note{margin-top:22px;padding:18px 20px;border-radius:16px;background:var(--paper);border-left:3px solid var(--sun)}
.pd-note-k{font:500 11px var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--accent-ink)}
.pd-note h3{margin:8px 0 0;font-size:19px;font-weight:500;letter-spacing:-0.015em;color:var(--ink)}
.pd-note p{margin:6px 0 0;font-size:15.5px;line-height:1.6;color:var(--muted)}
.pd-foot{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px;margin-top:auto;padding-top:28px}
.pd-nav{display:flex;align-items:center;gap:10px}
.pd-arrow{display:grid;place-items:center;width:44px;height:44px;border:1px solid var(--line);border-radius:50%;background:#fff;color:var(--ink);cursor:pointer;transition:background .3s,border-color .3s}
.pd-arrow:hover{background:var(--navy-deep);border-color:var(--navy-deep);color:#fff}
.pd-arrow svg{width:18px;height:18px}
.pd-arrow:focus-visible,.pd-close:focus-visible{outline:2px solid var(--ink);outline-offset:3px;box-shadow:0 0 0 3px var(--sun)}
.pd-count{font:500 12px var(--f-mono);letter-spacing:.06em;color:var(--muted)}
.pd-close{position:absolute;right:16px;top:16px;z-index:2;display:grid;place-items:center;width:44px;height:44px;border:0;border-radius:50%;background:rgba(255,255,255,.92);color:var(--ink);cursor:pointer;box-shadow:0 4px 16px rgba(9,9,11,.15)}
.pd-close svg{width:20px;height:20px}
.pd-body > *{transition:opacity .35s ease}
.pd.swap .pd-body > *,.pd.swap .pd-img img{opacity:0}
.pd-img img{transition:opacity .35s ease}

@media (max-width:1100px){
}
@media (max-width:820px){
  .pd{width:100vw;max-width:100vw;height:100svh;max-height:100svh;margin:0;border-radius:0}
  .pd-in{grid-template-columns:1fr;grid-template-rows:max-content auto;align-content:start;min-height:0;max-height:100svh;height:100svh;overflow-y:auto}
  .pd-close{position:fixed;right:14px;top:14px}
  .pd-img{min-height:0;aspect-ratio:16/10}
  .pd-body{overflow:visible}
  .sc li{grid-template-columns:minmax(0,1fr) auto;row-gap:10px}
  .sc-bar{grid-column:1/-1;grid-row:2}
}
@media (max-width:640px){
  .pgrid{grid-template-columns:1fr;padding-bottom:0}
  .pcard.shift{--sh:0px}
  /* phones (user: "make it mobile friendly"): every filter visible at once – All on top, then two per row */
  .pf-bar{display:grid;grid-template-columns:1fr 1fr;gap:8px}
  .pf{justify-content:space-between;min-height:48px;padding:6px 8px 6px 14px;border-radius:14px;font-size:14.5px;line-height:1.25;text-align:left}
  .pf[data-f="all"]{grid-column:1/-1}
}
@media (prefers-reduced-motion: reduce){
  .pc-img img,.sc-bar i,.pd-body > *,.pd-img img,.pc-go{transition:none!important;transform:none!important;opacity:1}
  .pcard{transition:none!important;opacity:1;transform:translateY(var(--sh))!important}   /* the stagger is layout, not motion */
  .pd[open],.pd[open]::backdrop,.pcard.pop{animation:none}
}
'''
head = head[:head.rindex('</style>')] + CSS + head[head.rindex('</style>'):]

JS = r'''/* ---------- Hero: the two headline lines rise in one after the other on load ---------- */
(function(){ const h = document.getElementById('pj-hero'); if (!h) return; requestAnimationFrame(() => setTimeout(() => h.classList.add('in'), 60)); })();

/* ---------- Project grid: cards rise in; the filter shows one kind of project at a time ---------- */
(function(){
  const grid = document.getElementById('pgrid'); if (!grid) return;
  const cards = [...grid.querySelectorAll('.pcard')], btns = [...document.querySelectorAll('.pf')], status = document.getElementById('pfStatus');
  if (reduce || !('IntersectionObserver' in window)) grid.classList.add('in');
  else { const io = new IntersectionObserver(es => { if (es[0].isIntersecting){ grid.classList.add('in'); io.disconnect(); } }, { rootMargin:'0px 0px -12% 0px' }); io.observe(grid); }
  btns.forEach(b => b.addEventListener('click', () => {
    const f = b.dataset.f; let n = 0;
    btns.forEach(x => { const on = x === b; x.classList.toggle('on', on); x.setAttribute('aria-pressed', String(on)); });
    cards.forEach(c => {
      const show = f === 'all' || c.dataset.cats.split(' ').includes(f);
      c.classList.toggle('out', !show); c.classList.remove('pop');
      if (show){ c.classList.toggle('shift', n % 2 === 1); n++; if (!reduce){ void c.offsetWidth; c.classList.add('pop'); } }
    });
    grid.classList.toggle('filtered', f !== 'all');
    status.textContent = 'Showing ' + n + (n === 1 ? ' project' : ' projects');
    if (window.ScrollTrigger) ScrollTrigger.refresh();
  }));
})();

/* ---------- Case study dialog: opens over the page; arrows step through the projects ---------- */
(function(){
  const dlg = document.getElementById('pd'); if (!dlg || !dlg.showModal) return;
  const P = PROJECTS, $ = id => document.getElementById(id);
  let cur = 0, opener = null;
  const fill = k => {
    const p = P[k]; cur = k;
    $('pdImg').src = document.querySelector('#' + p.id + ' .pc-img img').src; $('pdImg').alt = p.alt;
    $('pdType').textContent = p.type; $('pdType2').textContent = p.type;
    $('pdStatus').textContent = p.status || ''; $('pdStatus').classList.toggle('pend', !!(p.status && /pending/i.test(p.status)));
    $('pdName').textContent = p.name; $('pdSector').textContent = p.sector; $('pdImg').style.objectPosition = p.focus;
    $('pdSum').textContent = p.summary;
    $('pdNote').hidden = !p.note; if (p.note){ $('pdNoteT').textContent = p.note[0]; $('pdNoteP').textContent = p.note[1]; }
    $('pdCount').textContent = String(k + 1).padStart(2, '0') + ' / ' + String(P.length).padStart(2, '0');
  };
  const swap = k => {
    if (reduce){ fill(k); return; }
    dlg.classList.add('swap'); setTimeout(() => { fill(k); dlg.querySelector('.pd-in').scrollTop = 0; dlg.classList.remove('swap'); }, 220);
  };
  document.querySelectorAll('.pc-open').forEach(b => b.addEventListener('click', () => {
    opener = b; fill(+b.dataset.k); dlg.showModal(); if (lenis) lenis.stop(); dlg.querySelector('.pd-in').scrollTop = 0;
    $('pdClose').focus();
  }));
  const step = dir => { const vis = P.map((p, i) => i).filter(i => !document.getElementById(P[i].id).classList.contains('out'));
    const at = vis.indexOf(cur); swap(vis[(at + dir + vis.length) % vis.length]); };
  $('pdPrev').addEventListener('click', () => step(-1));
  $('pdNext').addEventListener('click', () => step(1));
  dlg.addEventListener('keydown', e => { if (e.key === 'ArrowRight' && !e.target.closest('a')) step(1); if (e.key === 'ArrowLeft' && !e.target.closest('a')) step(-1); });
  $('pdClose').addEventListener('click', () => dlg.close());
  dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });      // click on the dimmed backdrop
  dlg.addEventListener('close', () => { if (lenis) lenis.start(); const card = document.getElementById(P[cur].id).querySelector('.pc-open'); (card.offsetParent ? card : opener || card).focus({ preventScroll:false }); });
})();

/* ---------- Capacity chart: bars grow when it comes into view ---------- */
(function(){
  const c = document.getElementById('scChart'); if (!c) return;
  if (reduce || !('IntersectionObserver' in window)) { c.classList.add('in'); return; }
  const io = new IntersectionObserver(es => { if (es[0].isIntersecting){ c.classList.add('in'); io.disconnect(); } }, { rootMargin:'0px 0px -20% 0px' }); io.observe(c);
})();

/* ---------- Closing card: the night photo settles in when it comes into view ---------- */
(function(){
  const c = document.querySelector('.ab-cta-card'); if (!c) return;
  if (reduce || !('IntersectionObserver' in window)) { c.classList.add('in'); return; }
  const io = new IntersectionObserver(es => { if (es[0].isIntersecting){ c.classList.add('in'); io.disconnect(); } }, { rootMargin:'0px 0px -15% 0px' }); io.observe(c);
})();

'''
script = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>\n'
          '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>\n'
          '<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>\n<script>\n'
          + 'const PROJECTS = ' + DATA + ';\n' + js_core + js_nav + JS + '})();\n</script>\n')
src = (head + body + script).replace('index.html#contact', 'contact.html')   # the Contact page now exists
open(d + 'projects_src.html', 'w').write(src)

mime = {'png':'image/png','jpg':'image/jpeg','webp':'image/webp'}
import sys; sys.path.insert(0, d); from webp_cache import webp   # all images as WebP
def uri(path): path = webp(path); return 'data:' + mime[path.rsplit('.',1)[1]] + ';base64,' + base64.b64encode(open(path,'rb').read()).decode()
out = re.sub(r'\{\{L:([^}]+)\}\}', lambda m: uri(d + 'layers/' + m.group(1)), src)
out = out.replace('{{LOGO_BLACK}}', uri(d + 'logo_black.png')).replace('{{LOGO_WHITE}}', uri(d + 'logo_white.png'))
assert '{{' not in out, re.findall(r'\{\{[^}]+\}\}', out)[:3]
hi = out.index('<!-- ======= NAV ======= -->')
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
       + out[:hi] + '</head>\n<body>\n' + out[hi:] + '</body>\n</html>\n')
open(d + 'projects.html', 'w').write(doc)
print('projects.html', len(doc) // 1024, 'KB')
