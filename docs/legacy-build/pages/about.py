# About Us page. Shares the homepage's stylesheet, nav, footer, smooth scroll, menu, glass nav, floating
# elements and leader cards (all lifted from src_draft.html), and adds its own sections:
# hero, story, milestones timeline (line fills as you scroll), vision & mission, manufacturing & recognition,
# leadership preview and a closing call to action.
import re, base64
d = '/tmp/claude-0/site/'
home = open(d + 'src_draft.html').read()
def cut(a, b, src=home, inclusive_a=True):
    i = src.index(a); j = src.index(b, i + len(a)); return src[i if inclusive_a else i + len(a):j]

ARR = '<svg class="arr" width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 9h10M10 5l4 4-4 4"/></svg>'
LINKS = [('#about', 'about.html'), ('#solutions', 'index.html#solutions'), ('#projects', 'index.html#projects'), ('#gallery', 'index.html#gallery'),
         ('#team', 'index.html#team'), ('#contact', 'index.html#contact'), ('#blog', 'index.html#blog'), ('#top', 'index.html')]
def relink(html):
    for a, b in LINKS: html = html.replace(f'href="{a}"', f'href="{b}"')
    return html.replace('href="about.html"', 'href="about.html"')

# ---------- shared pieces from the homepage ----------
head = home[:home.index('<!-- ======= NAV ======= -->')]
head = head.replace('<title>Sinelab Website</title>', '<title>About Us | Sinelab Technologies</title>')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Rooted in the manufacturing legacy of SARK Group since 1996, Sinelab Technologies delivers solar, energy storage and lighting solutions across Kerala.">', head)
nav = relink(cut('<!-- ======= NAV ======= -->', '<main id="top">'))
nav = nav.replace('<a class="nav-logo" href="index.html"', '<a class="nav-logo" href="index.html"')
nav = nav.replace('<a href="about.html">About Us</a>', '<a href="about.html" aria-current="page">About Us</a>')
nav = nav.replace('<a href="about.html" style="--i:0">About Us', '<a href="about.html" style="--i:0" aria-current="page">About Us')
foot = relink(home[home.index('<footer'):home.index('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js">')])
SIL = '<svg viewBox="0 0 40 40" fill="currentColor" aria-hidden="true"><circle cx="20" cy="14" r="8"/><path d="M4 40c0-9 7-15 16-15s16 6 16 15z"/></svg>'
TEAM = [
  ('Sajeev Kumar K', 'Managing Director', 'Co-founder', 'Co-founded SARK Cables in Kanjikode in 1996 with his classmate Sunil Joseph, and grew the group to Thodupuzha, Coimbatore and Qatar. A former President of the Kanjikode Industries Forum.'),
  ('Sunil Joseph', 'Director', 'Co-founder', 'Instrumental in the growth of the SARK Group since 1996, including its move into renewable energy through Sinelab. An entrepreneurship mentor and industry speaker, active in KSSIA.'),
  ('Athul S. Krishna', 'Chief Marketing Officer', 'Leadership', 'An Electrical and Electronics engineer with postgraduate certification in Business Analytics from IIT Roorkee. Heads Sinelab’s Kochi operations and regional expansion.'),
  ('Sravan Paul Sunil', 'Chief Operating Officer', 'Leadership', 'A graduate of SRM Institute of Science and Technology, Chennai. Supports Sinelab’s operational management, project coordination and site execution.'),
  ('Ravinder Mehta', 'Head of Solar Division', 'Leadership', ''),   # added 29 Oct (user); grouped with the leadership
  # added 29 Oct (user); designations to come from the user
  ('Saran', 'Regional Manager, Kochi Division', 'Team', ''),
  ('Leenu Joseph', 'Project Engineer, Kochi Division', 'Team', ''),
]
# real portraits (user's Downloads). Others keep the silhouette until their photos arrive.
PHOTOS = {n: (f'team_{k}_sq.jpg', f'team_{k}_tall.jpg') for n, k in [('Sajeev Kumar K', 'sajeev'), ('Sunil Joseph', 'sunil'), ('Athul S. Krishna', 'athul'),
          ('Sravan Paul Sunil', 'sravan'), ('Saran', 'saran'), ('Leenu Joseph', 'leenu'), ('Ravinder Mehta', 'ravinder')]}
def tm_card(n, r, g, b, big):
    ph = ('<img src="{{L:' + PHOTOS[n][1 if big else 0] + '}}" alt="" loading="lazy">') if n in PHOTOS else SIL
    tbc = ' tbc' if 'to be confirmed' in r else ''
    bio = f'<p class="tm-bio">{b}</p>' if (b and big) else ''
    rr = r if (', ' not in r or tbc) else r.split(', ', 1)[0] + '<span class="tm-div">' + r.split(', ', 1)[1] + '</span>'   # 'Regional Manager' / 'Kochi Division' on two lines   # user: name + designation only for the team; bios stay for the two founders
    return f'''        <article class="tm-card{" tm-lg" if big else ""}">
          <div class="tm-ph{" has-img" if n in PHOTOS else ""}">{ph}<span class="ab-ld-tag">{g}</span></div>
          <div class="tm-body"><h3>{n}</h3><p class="tm-role{tbc}">{rr}</p>{bio}</div>
        </article>'''
founders = [t for t in TEAM if t[2] == 'Co-founder']; others = [t for t in TEAM if t[2] != 'Co-founder']
leaders = ('<div class="tm">\n      <div class="tm-founders">\n' + '\n'.join(tm_card(*t, True) for t in founders) + '\n      </div>\n'
           + '      <div class="tm-team">\n' + '\n'.join(tm_card(*t, False) for t in others) + '\n      </div>\n    </div>\n')

js_core = cut('(function(){\nconst reduce', '/* ---------- Solar panel model').replace("node.matches('.leaders')", "node.matches('.leaders:not(.ab-leaders)')")
js_nav = cut('/* ---------- Floating glass nav: compact', '/* ---------- Why Sinelab: the reason nearest')
js_reveal = cut('/* ---------- Reveal cards ---------- */', '/* ---------- Savings calculator')
js_leaders = cut('/* ---------- Our people: the card you point at', '/* ---------- Enquiry form')
def rp(s, a, b):
    assert a in s, a[:80]; return s.replace(a, b)
js_nav = rp(js_nav, "['#anatomy','#films','#savings','#faq','footer']", "['#ab-hero','#vision','footer']")
js_nav = rp(js_nav, "['#why','#solutions','#projects','#gallery','#faq','#blog','#contact']", "['#story','#milestones','#facilities','#ab-team']")
js_reveal = rp(js_reveal, "'.sol-grid .sol, .team > *, .leader, .t-deck, .post, .why-card'", "'.tm-card, .ab-site, .ab-award, .ab-vm-item, .ab-pr li, .ab-story-body > p'")

# ---------- page sections ----------
MILES = [
  ('1996', 'Where it began', 'SARK Cables established in Kanjikode by Sajeev Kumar K and Sunil Joseph.'),
  ('2002', 'Growing to Thodupuzha', 'Manufacturing expands to a plant in Thodupuzha.'),
  ('2008', 'Into Coimbatore', 'Manufacturing expands to a facility in Coimbatore.'),
  ('2013', 'Sinelab is born', 'Sinelab Technologies is founded as an energy-focused venture, starting with industrial lighting, high-mast and streetlighting systems and solar streetlight batteries.'),
  ('2018', 'Recognition', 'The founders’ entrepreneurial journey is recognised with the Asianet Keerthimudra Award in the Electrical and Electronics sector.'),
  ('2019', 'Power for a community', 'A government 20 kW off-grid solar project brings dependable power to a tribal village in the Nelliampathy Hills.'),
  ('2024', 'Storage, made in-house', 'A Kanjikode facility for lithium batteries and integrated lithium inverter solutions.'),
  ('2025', 'Megawatt-scale', 'Approximately 4–5 MW of solar installations commissioned in a single year.'),
  ('2026', 'A flagship 1 MW rooftop', 'Installation completed on a flagship 1 MW rooftop project. Commissioning pending.'),
]
tl = '\n'.join(f'''        <li class="tl-item"><div class="tl-year">{y}</div><span class="tl-dot" aria-hidden="true"></span><div class="tl-body"><h3>{t}</h3><p>{x}</p></div></li>''' for y, t, x in MILES)
SITES = [('1996', 'Kanjikode, Palakkad', 'SARK Cables, where the group began.', 'SARK Group', ''),
         ('2002', 'Thodupuzha', 'Manufacturing expansion.', 'SARK Group', ''),
         ('2008', 'Coimbatore', 'Manufacturing expansion.', 'SARK Group', ''),
         ('Overseas', 'Qatar', 'Manufacturing operations.', 'SARK Group', ''),
         ('2024', 'Kanjikode Industrial Area', 'Lithium batteries and integrated lithium inverters.', 'Sinelab', ' hi')]
sites = '\n'.join(f'''        <li class="ab-site{h}"><span class="ab-site-y">{y}</span><span class="ab-site-dot" aria-hidden="true"></span><h3>{n}</h3><p>{t}</p><span class="ab-site-tag">{g}</span></li>''' for y, n, t, g, h in SITES)
TROPHY = '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10h24v14a12 12 0 0 1-24 0z"/><path d="M20 15h-7a7 7 0 0 0 9 9M44 15h7a7 7 0 0 1-9 9M32 36v10M24 54h16M26 46h12v8H26z"/></svg>'

body = f'''{nav}
<main id="top">

<!-- ======= ABOUT HERO ======= -->
<section class="ab-hero" id="ab-hero" aria-labelledby="abTitle">
  <div class="ab-hero-bg" aria-hidden="true"><img class="ab-hero-img" src="{{{{L:proj3.jpg}}}}" alt=""></div>
  <span class="hl-ph ab-ph">Sample photo</span>
  <div class="wrap ab-hero-copy">
    <nav class="ab-crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">About us</span></nav>
    <h1 class="ab-h1" id="abTitle"><span class="ln"><span>Built on a legacy.</span></span><span class="ln"><span><em>Driven by a vision.</em></span></span></h1>
    <p class="ab-since"><span>Since 1996</span><span>Palakkad</span><span>Kochi</span></p>
  </div>
  <div class="ab-cue" aria-hidden="true"><span>Scroll</span><i></i></div>
</section>

<!-- ======= STORY ======= -->
<section class="ab-story band" id="story">
  <div class="wrap">
    <div class="ab-story-in">
      <figure class="ab-story-media"><img src="{{{{L:pj_drone.jpg}}}}" alt="Aerial view of a rooftop solar installation"><span class="hl-ph">Sample photo</span></figure>
      <div class="ab-story-body">
        <div class="eyebrow">Our story</div>
        <h2>From classmates to <em>industry leaders</em></h2>
        <p class="ab-pull" data-fill>Some journeys begin with a business plan. Ours began with two classmates who shared an ambition to build something meaningful.</p>
        <p class="ab-story-p">In 1996, Sajeev Kumar K and Sunil Joseph founded SARK Cables in Kanjikode. In 2013, that experience gave rise to Sinelab Technologies, first lighting major junctions and public spaces across Kerala, and now powering homes, businesses and industries with solar and storage.</p>
      </div>
    </div>
    <dl class="ab-stats" id="abStats">
      <div><dt>Industrial heritage, beginning with SARK Cables</dt><dd>1996</dd></div>
      <div><dt>Sinelab Technologies founded</dt><dd>2013</dd></div>
      <div><dt>Solar commissioned in 2025 (approx.)</dt><dd>4–5<small>MW</small></dd></div>
      <div><dt>Offices in Palakkad and Kochi, Kerala</dt><dd>2<small>offices</small></dd></div>
    </dl>
  </div>
</section>

<!-- ======= RECOGNITION (user: award above the milestones) ======= -->
<section class="ab-rec" id="recognition" aria-labelledby="recTitle">
  <div class="rec-bg" aria-hidden="true">
    <div class="floaters run">
      <div class="flp" style="left:2.5%;top:4%;--s:84px"><div class="fl" style="--o:0.1;--d:9s;--dl:-0.0s;--dx:-8px;--dy:12px;--r0:-12deg;--r1:-4deg"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"><circle cx="24" cy="24" r="8.5"/><path d="M24 5v6M24 37v6M5 24h6M37 24h6M10.6 10.6l4.2 4.2M33.2 33.2l4.2 4.2M10.6 37.4l4.2-4.2M33.2 14.8l4.2-4.2"/></svg></div></div>
      <div class="flp" style="left:9%;top:70%;--s:24px"><div class="fl y" style="--o:0.5;--d:10s;--dl:-1.3s;--dx:12px;--dy:-15px;--r0:1deg;--r1:9deg"><svg viewBox="0 0 48 48" fill="currentColor"><path d="M24 6c1.4 9.6 8.4 16.6 18 18-9.6 1.4-16.6 8.4-18 18-1.4-9.6-8.4-16.6-18-18 9.6-1.4 16.6-8.4 18-18z"/></svg></div></div>
      <div class="flp" style="left:92%;top:2%;--s:76px"><div class="fl" style="--o:0.08;--d:11s;--dl:-2.6s;--dx:-16px;--dy:-18px;--r0:-10deg;--r1:-2deg"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.3"><circle cx="24" cy="24" r="17"/><circle cx="24" cy="24" r="9" stroke-dasharray="2 4"/></svg></div></div>
      <div class="flp" style="left:94%;top:58%;--s:58px"><div class="fl" style="--o:0.1;--d:12s;--dl:-3.9s;--dx:8px;--dy:21px;--r0:3deg;--r1:11deg"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"><circle cx="24" cy="29" r="11"/><path d="M17 20 11 6h8l5 10M31 20l6-14h-8l-5 10M24 23l1.8 3.7 4 .6-2.9 2.8.7 4-3.6-1.9-3.6 1.9.7-4-2.9-2.8 4-.6z"/></svg></div></div>
      <div class="flp" style="left:47%;top:86%;--s:40px"><div class="fl" style="--o:0.08;--d:13s;--dl:-5.2s;--dx:-12px;--dy:-12px;--r0:-8deg;--r1:0deg"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"><path d="M9 39C9 19 22 9 40 8c0 19-11 31-31 31z"/><path d="M9 39C17 30 24 24 31 17"/></svg></div></div>
      <div class="flp" style="left:86%;top:88%;--s:18px"><div class="fl y" style="--o:0.5;--d:9s;--dl:-6.5s;--dx:16px;--dy:-15px;--r0:5deg;--r1:13deg"><svg viewBox="0 0 48 48" fill="currentColor"><path d="M24 6c1.4 9.6 8.4 16.6 18 18-9.6 1.4-16.6 8.4-18 18-1.4-9.6-8.4-16.6-18-18 9.6-1.4 16.6-8.4 18-18z"/></svg></div></div>
      <div class="flp" style="left:30%;top:-2%;--s:16px"><div class="fl y" style="--o:0.45;--d:10s;--dl:-7.8s;--dx:-8px;--dy:18px;--r0:-6deg;--r1:2deg"><svg viewBox="0 0 48 48" fill="currentColor"><path d="M24 6c1.4 9.6 8.4 16.6 18 18-9.6 1.4-16.6 8.4-18 18-1.4-9.6-8.4-16.6-18-18 9.6-1.4 16.6-8.4 18-18z"/></svg></div></div>
    </div>
  </div>
  <div class="wrap">
    <div class="ab-award">
      <span class="rec-num" aria-hidden="true">2018</span>
      <div class="ab-award-ph"><svg class="rec-emblem" viewBox="0 0 400 320" aria-hidden="true"><g class="rec-rays" stroke="#F9C22E" stroke-width="1.2" stroke-linecap="round" stroke-dasharray="2 7"><line x1="328.0" y1="160.0" x2="390.0" y2="160.0"/><line x1="323.6" y1="193.1" x2="383.5" y2="209.2"/><line x1="310.9" y1="224.0" x2="364.5" y2="255.0"/><line x1="290.5" y1="250.5" x2="334.4" y2="294.4"/><line x1="264.0" y1="270.9" x2="295.0" y2="324.5"/><line x1="233.1" y1="283.6" x2="249.2" y2="343.5"/><line x1="200.0" y1="288.0" x2="200.0" y2="350.0"/><line x1="166.9" y1="283.6" x2="150.8" y2="343.5"/><line x1="136.0" y1="270.9" x2="105.0" y2="324.5"/><line x1="109.5" y1="250.5" x2="65.6" y2="294.4"/><line x1="89.1" y1="224.0" x2="35.5" y2="255.0"/><line x1="76.4" y1="193.1" x2="16.5" y2="209.2"/><line x1="72.0" y1="160.0" x2="10.0" y2="160.0"/><line x1="76.4" y1="126.9" x2="16.5" y2="110.8"/><line x1="89.1" y1="96.0" x2="35.5" y2="65.0"/><line x1="109.5" y1="69.5" x2="65.6" y2="25.6"/><line x1="136.0" y1="49.1" x2="105.0" y2="-4.5"/><line x1="166.9" y1="36.4" x2="150.8" y2="-23.5"/><line x1="200.0" y1="32.0" x2="200.0" y2="-30.0"/><line x1="233.1" y1="36.4" x2="249.2" y2="-23.5"/><line x1="264.0" y1="49.1" x2="295.0" y2="-4.5"/><line x1="290.5" y1="69.5" x2="334.4" y2="25.6"/><line x1="310.9" y1="96.0" x2="364.5" y2="65.0"/><line x1="323.6" y1="126.9" x2="383.5" y2="110.8"/></g><circle cx="200" cy="160" r="74" fill="none" stroke="rgba(255,255,255,.12)" stroke-width="1"/><g class="rec-laurel" fill="rgba(249,194,46,.16)" stroke="#F9C22E" stroke-width="1.5"><path fill="none" d="M183.0 256.5 A98 98 0 0 1 169.7 66.8"/><path fill="none" d="M217.0 256.5 A98 98 0 0 0 230.3 66.8"/><ellipse cx="174.4" cy="259.3" rx="14.0" ry="5.6" transform="rotate(162.0 174.4 259.3)"/><ellipse cx="175.9" cy="251.0" rx="14.0" ry="5.6" transform="rotate(218.0 175.9 251.0)"/><ellipse cx="146.7" cy="247.6" rx="13.5" ry="5.4" transform="rotate(178.9 146.7 247.6)"/><ellipse cx="150.5" cy="240.0" rx="13.5" ry="5.4" transform="rotate(234.9 150.5 240.0)"/><ellipse cx="123.5" cy="228.3" rx="12.9" ry="5.2" transform="rotate(195.8 123.5 228.3)"/><ellipse cx="129.4" cy="222.2" rx="12.9" ry="5.2" transform="rotate(251.8 129.4 222.2)"/><ellipse cx="107.0" cy="203.2" rx="12.4" ry="4.9" transform="rotate(212.7 107.0 203.2)"/><ellipse cx="114.4" cy="199.0" rx="12.4" ry="4.9" transform="rotate(268.7 114.4 199.0)"/><ellipse cx="98.5" cy="174.3" rx="11.8" ry="4.7" transform="rotate(229.6 98.5 174.3)"/><ellipse cx="106.7" cy="172.4" rx="11.8" ry="4.7" transform="rotate(285.6 106.7 172.4)"/><ellipse cx="98.7" cy="144.2" rx="11.3" ry="4.5" transform="rotate(246.4 98.7 144.2)"/><ellipse cx="107.1" cy="144.8" rx="11.3" ry="4.5" transform="rotate(302.4 107.1 144.8)"/><ellipse cx="107.7" cy="115.4" rx="10.7" ry="4.3" transform="rotate(263.3 107.7 115.4)"/><ellipse cx="115.5" cy="118.5" rx="10.7" ry="4.3" transform="rotate(319.3 115.5 118.5)"/><ellipse cx="124.6" cy="90.5" rx="10.2" ry="4.1" transform="rotate(280.2 124.6 90.5)"/><ellipse cx="131.2" cy="95.7" rx="10.2" ry="4.1" transform="rotate(336.2 131.2 95.7)"/><ellipse cx="148.0" cy="71.6" rx="9.6" ry="3.9" transform="rotate(297.1 148.0 71.6)"/><ellipse cx="152.9" cy="78.5" rx="9.6" ry="3.9" transform="rotate(353.1 152.9 78.5)"/><ellipse cx="176.0" cy="60.3" rx="9.1" ry="3.6" transform="rotate(314.0 176.0 60.3)"/><ellipse cx="178.6" cy="68.4" rx="9.1" ry="3.6" transform="rotate(370.0 178.6 68.4)"/><ellipse cx="224.1" cy="251.0" rx="14.0" ry="5.6" transform="rotate(-38.0 224.1 251.0)"/><ellipse cx="225.6" cy="259.3" rx="14.0" ry="5.6" transform="rotate(18.0 225.6 259.3)"/><ellipse cx="249.5" cy="240.0" rx="13.5" ry="5.4" transform="rotate(-54.9 249.5 240.0)"/><ellipse cx="253.3" cy="247.6" rx="13.5" ry="5.4" transform="rotate(1.1 253.3 247.6)"/><ellipse cx="270.6" cy="222.2" rx="12.9" ry="5.2" transform="rotate(-71.8 270.6 222.2)"/><ellipse cx="276.5" cy="228.3" rx="12.9" ry="5.2" transform="rotate(-15.8 276.5 228.3)"/><ellipse cx="285.6" cy="199.0" rx="12.4" ry="4.9" transform="rotate(-88.7 285.6 199.0)"/><ellipse cx="293.0" cy="203.2" rx="12.4" ry="4.9" transform="rotate(-32.7 293.0 203.2)"/><ellipse cx="293.3" cy="172.4" rx="11.8" ry="4.7" transform="rotate(-105.6 293.3 172.4)"/><ellipse cx="301.5" cy="174.3" rx="11.8" ry="4.7" transform="rotate(-49.6 301.5 174.3)"/><ellipse cx="292.9" cy="144.8" rx="11.3" ry="4.5" transform="rotate(-122.4 292.9 144.8)"/><ellipse cx="301.3" cy="144.2" rx="11.3" ry="4.5" transform="rotate(-66.4 301.3 144.2)"/><ellipse cx="284.5" cy="118.5" rx="10.7" ry="4.3" transform="rotate(-139.3 284.5 118.5)"/><ellipse cx="292.3" cy="115.4" rx="10.7" ry="4.3" transform="rotate(-83.3 292.3 115.4)"/><ellipse cx="268.8" cy="95.7" rx="10.2" ry="4.1" transform="rotate(-156.2 268.8 95.7)"/><ellipse cx="275.4" cy="90.5" rx="10.2" ry="4.1" transform="rotate(-100.2 275.4 90.5)"/><ellipse cx="247.1" cy="78.5" rx="9.6" ry="3.9" transform="rotate(-173.1 247.1 78.5)"/><ellipse cx="252.0" cy="71.6" rx="9.6" ry="3.9" transform="rotate(-117.1 252.0 71.6)"/><ellipse cx="221.4" cy="68.4" rx="9.1" ry="3.6" transform="rotate(-190.0 221.4 68.4)"/><ellipse cx="224.0" cy="60.3" rx="9.1" ry="3.6" transform="rotate(-134.0 224.0 60.3)"/></g><g fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" transform="translate(160 114) scale(1.25)"><path d="M20 10h24v14a12 12 0 0 1-24 0z"/><path d="M20 15h-7a7 7 0 0 0 9 9M44 15h7a7 7 0 0 1-9 9M32 36v10M24 54h16M26 46h12v8H26z"/></g><g class="rec-sparks" fill="#F9C22E"><path transform="translate(92 62) scale(1.1)" d="M0 -10C.7 -4.6 4.6 -.7 10 0 4.6 .7 .7 4.6 0 10-.7 4.6-4.6 .7-10 0-4.6-.7-.7-4.6 0-10z"/><path transform="translate(318 92) scale(0.8)" d="M0 -10C.7 -4.6 4.6 -.7 10 0 4.6 .7 .7 4.6 0 10-.7 4.6-4.6 .7-10 0-4.6-.7-.7-4.6 0-10z"/><path transform="translate(300 250) scale(1)" d="M0 -10C.7 -4.6 4.6 -.7 10 0 4.6 .7 .7 4.6 0 10-.7 4.6-4.6 .7-10 0-4.6-.7-.7-4.6 0-10z"/><path transform="translate(78 236) scale(0.7)" d="M0 -10C.7 -4.6 4.6 -.7 10 0 4.6 .7 .7 4.6 0 10-.7 4.6-4.6 .7-10 0-4.6-.7-.7-4.6 0-10z"/></g></svg><span class="ph-note">Award photo to be added</span></div>
      <div class="ab-award-txt">
        <div class="eyebrow">Recognition</div>
        <span class="ab-award-y">2018</span>
        <h2 id="recTitle">Asianet Keerthimudra Award</h2>
        <p>Recognition for the founders’ entrepreneurial journey in the Electrical and Electronics sector.</p>
      </div>
    </div>
  </div>
</section>

<!-- ======= MILESTONES ======= -->
<section class="ab-time band" id="milestones">
  <div class="wrap">
    <div class="sec-head">
      <div><div class="eyebrow">Milestones</div><h2>Three decades of <em>progress</em></h2></div>
      <p>From a cable plant in Kanjikode to megawatt-scale solar. Scroll through the journey.</p>
    </div>
    <div class="tl-wrap">
      <span class="tl-line" aria-hidden="true"><i id="tlFill"></i></span>
      <ol class="tl" id="tl">
{tl}
      </ol>
    </div>
    <p class="tl-end">Our journey began with lighting the way. Today, we are helping power the future. <em>And the journey continues.</em></p>
  </div>
</section>

<!-- ======= VISION & MISSION ======= -->
<section class="ab-vm" id="vision">
  <div class="wrap">
    <div class="ab-vm-grid">
      <div class="ab-vm-item"><span class="ab-vm-k">Vision</span><p data-fill>To be at the forefront of renewable energy adoption, empowering businesses and communities with high-quality, reliable and innovative energy solutions that make sustainability both accessible and economically rewarding.</p></div>
      <div class="ab-vm-item"><span class="ab-vm-k">Mission</span><p data-fill>To be a trusted one-stop energy solutions partner for residential, commercial and industrial customers, delivering quality products, expert engineering, seamless execution and dependable service at every stage of their energy journey.</p></div>
    </div>
    <div class="ab-pr">
      <p class="ab-pr-intro">One philosophy, from 1996 to today</p>
      <ol>
        <li><span>01</span>Build with purpose</li>
        <li><span>02</span>Deliver with responsibility</li>
        <li><span>03</span>Keep progressing</li>
      </ol>
    </div>
  </div>
</section>

<!-- ======= MANUFACTURING & RECOGNITION ======= -->
<section class="ab-fac band" id="facilities">
  <div class="wrap">
    <div class="sec-head">
      <div><div class="eyebrow">Manufacturing</div><h2>Built on <em>real capability</em></h2></div>
      <p>The group’s manufacturing laid the foundation. Since 2024, Sinelab makes lithium batteries and integrated inverters in Kanjikode.</p>
    </div>
    <ol class="ab-sites">
{sites}
    </ol>
  </div>
</section>

<!-- ======= LEADERSHIP PREVIEW ======= -->
<section class="people band" id="ab-team">
  <div class="wrap">
    <div class="sec-head">
      <div><div class="eyebrow">Our people</div><h2>The people behind <em>the progress</em></h2></div>
      <p>Visionary founders. Experienced professionals. A new generation of leadership.</p>
    </div>
    {leaders}  </div>
</section>

<!-- ======= CALL TO ACTION ======= -->
<section class="ab-cta" id="cta">
  <div class="wrap">
    <div class="ab-cta-card">
      <div class="ab-cta-img" aria-hidden="true"><img src="{{{{L:cta_night.jpg}}}}" alt=""></div>
      <div class="ab-cta-copy">
        <span class="ab-cta-k">Start a project</span>
        <h2>Let’s power <em>your next move</em></h2>
        <p>Planning solar for your home, business or plant? Our team is here to help.</p>
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

CSS = '''
/* ================= About page ================= */
.ab-hero{position:relative;height:100svh;min-height:620px;background:var(--navy-deep);color:#fff;overflow:hidden;isolation:isolate;display:flex;align-items:flex-end}
.ab-hero-bg{position:absolute;inset:0;z-index:-1}
.ab-hero-img{width:100%;height:100%;object-fit:cover}
.ab-hero-bg::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(9,9,11,.88) 0%,rgba(9,9,11,.55) 48%,rgba(9,9,11,.12) 100%),linear-gradient(0deg,rgba(9,9,11,.75) 0%,rgba(9,9,11,0) 45%)}
.ab-ph{top:auto;bottom:24px;right:24px}
.ab-hero-copy{width:100%;padding-bottom:clamp(56px,9vh,110px)}
.ab-crumb{display:flex;gap:10px;align-items:center;font:500 12px var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.75)}
.ab-crumb a{display:inline-block;padding-block:5px;color:inherit;text-decoration:none}   /* 24px target */.ab-crumb a:hover{color:#fff;text-decoration:underline;text-decoration-color:var(--sun);text-underline-offset:4px}
.ab-h1{margin:22px 0 0;font-size:clamp(38px,5vw,76px);font-weight:300;line-height:.98;letter-spacing:-0.05em;color:#fff}
.ab-h1 .ln{display:block;overflow:hidden;padding-bottom:.16em;margin-bottom:-.1em}   /* room for g, y and p descenders inside the mask */
.ab-h1 .ln>span{display:block}
.ab-h1 em{font-style:normal;font-weight:600;color:var(--sun)}
.ab-since{display:flex;gap:22px;margin:30px 0 0;font:500 12px var(--f-mono);letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.75)}
.ab-since span+span::before{content:"";display:inline-block;width:5px;height:5px;margin:0 22px 2px 0;border-radius:50%;background:var(--sun);vertical-align:middle}
.ab-cue{position:absolute;right:clamp(16px,4vw,48px);bottom:clamp(56px,9vh,110px);display:flex;flex-direction:column;align-items:center;gap:12px;font:500 11px var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.75)}
.ab-cue i{display:block;width:1px;height:56px;background:linear-gradient(rgba(255,255,255,.7),rgba(255,255,255,0));animation:cue 2.2s ease-in-out infinite;transform-origin:top}
@keyframes cue{0%{transform:scaleY(0)}50%{transform:scaleY(1)}100%{transform:scaleY(1);opacity:0}}
/* entrance: the first line rises on load; on desktop the next two arrive as you scroll (JS), on phones they follow on load */
.ab-crumb,.ab-since{opacity:0;transform:translateY(16px);transition:opacity .9s ease,transform 1.1s cubic-bezier(.2,.7,.2,1)}
.ab-h1 .ln>span{transform:translateY(105%);transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}
.ab-hero.in .ab-crumb,.ab-hero.in .ab-since{opacity:1;transform:none}
.ab-hero.in .ab-h1 .ln:nth-child(1)>span{transform:none;transition-delay:.1s}
.ab-hero.in .ab-h1 .ln:nth-child(2)>span{transform:none;transition-delay:.45s}
.ab-hero.in .ab-since{transition-delay:.75s}

.ab-story{padding-block:clamp(90px,11vw,160px)}
.ab-story-in{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:clamp(40px,7vw,120px);align-items:center}
.ab-story-media{position:relative;margin:0;aspect-ratio:4/5;border-radius:18px;overflow:hidden;clip-path:inset(10% 12% 10% 0 round 18px);transition:clip-path 1.4s cubic-bezier(.2,.7,.2,1)}
.ab-story-media img{width:100%;height:100%;object-fit:cover;transform:scale(1.12);transition:transform 1.8s cubic-bezier(.2,.7,.2,1)}
.ab-story-media.open{clip-path:inset(0 0 0 0 round 18px)}
.ab-story-media.open img{transform:none}
.ab-story-body h2{margin-top:14px;font-size:clamp(32px,3.9vw,56px);color:var(--navy)}
.ab-pull{margin:clamp(28px,3vw,40px) 0 0;font-size:clamp(24px,2.4vw,34px);font-weight:300;line-height:1.3;letter-spacing:-0.025em;color:var(--ink)}
.ab-story-p{margin:26px 0 0;max-width:52ch;font-size:clamp(16.5px,1.2vw,18px);line-height:1.7;color:var(--muted)}
.ab-stats{position:relative;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));margin:clamp(70px,8vw,120px) 0 0;border-top:1px solid var(--line)}
.ab-stats::before{content:"";position:absolute;left:0;top:-1px;height:2px;width:0;background:var(--sun);transition:width 1.6s cubic-bezier(.2,.7,.2,1)}
.ab-stats.in::before{width:100%}
.ab-stats>div{display:flex;flex-direction:column-reverse;justify-content:flex-end;padding:26px 24px 0 0;opacity:0;transform:translateY(18px);transition:opacity .8s ease,transform 1s cubic-bezier(.2,.7,.2,1)}
.ab-stats.in>div{opacity:1;transform:none}
.ab-stats.in>div:nth-child(2){transition-delay:.12s}.ab-stats.in>div:nth-child(3){transition-delay:.24s}.ab-stats.in>div:nth-child(4){transition-delay:.36s}
.ab-stats dd{margin:0;font:300 clamp(40px,4.6vw,68px)/1 var(--f-display);letter-spacing:-0.045em;color:var(--ink)}
.ab-stats dd small{margin-left:8px;font-size:.32em;letter-spacing:0;color:var(--muted)}
.ab-stats dt{margin-top:12px;max-width:24ch;font-size:14px;line-height:1.45;color:var(--muted)}
/* words fill in as you read (quote, vision, mission) */
[data-fill] .w{transition:color .25s linear}
.ab-pull[data-fill] .w{color:#8A8A93}
.ab-pull[data-fill] .w.on{color:var(--ink)}
.ab-vm [data-fill] .w{color:rgba(255,255,255,.5)}
.ab-vm [data-fill] .w.on{color:#fff}

.ab-time{background:var(--paper);padding-block:clamp(90px,11vw,160px)}
.tl-wrap{position:relative;margin-top:clamp(30px,4vw,60px)}
.tl-line{position:absolute;left:50%;top:0;bottom:0;width:2px;margin-left:-1px;background:#DCDCE0;border-radius:2px;overflow:hidden}
.tl-line i{position:absolute;inset:0;background:var(--sun);transform-origin:50% 0;transform:scaleY(0)}
.tl{list-style:none;margin:0;padding:0}
.tl-item{position:relative;display:grid;grid-template-columns:minmax(0,1fr) 64px minmax(0,1fr);align-items:center;padding:clamp(26px,3.2vw,44px) 0}
.tl-year{font:300 clamp(40px,4.6vw,72px)/.9 var(--f-display);letter-spacing:-0.05em;color:#8A8A93;transition:color .6s ease}
.tl-dot{grid-column:2;justify-self:center;width:15px;height:15px;border-radius:50%;background:var(--paper);border:2px solid #B9B9C0;transition:background .5s,border-color .5s,box-shadow .5s;z-index:1}
.tl-body h3{margin:0;font-size:clamp(20px,1.8vw,26px);font-weight:500;letter-spacing:-0.02em;color:#3F3F46;transition:color .5s}
.tl-body p{margin:8px 0 0;max-width:40ch;font-size:16px;line-height:1.6;color:var(--muted)}
.tl-body{transition:transform .9s cubic-bezier(.2,.7,.2,1)}
.tl-item:nth-child(odd) .tl-year{grid-column:1;grid-row:1;justify-self:end;text-align:right}
.tl-item:nth-child(odd) .tl-body{grid-column:3;grid-row:1}
.tl-item:nth-child(even) .tl-year{grid-column:3;grid-row:1}
.tl-item:nth-child(even) .tl-body{grid-column:1;grid-row:1;justify-self:end;text-align:right}
.tl-item:nth-child(even) .tl-body p{margin-left:auto}
.tl-item.on .tl-year{color:var(--ink)}
.tl-item.on .tl-dot{background:var(--sun);border-color:var(--sun);box-shadow:0 0 0 6px rgba(249,194,46,.22)}
.tl-item.on .tl-body h3{color:var(--ink)}
.tl-end{margin:clamp(40px,5vw,72px) auto 0;max-width:30ch;text-align:center;font-size:clamp(22px,2.2vw,32px);font-weight:300;line-height:1.3;letter-spacing:-0.025em;color:var(--ink)}
.tl-end em{font-style:normal;font-weight:600}

.ab-vm{background:var(--navy-deep);color:#fff;padding-block:clamp(90px,11vw,160px)}
.ab-vm-grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(30px,5vw,80px)}
.ab-vm-item{padding-top:24px;border-top:1px solid var(--line-dark)}
.ab-vm-k{display:block;font:500 12px var(--f-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--sun)}
.ab-vm-item p{margin:18px 0 0;font-size:clamp(21px,2vw,29px);font-weight:300;line-height:1.38;letter-spacing:-0.02em;color:#fff}
.ab-pr{margin-top:clamp(60px,8vw,110px)}
.ab-pr-intro{margin:0;font:500 12px var(--f-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--on-dark-muted)}
.ab-pr ol{list-style:none;margin:18px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(16px,2vw,28px)}
.ab-pr li{position:relative;padding:26px 0 0;border-top:1px solid var(--line-dark);font:300 clamp(26px,2.8vw,42px)/1.1 var(--f-display);letter-spacing:-0.035em;color:#fff}
.ab-pr li::before{content:"";position:absolute;left:0;top:-1px;height:2px;width:0;background:var(--sun);transition:width 1.1s cubic-bezier(.2,.7,.2,1)}
.ab-pr.in li::before{width:100%}
.ab-pr.in li:nth-child(2)::before{transition-delay:.18s}.ab-pr.in li:nth-child(3)::before{transition-delay:.36s}
.ab-pr li span{display:block;margin-bottom:14px;font:500 12px var(--f-mono);letter-spacing:.08em;color:var(--sun)}

.ab-fac{padding-block:clamp(90px,11vw,160px)}
.ab-sites{position:relative;list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px}
.ab-sites::before{content:"";position:absolute;left:24px;right:24px;top:58px;height:1px;background:var(--line)}
.ab-site{position:relative;display:flex;flex-direction:column;padding:22px 22px 24px;border-radius:16px;background:var(--paper);transition:transform .45s cubic-bezier(.2,.7,.2,1),background .3s,color .3s}
.ab-site:hover{transform:translateY(-4px)}
.ab-site-y{font:500 12px var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--accent-ink)}
.ab-site-dot{width:11px;height:11px;margin:16px 0 18px;border-radius:50%;background:var(--paper);border:2px solid #B9B9C0;position:relative;z-index:1}
.ab-site h3{margin:0;font-size:20px;font-weight:500;letter-spacing:-0.02em;line-height:1.2;color:var(--ink)}
.ab-site p{margin:8px 0 18px;font-size:15px;line-height:1.5;color:var(--muted)}
.ab-site-tag{margin-top:auto;align-self:flex-start;padding:5px 10px;border-radius:999px;background:#fff;font:500 11.5px var(--f-mono);letter-spacing:.04em;color:var(--ink)}
.ab-site.hi{background:var(--navy-deep);color:#fff}
.ab-site.hi h3{color:#fff}.ab-site.hi p{color:var(--on-dark-muted)}.ab-site.hi .ab-site-y{color:var(--sun)}
.ab-site.hi .ab-site-dot{background:var(--sun);border-color:var(--sun);box-shadow:0 0 0 5px rgba(249,194,46,.2)}
.ab-site.hi .ab-site-tag{background:var(--sun);color:var(--ink)}
.ab-rec{position:relative;isolation:isolate;margin-top:calc(-1 * clamp(50px,7vw,100px));padding-block:clamp(36px,4vw,56px) clamp(90px,11vw,150px)}
.rec-bg{position:absolute;inset:0;z-index:-1;pointer-events:none;overflow:hidden;
  background:radial-gradient(42% 60% at 28% 48%,rgba(249,194,46,.16),transparent 70%),radial-gradient(rgba(9,9,11,.09) 1px,transparent 1.4px) 0 0/22px 22px;
  -webkit-mask:radial-gradient(75% 85% at 50% 50%,#000 45%,transparent 100%);mask:radial-gradient(75% 85% at 50% 50%,#000 45%,transparent 100%)}
.rec-bg .floaters{z-index:0}
.rec-bg .fl.y{color:var(--sun)}
.ab-award{position:relative;isolation:isolate;overflow:hidden;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(24px,4vw,64px);align-items:center;padding:clamp(14px,1.4vw,18px);border-radius:24px;background:radial-gradient(60% 90% at 22% 50%,#1C1F2B,#0E0F15 70%);box-shadow:0 40px 90px -40px rgba(9,9,11,.55)}
.rec-num{position:absolute;z-index:-1;right:-.04em;bottom:-.2em;font:600 clamp(150px,19vw,290px)/1 var(--f-display);letter-spacing:-0.06em;color:transparent;-webkit-text-stroke:1.5px rgba(255,255,255,.07);pointer-events:none;user-select:none}
.ab-award-ph{position:relative;aspect-ratio:4/3;border-radius:16px;background:radial-gradient(70% 70% at 50% 50%,rgba(249,194,46,.14),rgba(255,255,255,.02) 70%);border:1px solid rgba(255,255,255,.08);display:grid;place-items:center;overflow:hidden}
.rec-emblem{width:92%;height:auto}
.rec-rays{transform-origin:200px 160px;animation:recSpin 60s linear infinite}
.rec-sparks path{transform-box:fill-box;transform-origin:center;animation:recTw 3.2s ease-in-out infinite alternate}
.rec-sparks path:nth-child(2){animation-delay:-1.1s}.rec-sparks path:nth-child(3){animation-delay:-2s}.rec-sparks path:nth-child(4){animation-delay:-.5s}
@keyframes recSpin{to{transform:rotate(360deg)}}
@keyframes recTw{from{opacity:.35}to{opacity:1}}
.ab-award-ph .ph-note{position:absolute;left:14px;top:14px;font:500 10.5px var(--f-mono);letter-spacing:.05em;text-transform:uppercase;color:rgba(255,255,255,.72)}
.ab-award-txt{position:relative;padding-block:clamp(10px,2vw,28px)}
.ab-award-txt .eyebrow{margin-bottom:14px;color:rgba(255,255,255,.78)}
.ab-award-y{display:inline-block;padding:5px 10px;border-radius:999px;background:var(--sun);font:600 12px var(--f-mono);letter-spacing:.08em;color:var(--ink)}
.ab-award-txt h2{margin:14px 0 0;font-size:clamp(28px,3vw,44px);font-weight:300;letter-spacing:-0.035em;line-height:1.08;color:#fff}
.ab-award-txt p{margin:14px 0 0;max-width:44ch;font-size:17px;line-height:1.6;color:rgba(255,255,255,.76)}
@media (prefers-reduced-motion: reduce){.rec-rays,.rec-sparks path{animation:none}}

.ab-cta{padding-block:clamp(70px,8vw,120px) clamp(80px,9vw,140px)}
.ab-cta-card{position:relative;isolation:isolate;overflow:hidden;border-radius:28px;background:var(--navy-deep);color:#fff;min-height:clamp(420px,40vw,540px);display:grid;grid-template-rows:1fr auto;padding:clamp(28px,4.5vw,64px)}
.ab-cta-img{position:absolute;inset:0 0 0 30%;z-index:-1}
.ab-cta-img img{width:100%;height:100%;object-fit:cover;object-position:60% 55%;filter:brightness(1.45) saturate(1.1);transform:scale(1.08);transition:transform 2.2s cubic-bezier(.2,.7,.2,1)}
.ab-cta-card.in .ab-cta-img img{transform:none}
.ab-cta-img::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,var(--navy-deep) 0%,rgba(9,9,11,.7) 28%,rgba(9,9,11,0) 62%),linear-gradient(0deg,rgba(9,9,11,.8) 0%,rgba(9,9,11,0) 38%)}
.ab-cta-copy{align-self:center;max-width:560px}
.ab-cta-k{font:500 12px var(--f-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--sun)}
.ab-cta h2{margin-top:16px;font-size:clamp(36px,4.6vw,68px);font-weight:300;line-height:1.02;letter-spacing:-0.045em;color:#fff}
.ab-cta h2 em{font-style:normal;font-weight:600;color:var(--sun)}
.ab-cta-copy p{margin:18px 0 0;max-width:38ch;font-size:clamp(16.5px,1.25vw,19px);line-height:1.55;color:rgba(255,255,255,.8)}
.ab-cta-btns{display:flex;gap:12px;flex-wrap:wrap;margin-top:30px}
.ab-btn-ghost{border-color:rgba(255,255,255,.55);color:#fff;background:rgba(255,255,255,.04);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.ab-btn-ghost:hover{border-color:#fff;background:rgba(255,255,255,.1)}
.ab-cta-meta{display:flex;flex-wrap:wrap;gap:clamp(20px,4vw,56px);margin:clamp(36px,4vw,56px) 0 0;padding-top:22px;border-top:1px solid rgba(255,255,255,.14)}
.ab-cta-meta dt{font:500 11px var(--f-mono);letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.7)}
.ab-cta-meta dd{margin:6px 0 0;font-size:15px;color:#fff}
.ab-cta-meta a{display:inline-block;padding-block:3px;color:inherit;text-decoration:none}.ab-cta-meta a:hover{text-decoration:underline;text-decoration-color:var(--sun);text-underline-offset:4px}

/* About: team – two co-founders large, then four equal cards */
.tm{display:grid;gap:clamp(36px,4vw,56px)}
.tm-founders{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(14px,1.6vw,22px)}
.tm-team{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:clamp(16px,1.6vw,24px)}
.tm-team .tm-card h3{font-size:clamp(17px,1.35vw,20px)}
.tm-team .tm-bio{font-size:14.5px}
.tm-card{position:relative;min-width:0}
.tm-ph{position:relative;display:grid;place-items:end center;aspect-ratio:1/1;border-radius:18px;overflow:hidden;background:linear-gradient(170deg,#EFEFF2,#CDCDD3);color:#A7A7AF}
.tm-ph svg{width:62%;margin-bottom:-7%;transition:transform 1s cubic-bezier(.2,.7,.2,1)}
.tm-card:hover .tm-ph svg{transform:translateY(-4px) scale(1.03)}
.tm-ph .ab-ld-tag{right:12px;top:12px}
.tm-ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 30%;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}
.tm-card:hover .tm-ph img{transform:scale(1.04)}
.tm-ph.has-img::after{content:"";position:absolute;inset:0;border-radius:inherit;box-shadow:inset 0 0 0 1px rgba(9,9,11,.08);pointer-events:none}
.tm-body{padding:18px 2px 0}
.tm-card h3{margin:0;font-size:clamp(19px,1.5vw,22px);font-weight:500;letter-spacing:-0.015em;line-height:1.2;color:var(--ink)}
.tm-role{margin:6px 0 0;font:500 12.5px var(--f-mono);letter-spacing:.04em;text-transform:uppercase;color:var(--accent-ink)}
.tm-div{display:block;margin-top:3px;color:var(--muted)}
.tm-role.tbc{text-transform:none;letter-spacing:0;font-family:var(--f-body);font-size:14px;font-style:italic;color:var(--muted)}
.tm-bio{margin:12px 0 0;padding-top:12px;border-top:1px solid var(--line);font-size:15px;line-height:1.6;color:var(--muted)}
.tm-lg{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1fr);border-radius:22px;background:var(--paper);overflow:hidden}
.tm-lg .tm-ph{aspect-ratio:auto;min-height:clamp(300px,26vw,380px);border-radius:0}
.tm-lg .tm-ph img{object-position:50% 12%}
.tm-lg .tm-body{display:flex;flex-direction:column;justify-content:flex-end;padding:clamp(22px,2.4vw,34px)}
.tm-lg h3{font-size:clamp(24px,2.1vw,32px);font-weight:400;letter-spacing:-0.03em}
.tm-lg .tm-bio{font-size:15.5px}
@media (max-width:1100px){
  .tm-founders{grid-template-columns:1fr}
  .tm-team{grid-template-columns:repeat(3,minmax(0,1fr));row-gap:34px}
}
@media (max-width:820px){
  /* the other four become a compact list: small photo beside name, role and bio */
  .tm-team{grid-template-columns:repeat(2,minmax(0,1fr));column-gap:28px;row-gap:0}
  .tm-team .tm-card{display:grid;grid-template-columns:88px minmax(0,1fr);column-gap:16px;align-items:start;padding:18px 0;border-top:1px solid var(--line)}
  .tm-team .tm-ph{border-radius:14px}
  .tm-team .tm-ph .ab-ld-tag{display:none}
  .tm-team .tm-body{padding:0}
}
@media (max-width:600px){
  /* phones (user asked for vertical cards): founders photo-on-top; the other four as a simple list */
  .tm-lg{grid-template-columns:1fr}
  .tm-lg .tm-ph{min-height:0;height:min(320px,86vw)}
  .tm-lg .tm-body{padding:20px 20px 22px}
  .tm-team{grid-template-columns:1fr}
  .tm-team .tm-card:last-child{border-bottom:1px solid var(--line)}
}
@media (prefers-reduced-motion: reduce){.tm-ph svg,.tm-ph img{transition:none}.tm-card:hover .tm-ph svg,.tm-card:hover .tm-ph img{transform:none}}
/* (older single-row styles below no longer match anything) */
.ab-leaders .leader.open{flex-grow:1.9}
.ab-leaders{gap:12px}
.ab-leaders .ld-role.tbc{font-style:italic;opacity:.85}
.ab-ld-tag{position:absolute;z-index:2;right:14px;top:14px;padding:4px 10px;border-radius:999px;background:rgba(9,9,11,.6);border:1px solid rgba(255,255,255,.25);font:500 10.5px var(--f-mono);letter-spacing:.06em;text-transform:uppercase;color:#fff;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.ab-leaders .ld-msg p{max-width:42ch}
.ab-leaders .leader h3{white-space:normal;overflow:visible;font-size:clamp(16px,1.35vw,20px)}
.ab-leaders .ld-ph .ph-note{display:none}

@media (max-width:1100px){
  .ab-leaders{display:grid;grid-template-columns:1fr 1fr;height:auto;gap:14px}
  .ab-leaders .leader,.ab-leaders .leader.open{height:440px}
  .ab-leaders .ld-msg{max-height:none;opacity:1;transform:none;margin-bottom:14px}
  .ab-leaders .leader::after{height:82%;background:linear-gradient(180deg,rgba(9,9,11,0) 0%,rgba(9,9,11,.7) 34%,rgba(9,9,11,.94) 100%)}
  .ab-cta-img{inset:0}
  .ab-sites{grid-template-columns:repeat(3,minmax(0,1fr))}
  .ab-sites::before{display:none}
}
@media (max-width:900px){
  .ab-hero{height:88svh;min-height:560px}
  .ab-cue{display:none}
  .ab-since{flex-wrap:wrap;gap:12px}
  .ab-since span+span::before{margin-right:12px}
  .ab-stats{grid-template-columns:1fr 1fr;row-gap:12px}
  .ab-story-in{grid-template-columns:1fr;gap:34px}
  .ab-story-media{aspect-ratio:4/3}
  .tl-line{left:7px;margin-left:0}
  .tl-item,.tl-item:nth-child(even),.tl-item:nth-child(odd){grid-template-columns:16px minmax(0,1fr);column-gap:20px;row-gap:6px;padding:22px 0;align-items:start}
  .tl-item .tl-dot{grid-column:1;grid-row:1;align-self:center;margin-left:0;justify-self:start}
  .tl-item:nth-child(odd) .tl-year,.tl-item:nth-child(even) .tl-year{grid-column:2;grid-row:1;justify-self:start;text-align:left;font-size:38px}
  .tl-item:nth-child(odd) .tl-body,.tl-item:nth-child(even) .tl-body{grid-column:2;grid-row:2;justify-self:start;text-align:left}
  .tl-item:nth-child(even) .tl-body p{margin-left:0}
  .ab-vm-grid{grid-template-columns:1fr}
  .ab-pr ol{grid-template-columns:1fr}
  .ab-award{grid-template-columns:1fr}
  .rec-num{font-size:clamp(120px,34vw,180px)}
}
@media (max-width:700px){
  /* phones (user): the four leaders stack as vertical cards – photo on top, then name, role and bio */
  .ab-leaders{display:grid;grid-template-columns:1fr;gap:14px;height:auto;margin-inline:0;padding-inline:0;overflow:visible;scroll-snap-type:none}
  .ab-leaders .leader,.ab-leaders .leader.open{display:flex;flex-direction:column;flex:none;height:auto;background:var(--navy-deep)}
  .ab-leaders .leader::after,.ab-leaders .leader.open::after{display:none}
  .ab-leaders .ld-ph{position:relative;inset:auto;flex:none;height:200px}
  .ab-leaders .ld-ph svg{width:44%}
  .ab-leaders .ld-txt{position:relative;inset:auto;display:flex;flex-direction:column;padding:18px 18px 20px;text-shadow:none}
  .ab-leaders .leader h3{order:1;font-size:18px;white-space:normal}
  .ab-leaders .ld-role{order:2}
  .ab-leaders .ld-msg,.ab-leaders .leader.open .ld-msg{order:3;margin:14px 0 0;padding-top:14px;border-top:1px solid rgba(255,255,255,.14)}
  .ab-leaders .ld-msg p{font-size:15px;line-height:1.55;max-width:none}
}
@media (max-width:600px){
  .ab-sites{grid-template-columns:1fr}
  .ab-site{display:grid;grid-template-columns:minmax(0,1fr) auto;column-gap:14px}
  .ab-site-dot{display:none}
  .ab-site-y{grid-column:1/-1}
  .ab-site h3{margin-top:8px}
  .ab-site p{grid-column:1/-1;margin-bottom:12px}
  .ab-site-tag{grid-column:1/-1}
  .ab-cta-btns .btn{width:100%;justify-content:center}
  .ab-cta-card{border-radius:20px}
  .ab-cta-meta{flex-direction:column;gap:14px}
}
@media (prefers-reduced-motion: reduce){
  .ab-crumb,.ab-since,.ab-h1 .ln>span,.ab-stats>div,.tl-body{opacity:1;transform:none!important;transition:none}
  .ab-hero-img,.ab-story-media img{transform:none!important;transition:none}
  .ab-story-media{clip-path:inset(0 0 0 0 round 18px);transition:none}
  .ab-stats::before{width:100%;transition:none}
  .tl-line i{transform:none}
}
'''
head = head[:head.rindex('</style>')] + CSS + head[head.rindex('</style>'):]

JS = r'''/* ---------- Arriving from the homepage's "Meet the full team" (about.html#ab-team): land with the heading just below the nav ---------- */
(function(){
  if (location.hash !== '#ab-team') return;
  const t = document.querySelector('#ab-team .sec-head'); if (!t) return;
  const go = () => { const y = Math.max(0, t.getBoundingClientRect().top + scrollY - 100); if (lenis) lenis.scrollTo(y, { immediate:true, force:true }); else scrollTo(0, y); };
  addEventListener('load', () => setTimeout(go, 80));
})();

/* ---------- About hero: static photo; the two headline lines rise in one after the other on load ---------- */
(function(){ const h = document.getElementById('ab-hero'); if (!h) return; requestAnimationFrame(() => setTimeout(() => h.classList.add('in'), 60)); })();

/* ---------- Story: the photo opens up and the numbers rise in when they come into view ---------- */
(function(){
  const els = [document.querySelector('.ab-story-media'), document.getElementById('abStats')].filter(Boolean);
  if (reduce || !('IntersectionObserver' in window)){ els.forEach(e => e.classList.add(e.id ? 'in' : 'open')); return; }
  els.forEach(e => { const io = new IntersectionObserver(es => { if (es[0].isIntersecting){ e.classList.add(e.id ? 'in' : 'open'); io.disconnect(); } }, { rootMargin:'0px 0px -18% 0px' }); io.observe(e); });
})();

/* ---------- Quote, vision and mission: words fill in as you scroll through them ---------- */
(function(){
  const blocks = [...document.querySelectorAll('[data-fill]')]; if (!blocks.length) return;
  blocks.forEach(b => {
    const words = b.textContent.trim().split(/\s+/);
    const keep = b.querySelector('svg');
    b.innerHTML = (keep ? keep.outerHTML : '') + words.map(w => '<span class="w">' + w + '</span>').join(' ');
  });
  if (reduce){ blocks.forEach(b => b.querySelectorAll('.w').forEach(w => w.classList.add('on'))); return; }
  let queued = false;
  const update = () => {
    queued = false;
    blocks.forEach(b => {
      const r = b.getBoundingClientRect(), start = innerHeight * .88, end = innerHeight * .42;
      const p = Math.min(1, Math.max(0, (start - r.top) / (start - end + r.height * .6)));
      const ws = b.querySelectorAll('.w'), n = Math.round(p * ws.length);
      ws.forEach((w, k) => w.classList.toggle('on', k < n));
    });
  };
  addEventListener('scroll', () => { if (!queued){ queued = true; requestAnimationFrame(update); } }, { passive:true });
  addEventListener('resize', update); update();
})();

/* ---------- Milestones: the yellow line fills as you scroll; each year lights up as it passes the middle ---------- */
(function(){
  const tl = document.getElementById('tl'), fill = document.getElementById('tlFill'); if (!tl || !fill) return;
  const items = [...tl.querySelectorAll('.tl-item')];
  if (reduce){ items.forEach(li => li.classList.add('on')); return; }
  let queued = false;
  const update = () => {
    queued = false;
    const r = tl.getBoundingClientRect(), mid = innerHeight * .55;
    const p = Math.min(1, Math.max(0, (mid - r.top) / r.height));
    fill.style.transform = 'scaleY(' + p.toFixed(4) + ')';
    items.forEach(li => { const b = li.getBoundingClientRect(); li.classList.toggle('on', b.top + b.height / 2 < mid); });
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

/* ---------- Principles: the yellow rules draw across when they come into view ---------- */
(function(){
  const pr = document.querySelector('.ab-pr'); if (!pr) return;
  if (reduce || !('IntersectionObserver' in window)) { pr.classList.add('in'); return; }
  const io = new IntersectionObserver(es => { if (es[0].isIntersecting){ pr.classList.add('in'); io.disconnect(); } }, { rootMargin:'0px 0px -20% 0px' }); io.observe(pr);
})();

'''
script = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>\n'
          '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>\n'
          '<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>\n<script>\n'
          + js_core + js_nav + js_reveal + JS + '})();\n</script>\n')
src = (head + body + script).replace('index.html#contact', 'contact.html')   # the Contact page now exists
open(d + 'about_src.html', 'w').write(src)

# ---------- build: inline images, write a full document (it is a second page of the artifact) ----------
mime = {'png':'image/png','jpg':'image/jpeg','webp':'image/webp'}
import sys; sys.path.insert(0, d); from webp_cache import webp   # all images as WebP
def uri(path): path = webp(path); return 'data:' + mime[path.rsplit('.',1)[1]] + ';base64,' + base64.b64encode(open(path,'rb').read()).decode()
out = re.sub(r'\{\{L:([^}]+)\}\}', lambda m: uri(d + 'layers/' + m.group(1)), src)
out = out.replace('{{LOGO_BLACK}}', uri(d + 'logo_black.png')).replace('{{LOGO_WHITE}}', uri(d + 'logo_white.png'))
assert '{{' not in out, re.findall(r'\{\{[^}]+\}\}', out)[:3]
hi = out.index('<!-- ======= NAV ======= -->')
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
       + out[:hi] + '</head>\n<body>\n' + out[hi:] + '</body>\n</html>\n')
open(d + 'about.html', 'w').write(doc)
print('about.html', len(doc) // 1024, 'KB')
