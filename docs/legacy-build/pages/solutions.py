# Solutions page: all eight services on one page.
# Shares the homepage's stylesheet, nav, footer, smooth scroll, menu, glass nav and reveal code (lifted from src_draft.html)
# and the About page's hero and closing-card styles (lifted from about.py). Adds: a sticky illustration plate that changes
# with the service in view (isometric drawings from iso.py), an on-grid / off-grid / hybrid comparison, how we work, FAQs.
import re, base64
from iso import scenes, ISO_CSS
d = '/tmp/claude-0/site/'
home = open(d + 'src_draft.html').read()
about_py = open(d + 'about.py').read()
ABOUT_CSS = about_py[about_py.index("CSS = '''") + 9:about_py.index("'''\nhead = head[:head.rindex")]
def cut(a, b, src=home):
    i = src.index(a); j = src.index(b, i + len(a)); return src[i:j]
def rp(s, a, b):
    assert a in s, a[:80]; return s.replace(a, b)

ARR = '<svg class="arr" width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 9h10M10 5l4 4-4 4"/></svg>'
LINKS = [('#projects', 'index.html#projects'), ('#gallery', 'index.html#gallery'), ('#team', 'index.html#team'), ('#contact', 'index.html#contact'),
         ('#blog', 'index.html#blog'), ('#top', 'index.html')]
def relink(html):
    for a, b in LINKS: html = html.replace(f'href="{a}"', f'href="{b}"')
    return html

# ---------- shared pieces ----------
head = home[:home.index('<!-- ======= NAV ======= -->')]
head = head.replace('<title>Sinelab Website</title>', '<title>Solutions | Sinelab Technologies</title>')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Residential and commercial solar, lithium batteries and inverters, hybrid storage, manufacturing, lighting, energy consultancy and maintenance from Sinelab Technologies, Kerala.">', head)
nav = relink(cut('<!-- ======= NAV ======= -->', '<main id="top">'))
nav = rp(nav, '<a href="solutions.html">Solutions</a>', '<a href="solutions.html" aria-current="page">Solutions</a>')
nav = rp(nav, '<a href="solutions.html" style="--i:1">Solutions', '<a href="solutions.html" style="--i:1" aria-current="page">Solutions')
foot = relink(home[home.index('<footer'):home.index('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js">')])
foot = foot.replace('href="solutions.html#', 'href="#')       # same page now

js_core = cut('(function(){\nconst reduce', '/* ---------- Solar panel model')
js_nav = cut('/* ---------- Floating glass nav: compact', '/* ---------- Why Sinelab: the reason nearest')
js_reveal = cut('/* ---------- Reveal cards ---------- */', '/* ---------- Savings calculator')
js_nav = rp(js_nav, "['#anatomy','#films','#savings','#faq','footer']", "['#sl-hero','#process','footer']")
js_nav = rp(js_nav, "['#why','#solutions','#projects','#gallery','#faq','#blog','#contact']", "['#services']")   # small drifting solar icons, as on the homepage
js_reveal = rp(js_reveal, "'.sol-grid .sol, .team > *, .leader, .t-deck, .post, .why-card'", "'.cmp-wrap, .sl-faq details'")

# ---------- content (from the client's content document) ----------
SV = [
  ('residential', 'Homes', 'Residential Solar',
   'Thoughtfully designed rooftop solar solutions for homes, with guidance on system sizing, eligible government incentives and financing options.',
   ['System sizing from your bills, roof space and future needs', 'Guidance on eligible schemes such as PM Surya Ghar', 'Help with financing options and documentation']),
  ('commercial', 'Businesses', 'Commercial &amp; Industrial Solar',
   'Engineered rooftop and ground-mounted solar power plants that help businesses plan for long-term energy performance.',
   ['Rooftop solar power plants', 'Ground-mounted solar power plants', 'From a single building to megawatt scale']),
  ('storage', 'Storage', 'Lithium Battery &amp; Inverter Solutions',
   'Advanced battery and inverter solutions designed for dependable energy storage and backup applications.',
   ['Lithium battery systems', 'Integrated lithium inverters', 'Made at our Kanjikode facility']),
  ('hybrid', 'Solar + storage', 'Hybrid Solar &amp; Energy Storage',
   'Integrated solar and battery systems designed around energy savings, resilience and selected backup loads.',
   ['Solar and battery designed as one system', 'Backup for selected loads during power cuts', 'Solar first, battery next, then the grid']),
  ('manufacturing', 'In-house', 'Manufacturing',
   'Manufacturing expertise spanning lithium batteries, integrated inverters and industrial lighting, supported by the wider group’s cable manufacturing heritage.',
   ['Lithium batteries', 'Integrated inverters', 'Industrial lighting']),
  ('lighting', 'Lighting', 'Indoor &amp; Outdoor Lighting',
   'Lighting solutions for industrial, commercial and public-infrastructure applications, including high-mast and floodlighting.',
   ['High-mast lighting and floodlighting', 'Industrial and commercial lighting', 'Public spaces across Kerala, our work since 2013']),
  ('consultancy', 'Advisory', 'Energy Consultancy',
   'Practical energy assessments, technical evaluation and system recommendations aligned with each site’s requirements.',
   ['Energy assessments', 'Technical evaluation', 'System recommendations for your site']),
  ('maintenance', 'Support', 'Operations &amp; Maintenance',
   'Inspection, performance support and ongoing maintenance services in line with the agreed scope of work.',
   ['System inspection', 'Performance support', 'Ongoing maintenance and technical assistance']),
]
SC = scenes()
plain = lambda t: t.replace('&amp;', '&')
def unlabel(svg):   # the desktop plate repeats the drawings, so hide its copies from screen readers
    return re.sub(r'role="img" aria-label="[^"]*"', 'aria-hidden="true" focusable="false"', svg)
def uniq(svg, suffix):  # gradient / clip ids must be unique per copy
    for i in ('lgCone', 'lgBeam', 'omClip'): svg = svg.replace(f'id="{i}"', f'id="{i}{suffix}"').replace(f'url(#{i})', f'url(#{i}{suffix})')
    return svg

GO = '<svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 9h10M10 5l4 4-4 4"/></svg>'
# jump tiles: a small dark plate per service with its drawing; they build in a wave when the grid comes into view
# sun path: a quadratic arc from 6 AM to 6 PM above the services heading
SP = ((40, 112), (600, -60), (1160, 112))
def sp_pt(t):
    (a, b), (c, e), (f, g) = SP
    return ((1 - t) ** 2 * a + 2 * (1 - t) * t * c + t * t * f, (1 - t) ** 2 * b + 2 * (1 - t) * t * e + t * t * g)
SP_D = f'M{SP[0][0]} {SP[0][1]} Q{SP[1][0]} {SP[1][1]} {SP[2][0]} {SP[2][1]}'
SUNPATH = (f'<svg viewBox="0 0 1200 140" fill="none" aria-hidden="true" focusable="false"><path class="sp-arc" d="{SP_D}"/>'
           f'<path class="sp-day" id="spDay" d="{SP_D}" pathLength="1"/><g class="sp-ticks">'
           + ''.join(f'<g transform="translate({sp_pt(t)[0]:.1f} {sp_pt(t)[1]:.1f})"><path d="M0 -6V6"/><text y="24" text-anchor="middle">{lbl}</text></g>'
                     for t, lbl in zip((0, .25, .5, .75, 1), ('6 AM', '9 AM', '12 PM', '3 PM', '6 PM')))
           + '</g><g class="sp-sun" id="spSun"><circle class="sp-glow" r="30"/><circle class="sp-core" r="13"/></g></svg>')
def bg(svg, suffix):
    return uniq(unlabel(svg), suffix)
jump = '\n'.join(f'''        <a class="jt" href="#{sid}" style="--j:{k}">
          <span class="jt-art"><span class="sv-scene">{uniq(unlabel(SC[sid]), "j" + str(k))}</span></span>
          <span class="jt-go">{GO}</span>
          <span class="jt-n">{k + 1:02d}</span><span class="jt-name">{name}</span>
        </a>''' for k, (sid, tag, name, desc, inc) in enumerate(SV))
plate = '\n'.join(f'        <div class="sv-scene{" on" if k == 0 else ""}" data-k="{k}">{uniq(unlabel(SC[sid]), "d")}</div>' for k, (sid, *_r) in enumerate(SV))
CHECK = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.5 8.5l3 3 6-7"/></svg>'
arts = '\n'.join(f'''      <article class="sv{" on" if k == 0 else ""}" id="{sid}" data-k="{k}" tabindex="-1" aria-labelledby="sv-{sid}">
        <div class="sv-media"><div class="sv-scene">{uniq(SC[sid], "m")}</div></div>
        <div class="sv-top"><span class="sv-n">{k + 1:02d}</span><span class="sv-tag">{tag}</span></div>
        <h3 id="sv-{sid}">{name}</h3>
        <p>{desc}</p>
        <ul class="sv-inc">
{chr(10).join(f'          <li>{CHECK}{x}</li>' for x in inc)}
        </ul>
        <a class="text-link" href="index.html#contact">Ask about {name} {ARR}</a>
      </article>''' for k, (sid, tag, name, desc, inc) in enumerate(SV))

YES = '<span class="cmp-y"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.5 8.5l3 3 6-7"/></svg>Yes</span>'
NO = '<span class="cmp-n"><i aria-hidden="true"></i>No</span>'
ROWS = [('Connected to the grid', YES, NO, YES),
        ('Battery storage', NO, YES, YES),
        ('Power during a power cut', NO, YES, '<span class="cmp-y"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.5 8.5l3 3 6-7"/></svg>Selected loads</span>'),
        ('Extra solar power', 'Sent to the grid through a net meter', 'Stored in the battery', 'Battery first, then the grid'),
        ('Best for', '<b>Lower bills</b>', '<b>Remote sites, farms and estates</b>', '<b>Savings with backup</b>')]
# explicit table roles keep the table readable by screen readers when phones restyle it as cards
cmp_rows = '\n'.join(f'          <tr role="row"><th scope="row" role="rowheader">{r}</th><td role="cell" data-l="On-grid">{a}</td><td role="cell" data-l="Off-grid">{b}</td><td role="cell" data-l="Hybrid">{c}</td></tr>' for r, a, b, c in ROWS)

# phones (user: "make it easy for mobile, visually"): one card per system instead of the table
CI_GRID = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M12 2 7 22M12 2l5 20M8.5 15h7M9.6 10.5h4.8M5 6h14M10.7 6 12 2l1.3 4"/></svg>'
CI_BATT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="7" width="16" height="10" rx="2"/><path d="M19 10h2v4h-2M11.5 9 9 12.5h4l-2.5 3.5"/></svg>'
CI_PLUG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3v5M15 3v5M6 8h12v3a6 6 0 0 1-12 0zM12 17v4"/></svg>'
CI_SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg>'
CHK = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.5 8.5l3 3 6-7"/></svg>'
DASH = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 8h8"/></svg>'
SYSTEMS = [('On-grid', CI_GRID, ['yes', 'no', 'no'], 'Sent to the grid through a net meter', 'Lower bills'),
           ('Off-grid', CI_BATT, ['no', 'yes', 'yes'], 'Stored in the battery', 'Remote sites, farms and estates'),
           ('Hybrid', CI_SUN, ['yes', 'yes', 'part'], 'Battery first, then the grid', 'Savings with backup')]
FEATS = [('Grid', CI_GRID), ('Battery', CI_BATT), ('Power-cut backup', CI_PLUG)]
def feat(lbl, ic, st):
    word = {'yes': 'Yes', 'no': 'No', 'part': 'Selected loads'}[st]
    return (f'<li class="ccf is-{st}"><span class="ccf-ico">{ic}</span><span class="ccf-l">{lbl}</span>'
            f'<span class="ccf-s">{DASH if st == "no" else CHK}{word}</span></li>')
cmp_cards = '\n'.join(f'''      <article class="cc">
        <div class="cc-head"><span class="cc-ico">{ic}</span><div><h3>{name}</h3><p class="cc-best">Best for {best[0].lower() + best[1:]}</p></div></div>
        <ul class="cc-feats">{"".join(feat(l, fi, st) for (l, fi), st in zip(FEATS, sts))}</ul>
        <p class="cc-extra"><span>Extra solar power</span>{extra}</p>
      </article>''' for name, ic, sts, extra, best in SYSTEMS)

STEPS = [('Assess', 'We review your electricity bills, installation space, electrical requirements and future energy needs.'),
         ('Design', 'We recommend an appropriately sized system, and whether on-grid, off-grid or hybrid suits you.'),
         ('Guide', 'We guide you through eligible government schemes, financing options and documentation.'),
         ('Install', 'Our team installs and commissions your system.'),
         ('Support', 'Inspection, performance support and maintenance, in line with the agreed scope.')]
steps = '\n'.join(f'        <li class="ps-step"><span class="ps-dot" aria-hidden="true"></span><span class="ps-n">{k + 1:02d}</span><h3>{t}</h3><p>{x}</p></li>' for k, (t, x) in enumerate(STEPS))

FAQ_SRC = cut('<!-- ======= FAQ ======= -->', '</section>')
faqs = re.findall(r'<details[^>]*><summary>(.*?)<span class="pm"></span></summary><p>(.*?)</p></details>', FAQ_SRC)
keep = ['How do I know what solar capacity', 'Are government subsidies', 'Does Sinelab provide assistance with solar financing',
        'What is the difference between on-grid', 'Does Sinelab provide maintenance', 'Does Sinelab undertake large']
faqs = [f for f in faqs if any(f[0].startswith(k) for k in keep)]
assert len(faqs) == 6, len(faqs)
faq_html = '\n'.join(f'      <details{" open" if k == 0 else ""}><summary>{q}<span class="pm"></span></summary><p>{a}</p></details>' for k, (q, a) in enumerate(faqs))

body = f'''{nav}
<main id="top">

<!-- ======= SOLUTIONS HERO ======= -->
<section class="ab-hero sl-hero" id="sl-hero" aria-labelledby="slTitle">
  <div class="ab-hero-bg" aria-hidden="true"><img class="ab-hero-img" src="{{{{L:pj_array.jpg}}}}" alt=""></div>
  <span class="hl-ph ab-ph">Sample photo</span>
  <div class="wrap ab-hero-copy">
    <nav class="ab-crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">Solutions</span></nav>
    <h1 class="ab-h1" id="slTitle"><span class="ln"><span>One partner for</span></span><span class="ln"><span><em>every energy need.</em></span></span></h1>
    <p class="ab-since"><span>Homes</span><span>Businesses</span><span>Industries</span></p>
  </div>
  <div class="ab-cue" aria-hidden="true"><span>Scroll</span><i></i></div>
</section>

<!-- ======= SERVICES: sticky illustration + eight services ======= -->
<section class="sl-svc band" id="services" aria-labelledby="svcTitle">
  <div class="bgart sunpath" aria-hidden="true"><div class="wrap">{SUNPATH}</div></div>
  <div class="wrap">
    <div class="sec-head">
      <div><div class="eyebrow">Solutions</div><h2 id="svcTitle">Eight ways we <em>power progress</em></h2></div>
      <p>From a family home to an industrial plant, every solution is shaped around how much power you need and when you need it.</p>
    </div>
    <nav class="sl-jump" aria-label="Jump to a solution">
{jump}
    </nav>
    <div class="sv-wrap">
      <div class="sv-stage" aria-hidden="true">
        <div class="sv-plate" id="svPlate">
{plate}
          <div class="sv-count"><b id="svNum">01</b><span>/ 08</span><i><em id="svBar"></em></i></div>
          <span class="sv-cap">Illustration</span>
        </div>
      </div>
      <div class="sv-list" id="svList">
{arts}
      </div>
    </div>
  </div>
</section>

<!-- ======= ON-GRID / OFF-GRID / HYBRID ======= -->
<section class="sl-cmp band" id="compare" aria-labelledby="cmpTitle">
  <div class="bgart bg-array" aria-hidden="true">{bg(SC['maintenance'], 'b1')}</div>
  <div class="wrap">
    <div class="sec-head">
      <div><div class="eyebrow">Choosing a system</div><h2 id="cmpTitle">On-grid, <span class="nw">off-grid</span> <em>or hybrid?</em></h2></div>
      <p>Three ways to set up solar. Here is how they differ at a glance.</p>
    </div>
    <div class="cmp-wrap" role="region" aria-label="Comparison table" tabindex="0">
      <table class="cmp" role="table">
        <caption class="sr-only">How on-grid, off-grid and hybrid solar systems compare</caption>
        <thead role="rowgroup"><tr role="row"><td role="cell"></td><th scope="col" role="columnheader">On-grid</th><th scope="col" role="columnheader">Off-grid</th><th scope="col" role="columnheader">Hybrid</th></tr></thead>
        <tbody role="rowgroup">
{cmp_rows}
        </tbody>
      </table>
    </div>
    <div class="cmp-cards">
{cmp_cards}
    </div>
    <a class="text-link" href="index.html#anatomy">See how each one works, from midday to after sunset {ARR}</a>
  </div>
</section>

<!-- ======= HOW WE WORK ======= -->
<section class="sl-proc" id="process" aria-labelledby="procTitle">
  <div class="wrap">
    <div class="sec-head">
      <div><div class="eyebrow">How we work</div><h2 id="procTitle">From first call to <em>long-term care</em></h2></div>
      <p>One team from the first site visit to years of support.</p>
    </div>
    <div class="ps-wrap" id="psWrap">
      <span class="ps-line" aria-hidden="true"><i id="psFill"></i></span>
      <ol class="ps">
{steps}
      </ol>
    </div>
  </div>
</section>

<!-- ======= FAQ ======= -->
<section class="sl-faq band" id="sl-faq" aria-labelledby="faqTitle">
  <div class="bgart bg-house" aria-hidden="true">{bg(SC['residential'], 'b2')}</div>
  <div class="wrap faq-grid">
    <div><div class="eyebrow">FAQs</div><h2 id="faqTitle">Questions we <em>hear often</em></h2><p>Can't find your answer? Call or WhatsApp us and an engineer will help.</p></div>
    <div>
{faq_html}
    </div>
  </div>
</section>

<!-- ======= CALL TO ACTION ======= -->
<section class="ab-cta" id="cta">
  <div class="wrap">
    <div class="ab-cta-card">
      <div class="ab-cta-img" aria-hidden="true"><img src="{{{{L:cta_night.jpg}}}}" alt=""></div>
      <div class="ab-cta-copy">
        <span class="ab-cta-k">Not sure where to start?</span>
        <h2>Find the right fit <em>for your site</em></h2>
        <p>Share your electricity bill and what you need. Our team will recommend the right system.</p>
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

{foot}'''

CSS = ABOUT_CSS + ISO_CSS + '''
/* ================= Solutions page ================= */
/* background illustrations (user: "bg illustrations related to solar") */
.sl-svc,.sl-cmp,.sl-faq{position:relative;isolation:isolate;overflow:clip}
.bgart{position:absolute;z-index:-1;pointer-events:none}
.sunpath{left:0;right:0;top:clamp(6px,1vw,14px)}
.sunpath svg{display:block;width:100%;height:auto;overflow:visible}
.sp-arc{stroke:#D4D4D8;stroke-width:1.4;stroke-dasharray:3 9;stroke-linecap:round}
.sp-day{stroke:var(--sun);stroke-width:2;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:.5;opacity:.75}
.sp-ticks path{stroke:#C4C4CA;stroke-width:1.4}
.sp-ticks text{fill:#6E6E78;stroke:none;font:500 12px var(--f-mono);letter-spacing:.08em}
.sp-sun .sp-core{fill:var(--sun)}
.sp-sun .sp-glow{fill:var(--sun);opacity:.18}
.bg-array{right:-4%;bottom:-10%;width:min(640px,50vw);color:#CDCDD3;--bgc:var(--paper)}
.bg-house{left:-4%;bottom:-6%;width:min(520px,38vw);color:#D6D6DB;--bgc:#fff}
.bgart .iso polygon,.bgart .iso path,.bgart .iso ellipse{fill:var(--bgc)!important;stroke:currentColor!important}
.bgart .iso polyline,.bgart .iso .pg,.bgart .iso .lg,.bgart .iso .arm,.bgart .iso .wire,.bgart .iso .sun circle,.bgart .iso .sun path{fill:none!important;stroke:currentColor!important}
.bgart .iso .ac,.bgart .iso .acl,.bgart .iso .acr,.bgart .iso .ww,.bgart .iso .led,.bgart .iso .badge circle{fill:rgba(249,194,46,.45)!important}
.bgart .iso .badge path{stroke:#fff!important}
.bgart .iso .scan,.bgart .iso .beam,.bgart .iso .glow{display:none}
.bgart .iso .fl,.bgart .iso .fg{stroke:rgba(249,194,46,.7)!important}
@media (max-width:1100px){.bg-house{display:none}}
@media (max-width:700px){.sunpath .sp-ticks text{display:none}.bg-array{width:90vw;right:-20%;bottom:-6%}}
.nw{white-space:nowrap}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.sl-svc{padding-block:clamp(90px,12.5vw,184px) clamp(60px,7vw,110px)}   /* room for the sun path */
.sl-jump{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:clamp(8px,1vw,14px)}   /* four on top, four below */
.jt{position:relative;isolation:isolate;overflow:hidden;display:flex;flex-direction:column;justify-content:flex-end;min-height:clamp(200px,17vw,250px);padding:18px 20px 20px;border-radius:18px;
  background:radial-gradient(90% 80% at 60% 35%,#1C1C22 0%,#0D0D10 75%);color:#fff;text-decoration:none;transition:transform .5s cubic-bezier(.2,.7,.2,1),box-shadow .5s}
.jt-art{position:absolute;z-index:-2;left:8%;right:-6%;top:-4%;bottom:22%;transition:transform .8s cubic-bezier(.2,.7,.2,1)}
.jt-art .sv-scene{position:absolute;inset:0}
.jt::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(0deg,rgba(9,9,11,.96) 0%,rgba(9,9,11,.75) 26%,rgba(9,9,11,0) 58%)}
.jt::before{content:"";position:absolute;left:0;right:0;bottom:0;height:3px;background:var(--sun);transform:scaleX(0);transform-origin:0 50%;transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.jt-n{font:500 11.5px var(--f-mono);letter-spacing:.08em;color:var(--sun)}
.jt-name{margin-top:6px;font-size:clamp(16px,1.25vw,19px);font-weight:400;line-height:1.25;letter-spacing:-0.01em}
.jt-go{position:absolute;right:16px;top:16px;display:grid;place-items:center;width:32px;height:32px;border-radius:50%;background:var(--sun);color:var(--ink);opacity:0;transform:scale(.6) rotate(-45deg);transition:opacity .35s,transform .5s cubic-bezier(.2,.7,.2,1)}
.jt-go svg{width:15px;height:15px;transform:rotate(90deg)}
.jt:hover,.jt:focus-visible{transform:translateY(-4px);box-shadow:0 24px 50px -28px rgba(9,9,11,.7)}
.jt:hover::before,.jt:focus-visible::before{transform:scaleX(1)}
.jt:hover .jt-art,.jt:focus-visible .jt-art{transform:scale(1.07) translateY(-3px)}
.jt:hover .jt-go,.jt:focus-visible .jt-go{opacity:1;transform:none}
.sl-jump .sv-scene .pc{transition-delay:calc(var(--i) * 70ms + var(--j) * 110ms)}
.sl-jump .sv-scene.on .fl,.sl-jump .sv-scene.on .fg,.sl-jump .sv-scene.on .scan{animation:none}
.jt:hover .sv-scene.on .fl,.jt:hover .sv-scene.on .fg{animation:svFlow 1.1s linear infinite}
.jt:hover .sv-scene.on .scan{animation:svScan 3.6s cubic-bezier(.45,0,.55,1) infinite alternate}

.sv-wrap{display:grid;grid-template-columns:minmax(0,1.12fr) minmax(0,1fr);gap:clamp(40px,6vw,100px);margin-top:clamp(50px,6vw,90px)}
.sv-stage{position:sticky;top:96px;height:calc(100svh - 128px);display:flex;align-items:center}
.sv-plate{position:relative;width:100%;aspect-ratio:560/440;max-height:100%;border-radius:24px;overflow:hidden;isolation:isolate;
  background:radial-gradient(90% 80% at 50% 45%,#1A1A20 0%,#0D0D10 72%);box-shadow:0 30px 80px -40px rgba(9,9,11,.6)}
.sv-plate::before{content:"";position:absolute;inset:0;z-index:-1;opacity:.55;
  background-image:radial-gradient(rgba(255,255,255,.09) 1px,transparent 1.2px);background-size:22px 22px;
  -webkit-mask-image:radial-gradient(75% 70% at 50% 50%,#000 30%,transparent 100%);mask-image:radial-gradient(75% 70% at 50% 50%,#000 30%,transparent 100%)}
.sv-plate .sv-scene{position:absolute;inset:0;opacity:0;transition:opacity .6s ease}
.sv-plate .sv-scene.on{opacity:1}
.sv-count{position:absolute;left:24px;top:22px;display:flex;align-items:baseline;gap:8px;font:500 12px var(--f-mono);letter-spacing:.06em;color:rgba(255,255,255,.75)}
.sv-count b{font-weight:500;color:#fff}
.sv-count i{position:relative;align-self:center;display:block;width:72px;height:2px;margin-left:8px;background:rgba(255,255,255,.18);border-radius:2px;overflow:hidden}
.sv-count em{position:absolute;inset:0;background:var(--sun);transform-origin:0 50%;transform:scaleX(.125);transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.sv-cap{position:absolute;right:22px;bottom:18px;font:500 10.5px var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.62)}

/* drawings build up piece by piece when their service comes into view */
.sv-scene .pc{opacity:0;transform:translateY(-14px);transition:opacity .5s ease calc(var(--i) * 90ms),transform .8s cubic-bezier(.2,.7,.2,1) calc(var(--i) * 90ms)}
.sv-scene.on .pc{opacity:1;transform:none}
.sv-scene.on .fl,.sv-scene.on .fg{animation:svFlow 1.1s linear infinite}
.sv-scene.on .scan{animation:svScan 3.6s cubic-bezier(.45,0,.55,1) infinite alternate}
@keyframes svFlow{to{stroke-dashoffset:-18}}
@keyframes svScan{from{transform:translate(0,0)}to{transform:translate(204px,118px)}}

.sv{position:relative;min-height:calc(100svh - 160px);display:flex;flex-direction:column;justify-content:center;padding:40px 0 40px 30px;scroll-margin-top:90px}
.sv::before{content:"";position:absolute;left:0;top:50%;width:2px;height:62%;transform:translateY(-50%);background:var(--line);border-radius:2px}
.sv::after{content:"";position:absolute;left:0;top:50%;width:2px;height:62%;transform:translateY(-50%) scaleY(0);background:var(--sun);border-radius:2px;transition:transform .8s cubic-bezier(.2,.7,.2,1)}
.sv.on::after{transform:translateY(-50%) scaleY(1)}
.sv:focus{outline:none}
.sv-media{display:none}
.sv-top{display:flex;align-items:center;gap:14px}
.sv-n{font:500 12px var(--f-mono);letter-spacing:.08em;color:var(--accent-ink)}
.sv-tag{padding:5px 11px;border-radius:999px;background:var(--paper);font:500 11.5px var(--f-mono);letter-spacing:.04em;color:var(--ink)}
.sv h3{margin:18px 0 0;font-size:clamp(32px,3.2vw,48px);font-weight:300;line-height:1.05;letter-spacing:-0.04em;color:var(--ink)}
.sv>p{margin:18px 0 0;max-width:46ch;font-size:clamp(16.5px,1.2vw,18px);line-height:1.65;color:var(--muted)}
.sv-inc{list-style:none;margin:26px 0 0;padding:0;max-width:46ch}
.sv-inc li{display:flex;align-items:flex-start;gap:12px;padding:13px 0;border-top:1px solid var(--line);font-size:16px;line-height:1.45;color:var(--ink)}
.sv-inc li:last-child{border-bottom:1px solid var(--line)}
.sv-inc svg{flex:0 0 18px;width:18px;height:18px;margin-top:1px;padding:2px;border-radius:50%;background:var(--sun);color:var(--ink)}
.sv .text-link{align-self:flex-start;margin-top:22px}

.sl-cmp{background:var(--paper);padding-block:clamp(90px,11vw,150px)}
.cmp-wrap{overflow-x:auto;border-radius:20px;background:#fff}
.cmp-wrap:focus-visible{outline:2px solid var(--ink);outline-offset:3px;box-shadow:0 0 0 3px var(--sun)}
.cmp{width:100%;min-width:640px;border-collapse:collapse;font-size:16px;line-height:1.45}
.cmp th,.cmp td{padding:20px 24px;text-align:left;vertical-align:top;border-top:1px solid var(--line)}
.cmp thead th,.cmp thead td{border-top:0;padding-top:26px;padding-bottom:18px}
.cmp thead th{font-size:clamp(20px,1.8vw,26px);font-weight:500;letter-spacing:-0.02em;color:var(--ink)}
.cmp tbody th{width:24%;font:500 12px var(--f-mono);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding-top:23px}
.cmp td{width:25.3%;color:var(--ink);transition:background .3s}
.cmp td b{font-weight:500}
.cmp-y,.cmp-n{display:inline-flex;align-items:center;gap:9px}
.cmp-y svg{width:20px;height:20px;padding:3px;border-radius:50%;background:var(--sun);color:var(--ink)}
.cmp-n{color:var(--muted)}
.cmp-n i{display:block;width:20px;height:20px;border-radius:50%;border:1.5px solid #8A8A93;position:relative}
.cmp-n i::after{content:"";position:absolute;left:5px;right:5px;top:8px;height:1.5px;background:#8A8A93}
.sl-cmp .text-link{margin-top:26px}

.sl-proc{background:var(--navy-deep);color:#fff;padding-block:clamp(90px,11vw,150px)}
.sl-proc .eyebrow{color:var(--on-dark-muted)}
.sl-proc .sec-head h2{color:#fff}
.sl-proc .sec-head p{color:var(--on-dark-muted)}
.ps-wrap{position:relative;margin-top:clamp(30px,4vw,60px)}
.ps-line{position:absolute;left:0;right:0;top:7px;height:2px;background:rgba(255,255,255,.14);border-radius:2px;overflow:hidden}
.ps-line i{position:absolute;inset:0;background:var(--sun);transform-origin:0 50%;transform:scaleX(0)}
.ps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:clamp(18px,2.4vw,36px)}
.ps-step{position:relative}
.ps-dot{display:block;width:16px;height:16px;border-radius:50%;background:var(--navy-deep);border:2px solid rgba(255,255,255,.35);transition:background .5s,border-color .5s,box-shadow .5s}
.ps-n{display:block;margin-top:26px;font:500 12px var(--f-mono);letter-spacing:.08em;color:var(--on-dark-muted);transition:color .5s}
.ps-step h3{margin:10px 0 0;font-size:clamp(26px,2.4vw,36px);font-weight:300;letter-spacing:-0.035em;line-height:1.1;color:#fff}
.ps-step p{margin:12px 0 0;max-width:30ch;font-size:15.5px;line-height:1.6;color:var(--on-dark-muted)}
.ps-step.on .ps-dot{background:var(--sun);border-color:var(--sun);box-shadow:0 0 0 6px rgba(249,194,46,.2)}
.ps-step.on .ps-n{color:var(--sun)}

.sl-faq{padding-block:clamp(90px,11vw,150px)}
.sl-faq h2{font-size:clamp(32px,3.9vw,54px);color:var(--navy)}
.sl-faq .faq-grid>div:first-child p{color:var(--muted);margin-top:16px;max-width:34ch}
.sl-faq details p{color:var(--muted)}
.sl-faq summary .pm::before,.sl-faq summary .pm::after{background:var(--ink)}

@media (max-width:1100px){
  .sv-wrap{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
  .ps{grid-template-columns:repeat(3,minmax(0,1fr));row-gap:40px}
  .ps-line{display:none}
}
@media (max-width:900px){
  .sl-jump{grid-template-columns:repeat(2,minmax(0,1fr))}
  .jt{min-height:190px}
  .sv-wrap{display:block}
  .sv-stage{display:none}
  .sv{min-height:0;padding:0;margin-top:56px}
  .sv:first-child{margin-top:0}
  .sv::before,.sv::after{display:none}
  .sv-media{display:block;margin-bottom:22px;aspect-ratio:560/440;border-radius:18px;overflow:hidden;position:relative;
    background:radial-gradient(90% 80% at 50% 45%,#1A1A20 0%,#0D0D10 72%)}
  .sv-media .sv-scene{position:absolute;inset:0}
  .ps{grid-template-columns:1fr;row-gap:0}
  .ps-wrap{padding-left:34px}
  .ps-line{display:block;left:7px;right:auto;top:8px;bottom:8px;width:2px;height:auto}
  .ps-line i{transform-origin:50% 0;transform:scaleY(0)}
  .ps-step{padding-bottom:34px}
  .ps-step:last-child{padding-bottom:0}
  .ps-dot{position:absolute;left:-34px;top:4px}
  .ps-n{margin-top:0}
}
.cmp-cards{display:none}
@media (max-width:700px){
  .cmp-wrap{display:none}
  .cmp-cards{display:grid;gap:14px}
  .cc{padding:20px 18px;border-radius:20px;background:#fff}
  .cc-head{display:flex;align-items:center;gap:14px}
  .cc-ico{display:grid;place-items:center;flex:none;width:52px;height:52px;border-radius:50%;background:var(--navy-deep);color:var(--sun)}
  .cc-ico svg{width:26px;height:26px}
  .cc h3{margin:0;font-size:26px;font-weight:400;letter-spacing:-0.025em;line-height:1.1;color:var(--ink)}
  .cc-best{display:inline-flex;align-items:center;gap:7px;margin:6px 0 0;font-size:14.5px;color:var(--ink)}
  .cc-best::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--sun)}
  .cc-feats{list-style:none;margin:18px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
  .ccf{display:flex;flex-direction:column;align-items:center;gap:6px;padding:12px 6px 13px;border-radius:14px;background:var(--paper);text-align:center}
  .ccf-ico{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:#fff;color:#55555D}
  .ccf-ico svg{width:19px;height:19px}
  .ccf-l{font-size:13px;line-height:1.25;color:var(--ink)}
  .ccf-s{display:inline-flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:2px 4px;font-size:12.5px;font-weight:600;line-height:1.3;color:#55555D}
  .ccf-s svg{width:14px;height:14px}
  .ccf.is-yes,.ccf.is-part{background:#FFF4D4}
  .ccf.is-yes .ccf-ico,.ccf.is-part .ccf-ico{background:var(--sun);color:var(--ink)}
  .ccf.is-yes .ccf-s,.ccf.is-part .ccf-s{color:var(--ink)}
  .cc-extra{display:flex;flex-direction:column;gap:4px;margin:16px 0 0;padding-top:14px;border-top:1px solid var(--line);font-size:15.5px;color:var(--ink)}
  .cc-extra span{font:500 11px var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
}
@media (max-width:600px){
  .jt{min-height:160px;padding:14px 14px 16px;border-radius:16px}
  .jt-art{left:4%;right:-8%;bottom:30%}
  .jt-name{font-size:14.5px}
  .jt-go{display:none}
}
@media (prefers-reduced-motion: reduce){
  .sv-scene .pc{opacity:1;transform:none;transition:none}
  .sv-scene.on .fl,.sv-scene.on .fg,.sv-scene.on .scan{animation:none}
  .sv::after,.sv-count em,.sv-plate .sv-scene{transition:none}
  .ps-line i{transform:none!important}
}
'''
head = head[:head.rindex('</style>')] + CSS + head[head.rindex('</style>'):]

JS = r'''/* ---------- Hero: static photo; the two headline lines rise in one after the other on load ---------- */
(function(){ const h = document.getElementById('sl-hero'); if (!h) return; requestAnimationFrame(() => setTimeout(() => h.classList.add('in'), 60)); })();

/* ---------- Services: the plate shows the drawing for the service nearest the middle of the screen ---------- */
(function(){
  const list = document.getElementById('svList'), plate = document.getElementById('svPlate'); if (!list || !plate) return;
  const arts = [...list.querySelectorAll('.sv')], scenesD = [...plate.querySelectorAll('.sv-scene')];
  const num = document.getElementById('svNum'), bar = document.getElementById('svBar');
  let cur = -1, queued = false;
  const set = k => {
    if (k === cur) return; cur = k;
    arts.forEach((a, i) => a.classList.toggle('on', i === k));
    scenesD.forEach((s, i) => s.classList.toggle('on', i === k));
    num.textContent = String(k + 1).padStart(2, '0'); bar.style.transform = 'scaleX(' + ((k + 1) / arts.length) + ')';
  };
  const update = () => {
    queued = false; if (innerWidth <= 900) return;
    const mid = innerHeight / 2; let best = 0, bd = Infinity;
    arts.forEach((a, i) => { const r = a.getBoundingClientRect(), dd = Math.abs(r.top + r.height / 2 - mid); if (dd < bd){ bd = dd; best = i; } });
    set(best);
  };
  addEventListener('scroll', () => { if (!queued){ queued = true; requestAnimationFrame(update); } }, { passive:true });
  addEventListener('resize', update); update();
  // phones: each drawing builds when it scrolls into view
  const mob = [...list.querySelectorAll('.sv-media .sv-scene')];
  if (reduce || !('IntersectionObserver' in window)) mob.forEach(s => s.classList.add('on'));
  else mob.forEach(s => { const io = new IntersectionObserver(es => { if (es[0].isIntersecting){ s.classList.add('on'); io.disconnect(); } }, { rootMargin:'0px 0px -20% 0px' }); io.observe(s); });
  const tiles = [...document.querySelectorAll('.sl-jump .sv-scene')];
  if (reduce || !('IntersectionObserver' in window)) tiles.forEach(s => s.classList.add('on'));
  else { const jio = new IntersectionObserver(es => { if (es[0].isIntersecting){ tiles.forEach(s => s.classList.add('on')); jio.disconnect(); } }, { rootMargin:'0px 0px -15% 0px' }); jio.observe(document.querySelector('.sl-jump')); }
  // jump links: move keyboard focus to the service as well
  document.querySelectorAll('.sl-jump a').forEach(a => a.addEventListener('click', () => {
    const t = document.querySelector(a.getAttribute('href')); if (!t) return;
    if (lenis) lenis.scrollTo(t, { offset: innerWidth <= 900 ? -84 : -10, duration: 1.5, easing: e => e < .5 ? 4 * e * e * e : 1 - Math.pow(-2 * e + 2, 3) / 2 });   // clear of the nav pill on phones
    setTimeout(() => t.focus({ preventScroll:true }), 40);
  }));
})();

/* ---------- Sun path: the sun rises and sets along the arc as you scroll past the heading ---------- */
(function(){
  const sun = document.getElementById('spSun'), day = document.getElementById('spDay'); if (!sun || !day) return;
  const box = sun.closest('svg');
  const place = t => {
    const x = (1 - t) * (1 - t) * 40 + 2 * (1 - t) * t * 600 + t * t * 1160, y = (1 - t) * (1 - t) * 112 + 2 * (1 - t) * t * -60 + t * t * 112;
    sun.setAttribute('transform', 'translate(' + x.toFixed(1) + ' ' + y.toFixed(1) + ')'); day.style.strokeDashoffset = (1 - t).toFixed(4);
  };
  if (reduce){ place(.5); return; }
  let queued = false;
  const update = () => { queued = false; const r = box.getBoundingClientRect(); place(Math.min(1, Math.max(0, (innerHeight - r.top) / (innerHeight * .95)))); };
  addEventListener('scroll', () => { if (!queued){ queued = true; requestAnimationFrame(update); } }, { passive:true });
  addEventListener('resize', update); update();
})();

/* ---------- Background drawings drift slightly slower than the page ---------- */
(function(){
  if (reduce) return;
  const arts = [...document.querySelectorAll('.bg-array, .bg-house')]; if (!arts.length) return;
  let queued = false;
  const update = () => { queued = false; arts.forEach(a => { const r = a.parentNode.getBoundingClientRect(); const p = (innerHeight - r.top) / (innerHeight + r.height); a.style.transform = 'translateY(' + ((.5 - p) * 60).toFixed(1) + 'px)'; }); };
  addEventListener('scroll', () => { if (!queued){ queued = true; requestAnimationFrame(update); } }, { passive:true }); update();
})();

/* ---------- How we work: the yellow line fills as you scroll; each step lights up as the line reaches it ---------- */
(function(){
  const wrap = document.getElementById('psWrap'), fill = document.getElementById('psFill'); if (!wrap || !fill) return;
  const steps = [...wrap.querySelectorAll('.ps-step')];
  if (reduce){ steps.forEach(s => s.classList.add('on')); return; }
  let queued = false;
  const update = () => {
    queued = false;
    const r = wrap.getBoundingClientRect(), vert = innerWidth <= 900;
    const start = innerHeight * .85, end = innerHeight * (vert ? .35 : .45);
    const p = vert ? Math.min(1, Math.max(0, (innerHeight * .6 - r.top) / r.height))
                   : Math.min(1, Math.max(0, (start - r.top) / (start - end)));
    fill.style.transform = vert ? 'scaleY(' + p.toFixed(4) + ')' : 'scaleX(' + p.toFixed(4) + ')';
    steps.forEach((s, i) => {
      if (vert){ const b = s.getBoundingClientRect(); s.classList.toggle('on', b.top + 12 < innerHeight * .6); }
      else s.classList.toggle('on', p >= i / (steps.length - 1) - .001);
    });
  };
  addEventListener('scroll', () => { if (!queued){ queued = true; requestAnimationFrame(update); } }, { passive:true });
  addEventListener('resize', update); update();
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
          + js_core + js_nav + js_reveal + JS + '})();\n</script>\n')
src = (head + body + script).replace('index.html#contact', 'contact.html')   # the Contact page now exists
open(d + 'solutions_src.html', 'w').write(src)

mime = {'png':'image/png','jpg':'image/jpeg','webp':'image/webp'}
import sys; sys.path.insert(0, d); from webp_cache import webp   # all images as WebP
def uri(path): path = webp(path); return 'data:' + mime[path.rsplit('.',1)[1]] + ';base64,' + base64.b64encode(open(path,'rb').read()).decode()
out = re.sub(r'\{\{L:([^}]+)\}\}', lambda m: uri(d + 'layers/' + m.group(1)), src)
out = out.replace('{{LOGO_BLACK}}', uri(d + 'logo_black.png')).replace('{{LOGO_WHITE}}', uri(d + 'logo_white.png'))
assert '{{' not in out, re.findall(r'\{\{[^}]+\}\}', out)[:3]
hi = out.index('<!-- ======= NAV ======= -->')
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
       + out[:hi] + '</head>\n<body>\n' + out[hi:] + '</body>\n</html>\n')
open(d + 'solutions.html', 'w').write(doc)
print('solutions.html', len(doc) // 1024, 'KB')
