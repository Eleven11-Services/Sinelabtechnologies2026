# Contact page: quick contact tiles, the enquiry form (content-doc spec), and the two offices with map spots.
# Shares the homepage stylesheet, nav, footer and scripts (from src_draft.html) and the About page styles (from about.py).
import re, base64, math, random
d = '/tmp/claude-0/site/'
home = open(d + 'src_draft.html').read()
about_py = open(d + 'about.py').read()
ABOUT_CSS = about_py[about_py.index("CSS = '''") + 9:about_py.index("'''\nhead = head[:head.rindex")]
def cut(a, b, src=home):
    i = src.index(a); j = src.index(b, i + len(a)); return src[i:j]
def rp(s, a, b):
    assert a in s, a[:80]; return s.replace(a, b)

ARR = '<svg class="arr" width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 9h10M10 5l4 4-4 4"/></svg>'
LINKS = [('#team', 'index.html#team'), ('#blog', 'index.html#blog'), ('#top', 'index.html')]
def relink(html):
    for a, b in LINKS: html = html.replace(f'href="{a}"', f'href="{b}"')
    return html

head = home[:home.index('<!-- ======= NAV ======= -->')]
head = head.replace('<title>Sinelab Website</title>', '<title>Contact | Sinelab Technologies</title>')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Contact Sinelab Technologies in Palakkad and Kochi, Kerala. Call or WhatsApp +91 99462 07738, email info@sinelabtechnologies.com, or send an enquiry for a free quote.">', head)
nav = relink(cut('<!-- ======= NAV ======= -->', '<main id="top">'))
nav = rp(nav, '<a href="contact.html">Contact</a>', '<a href="contact.html" aria-current="page">Contact</a>')
nav = rp(nav, '<a href="contact.html" style="--i:4">Contact', '<a href="contact.html" style="--i:4" aria-current="page">Contact')
foot = relink(home[home.index('<footer'):home.index('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js">')])
foot = foot.replace('href="contact.html#offices"', 'href="#offices"')

js_core = cut('(function(){\nconst reduce', '/* ---------- Solar panel model')
js_nav = cut('/* ---------- Floating glass nav: compact', '/* ---------- Why Sinelab: the reason nearest')
js_nav = rp(js_nav, "['#anatomy','#films','#savings','#faq','footer']", "['#ct-hero','footer']")
js_nav = rp(js_nav, "['#why','#solutions','#projects','#gallery','#faq','#blog','#contact']", "['#enquiry']")

# ---------- icons ----------
I_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>'
I_WA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.2A9.8 9.8 0 0 0 3.6 17l-1.4 5 5.2-1.4A9.8 9.8 0 1 0 12 2.2zm0 17.9a8.1 8.1 0 0 1-4.1-1.1l-.3-.2-3.1.8.8-3-.2-.3A8.1 8.1 0 1 1 12 20.1zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.4-.3z"/></svg>'
I_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5 12 13l8.5-6.5"/></svg>'
I_HOME = '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" aria-hidden="true"><path d="M4 15 16 5l12 10"/><path d="M7 13v13h18V13"/><path d="M11 19h10l-2 4h-10z"/></svg>'
I_BIZ = '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" aria-hidden="true"><path d="M4 27V13l7 4.5V13l7 4.5V13l7 4.5V5h3v22z"/><path d="M4 27h24"/></svg>'
I_HYB = '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" aria-hidden="true"><path d="M3 16l3-7h10l-3 7z"/><path d="M8 16v4"/><rect x="17" y="17" width="12" height="9" rx="1.5"/><path d="M29 20v3M23 19l-1.5 2.5h3L23 24"/></svg>'
I_OTHER = '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><path d="M16 4v24M4 16h24"/><circle cx="16" cy="16" r="11"/></svg>'

QUICK = [('tel:+919946207738', I_PHONE, 'Call us', '+91 99462 07738', 'Talk to the team'),
         ('https://wa.me/919946207738', I_WA, 'WhatsApp', '+91 99462 07738', 'Message us any time'),
         ('mailto:info@sinelabtechnologies.com', I_MAIL, 'Email', 'info@sinelabtechnologies.com', 'Send details or bills')]
quick = '\n'.join(f'''        <a class="qc" href="{h}"{' target="_blank" rel="noopener"' if h.startswith('http') else ''}>
          <span class="qc-ico">{ic}</span>
          <span class="qc-txt"><span class="qc-k">{k}</span><b>{v}</b><span class="qc-d">{dsc}{' (opens WhatsApp)' if h.startswith('http') else ''}</span></span>
          <span class="qc-go" aria-hidden="true">{ARR}</span>
        </a>''' for h, ic, k, v, dsc in QUICK)

INTEREST = [('Residential Solar', I_HOME, 'For your home'), ('Commercial & Industrial Solar', I_BIZ, 'Businesses and plants'),
            ('Hybrid Solar & Battery', I_HYB, 'Solar with backup'), ('Other Energy Solutions', I_OTHER, 'Lighting, consultancy, O&amp;M')]
radios = '\n'.join(f'''            <label class="it"><input type="radio" name="type" value="{v}"{" checked" if k == 0 else ""}><span class="it-box"><span class="it-ico">{ic}</span><b>{v.replace("&", "&amp;")}</b><small>{dsc}</small></span></label>'''
                   for k, (v, ic, dsc) in enumerate(INTEREST))

# ---------- stylised map spots (no real addresses yet) ----------
def mapsvg(seed, water):
    rnd = random.Random(seed); W, H = 640, 400
    roads = []
    for k in range(7):     # gently curving streets
        y0 = rnd.uniform(20, H - 20); y1 = y0 + rnd.uniform(-90, 90); c = (y0 + y1) / 2 + rnd.uniform(-60, 60)
        roads.append(f'<path class="mr" d="M-10 {y0:.0f} Q{W/2:.0f} {c:.0f} {W+10} {y1:.0f}"/>')
    for k in range(6):
        x0 = rnd.uniform(30, W - 30); x1 = x0 + rnd.uniform(-80, 80); c = (x0 + x1) / 2 + rnd.uniform(-50, 50)
        roads.append(f'<path class="mr{" ma" if k == 2 else ""}" d="M{x0:.0f} -10 Q{c:.0f} {H/2:.0f} {x1:.0f} {H+10}"/>')
    blocks = ''.join(f'<rect class="mb" x="{rnd.uniform(0, W):.0f}" y="{rnd.uniform(0, H):.0f}" width="{rnd.uniform(26, 70):.0f}" height="{rnd.uniform(18, 50):.0f}" rx="4"/>' for _ in range(16))
    wat = ('<path class="mw" d="M-10 300 C120 250 210 330 330 290 S520 230 650 280 L650 410 L-10 410Z"/>' if water else
           '<path class="mw" d="M-10 70 C90 110 160 40 260 80 S430 140 520 90 650 60 650 60 L650 30 C540 40 450 110 360 100 S200 10 -10 40Z"/>')
    return (f'<svg class="map-svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false">'
            f'<rect width="{W}" height="{H}" class="mbg"/>{wat}{blocks}{"".join(roads)}</svg>')
I_PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-7.2 7-12.5A7 7 0 0 0 5 9.5C5 14.8 12 22 12 22z"/><circle cx="12" cy="9.5" r="2.5"/></svg>'
PIN = '<svg class="pin" viewBox="0 0 36 48" aria-hidden="true"><path d="M18 2C9.2 2 2 9 2 17.6 2 29.4 18 46 18 46s16-16.6 16-28.4C34 9 26.8 2 18 2z"/><circle cx="18" cy="17.5" r="6"/></svg>'
OFFICES = [('Palakkad', 'Sinelab Technologies Pvt Ltd', 'Prathiba Nagar, Chandranagar Colony,<br>Palakkad, Kerala 678007',
             'Sinelab Technologies Pvt Ltd, Prathiba Nagar, Chandranagar Colony, Palakkad, Kerala 678007', 'ChIJDznElBNtqDsRwlGeDS40paQ',
             'Prathiba Nagar, Chandranagar Colony, Palakkad, Keralam 678007'),
            ('Kochi', 'Sinelab Solar', 'Mahakavi Vailoppilli Rd, Ponnurunni,<br>Vyttila, Kochi, Kerala 682032',
             'Sinelab Solar, Mahakavi Vailoppilli Rd, Ponnurunni, Vyttila, Kochi, Kerala 682032', 'ChIJcaY_7vENCDsRLxtGqYodVqE',
             'Mahakavi Vailoppilli Rd, Ponnurunni, Vyttila, Kochi, Ernakulam, Keralam 682032')]
from urllib.parse import quote_plus
def gembed(q): return 'https://maps.google.com/maps?q=' + quote_plus(q) + '&amp;z=16&amp;output=embed'
def gplace(name, pid): return 'https://www.google.com/maps/search/?api=1&amp;query=' + quote_plus(name) + '&amp;query_place_id=' + pid
def gdir(daddr, pid): return 'https://www.google.com/maps/dir/?api=1&amp;destination=' + quote_plus(daddr) + '&amp;destination_place_id=' + pid
I_CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
I_DIR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M12 2.5 21.5 12 12 21.5 2.5 12z"/><path d="M9 14v-3h5M12 8.5 14.5 11 12 13.5"/></svg>'
locs = '\n'.join(f'''          <article class="loc" data-k="{k}">
            <div class="loc-hd"><span class="loc-n">{k + 1:02d}</span><span class="loc-t"><span class="loc-k">{city} office</span><b>{name}</b></span><span class="loc-pin" aria-hidden="true">{I_PIN}</span></div>
            <p class="loc-addr">{addr}</p>
            <p class="loc-hrs">{I_CLOCK}Mon – Sat, 9:00 am – 5:30 pm</p>
            <div class="loc-links">
              <a class="btn btn-sun loc-go" href="{gdir(daddr, pid)}" target="_blank" rel="noopener">{I_DIR}Get directions<span class="sr-only"> to the {city} office (opens Google Maps in a new tab)</span></a>
            </div>
          </article>''' for k, (city, name, addr, q, pid, daddr) in enumerate(OFFICES))
KERALA = '<svg class="km" viewBox="0 0 1000 678" preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false"><defs><pattern id="kmDots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="#D9D9DE"/></pattern></defs><rect class="km-sea" width="1000" height="678"/><path class="km-land" d="M1166.7,-169.4 L1166.7,847.1 L430.5,847.1 L423.2,822.4 L411.2,743.3 L415.2,729.0 L403.2,644.1 L391.2,602.1 L387.2,596.4 L383.2,570.7 L381.2,563.0 L389.2,557.3 L399.2,564.0 L407.2,577.3 L411.2,587.8 L409.2,590.7 L395.2,586.9 L393.2,587.8 L393.2,595.5 L395.2,601.2 L399.2,606.9 L403.2,609.8 L405.2,605.9 L407.2,598.3 L411.2,605.9 L409.2,614.5 L407.2,622.2 L405.2,625.0 L411.2,625.0 L417.2,622.2 L419.2,617.4 L415.2,609.8 L421.2,604.0 L425.2,614.5 L439.2,706.1 L443.2,706.1 L443.2,690.8 L437.2,655.5 L443.2,640.3 L429.2,623.1 L427.2,614.5 L435.2,609.8 L437.2,617.4 L445.2,632.6 L449.2,640.3 L451.2,647.0 L449.2,659.3 L449.2,667.0 L455.2,697.5 L459.2,708.9 L469.2,717.5 L467.2,727.1 L465.2,734.7 L461.2,741.4 L457.2,749.0 L447.2,798.6 L449.2,807.2 L459.2,811.0 L487.2,815.7 L491.2,814.8 L505.2,820.5 L515.2,816.7 L529.2,799.5 L519.2,793.8 L509.2,787.1 L499.2,783.3 L487.2,787.1 L481.2,784.3 L475.2,779.5 L483.2,766.2 L483.2,753.8 L481.2,742.3 L481.2,715.6 L477.2,706.1 L473.2,700.4 L469.2,702.3 L467.2,696.5 L469.2,686.0 L469.2,679.4 L467.2,673.7 L463.2,664.1 L461.2,657.4 L463.2,647.9 L467.2,642.2 L471.2,636.5 L469.2,625.0 L465.2,614.5 L451.2,593.5 L449.2,584.0 L429.2,563.0 L423.2,555.4 L413.2,564.0 L405.2,548.7 L399.2,527.7 L401.2,516.3 L391.2,509.6 L385.2,479.1 L381.2,478.2 L377.2,474.3 L373.2,470.5 L369.2,458.1 L365.2,470.5 L369.2,481.0 L373.2,490.6 L377.2,499.1 L379.2,522.0 L381.2,533.5 L385.2,544.0 L377.2,536.3 L369.2,523.0 L351.2,477.2 L351.2,467.7 L353.2,460.0 L353.2,454.3 L349.2,448.6 L349.2,440.0 L375.2,425.7 L381.2,418.1 L381.2,414.3 L385.2,410.5 L385.2,405.7 L383.2,401.9 L381.2,401.9 L377.2,403.8 L373.2,403.8 L369.2,393.3 L365.2,388.5 L359.2,384.7 L365.2,403.8 L367.2,414.3 L361.2,423.8 L353.2,429.5 L345.2,426.7 L339.2,420.0 L335.2,412.4 L327.2,389.5 L317.2,342.7 L309.2,318.9 L289.2,292.2 L285.2,282.7 L285.2,271.2 L279.2,246.4 L275.2,237.8 L261.2,223.5 L255.2,215.9 L249.2,194.9 L215.2,126.3 L213.2,115.8 L213.2,112.0 L209.2,108.2 L207.2,104.3 L205.2,98.6 L207.2,95.8 L215.2,90.0 L217.2,87.2 L201.2,79.5 L191.2,56.7 L183.2,9.9 L157.2,-83.5 L121.5,-169.4Z"/><path class="km-dots" d="M1166.7,-169.4 L1166.7,847.1 L430.5,847.1 L423.2,822.4 L411.2,743.3 L415.2,729.0 L403.2,644.1 L391.2,602.1 L387.2,596.4 L383.2,570.7 L381.2,563.0 L389.2,557.3 L399.2,564.0 L407.2,577.3 L411.2,587.8 L409.2,590.7 L395.2,586.9 L393.2,587.8 L393.2,595.5 L395.2,601.2 L399.2,606.9 L403.2,609.8 L405.2,605.9 L407.2,598.3 L411.2,605.9 L409.2,614.5 L407.2,622.2 L405.2,625.0 L411.2,625.0 L417.2,622.2 L419.2,617.4 L415.2,609.8 L421.2,604.0 L425.2,614.5 L439.2,706.1 L443.2,706.1 L443.2,690.8 L437.2,655.5 L443.2,640.3 L429.2,623.1 L427.2,614.5 L435.2,609.8 L437.2,617.4 L445.2,632.6 L449.2,640.3 L451.2,647.0 L449.2,659.3 L449.2,667.0 L455.2,697.5 L459.2,708.9 L469.2,717.5 L467.2,727.1 L465.2,734.7 L461.2,741.4 L457.2,749.0 L447.2,798.6 L449.2,807.2 L459.2,811.0 L487.2,815.7 L491.2,814.8 L505.2,820.5 L515.2,816.7 L529.2,799.5 L519.2,793.8 L509.2,787.1 L499.2,783.3 L487.2,787.1 L481.2,784.3 L475.2,779.5 L483.2,766.2 L483.2,753.8 L481.2,742.3 L481.2,715.6 L477.2,706.1 L473.2,700.4 L469.2,702.3 L467.2,696.5 L469.2,686.0 L469.2,679.4 L467.2,673.7 L463.2,664.1 L461.2,657.4 L463.2,647.9 L467.2,642.2 L471.2,636.5 L469.2,625.0 L465.2,614.5 L451.2,593.5 L449.2,584.0 L429.2,563.0 L423.2,555.4 L413.2,564.0 L405.2,548.7 L399.2,527.7 L401.2,516.3 L391.2,509.6 L385.2,479.1 L381.2,478.2 L377.2,474.3 L373.2,470.5 L369.2,458.1 L365.2,470.5 L369.2,481.0 L373.2,490.6 L377.2,499.1 L379.2,522.0 L381.2,533.5 L385.2,544.0 L377.2,536.3 L369.2,523.0 L351.2,477.2 L351.2,467.7 L353.2,460.0 L353.2,454.3 L349.2,448.6 L349.2,440.0 L375.2,425.7 L381.2,418.1 L381.2,414.3 L385.2,410.5 L385.2,405.7 L383.2,401.9 L381.2,401.9 L377.2,403.8 L373.2,403.8 L369.2,393.3 L365.2,388.5 L359.2,384.7 L365.2,403.8 L367.2,414.3 L361.2,423.8 L353.2,429.5 L345.2,426.7 L339.2,420.0 L335.2,412.4 L327.2,389.5 L317.2,342.7 L309.2,318.9 L289.2,292.2 L285.2,282.7 L285.2,271.2 L279.2,246.4 L275.2,237.8 L261.2,223.5 L255.2,215.9 L249.2,194.9 L215.2,126.3 L213.2,115.8 L213.2,112.0 L209.2,108.2 L207.2,104.3 L205.2,98.6 L207.2,95.8 L215.2,90.0 L217.2,87.2 L201.2,79.5 L191.2,56.7 L183.2,9.9 L157.2,-83.5 L121.5,-169.4Z"/><text class="km-sea-l" x="70" y="420">Arabian Sea</text><polyline class="km-road-c" points="424.7,549.4 421.3,521.8 427.8,506.6 445.3,475.7 464.4,425.8 436.1,363.1 405.6,310.6 400.0,237.2 461.1,214.6 515.7,201.8 548.9,170.6 575.0,144.0 625.6,103.9 666.7,84.7 716.7,62.1 777.8,11.3"/><polyline class="km-road" points="424.7,549.4 421.3,521.8 427.8,506.6 445.3,475.7 464.4,425.8 436.1,363.1 405.6,310.6 400.0,237.2 461.1,214.6 515.7,201.8 548.9,170.6 575.0,144.0 625.6,103.9 666.7,84.7 716.7,62.1 777.8,11.3"/><g class="km-nh" transform="translate(422 333)"><rect x="-30" y="-14" width="60" height="28" rx="6"/><text y="5">NH 544</text></g><g class="km-town"><circle cx="369.1" cy="238.5" r="5"/><text x="381.1" y="243.5">Thrissur</text></g><g class="km-town"><circle cx="445.3" cy="475.7" r="5"/><text x="457.3" y="480.7">Aluva</text></g><g class="km-town"><circle cx="716.7" cy="62.1" r="5"/><text x="728.7" y="67.1">Walayar</text></g></svg>'
PINPOS = [[62.561, 15.333], [42.467, 81.075]]
mpins = '\n'.join(f'''          <a class="kpin" data-k="{k}" href="{gplace(name, pid)}" target="_blank" rel="noopener" style="left:{PINPOS[k][0]}%;top:{PINPOS[k][1]}%">
            <span class="kpin-mark" aria-hidden="true"><svg viewBox="0 0 36 48"><path d="M18 2C9.2 2 2 9 2 17.6 2 29.4 18 46 18 46s16-16.6 16-28.4C34 9 26.8 2 18 2z"/><circle cx="18" cy="17.5" r="6"/></svg><i></i></span>
            <span class="kpin-l"><b>{city} office</b><span>{name}</span></span><span class="sr-only"> – open in Google Maps (new tab)</span>
          </a>''' for k, (city, name, addr, q, pid, daddr) in enumerate(OFFICES))

body = f'''{nav}
<main id="top">

<!-- ======= CONTACT HERO + QUICK CONTACT ======= -->
<section class="ct-hero" id="ct-hero" aria-labelledby="ctTitle">
  <div class="wrap ct-hero-in">
    <div class="ct-copy">
      <nav class="ab-crumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">Contact</span></nav>
      <h1 class="ab-h1" id="ctTitle"><span class="ln"><span>Let’s power</span></span><span class="ln"><span><em>your next move.</em></span></span></h1>
      <p class="ct-intro">Whether you’re planning solar for your home, exploring energy solutions for your business, or developing a large-scale industrial project, our team is here to help.</p>
    </div>
    <div class="qcs">
      <h2 class="sr-only">Quick contact</h2>
{quick}
    </div>
  </div>
</section>

<!-- ======= ENQUIRY ======= -->
<section class="ct-enq band" id="enquiry" aria-labelledby="enqTitle">
  <div class="wrap ct-enq-in">
    <div class="ct-side">
      <div class="eyebrow">Enquiry</div>
      <h2 id="enqTitle">Tell us about <em>your project</em></h2>
      <p>A few details are enough to get started. Name and phone are all we need.</p>
      <ol class="ct-steps">
        <li><span>01</span><div><b>We call you back</b><p>to understand what you need.</p></div></li>
        <li><span>02</span><div><b>We look at your bills and site</b><p>usage, space and future energy needs.</p></div></li>
        <li><span>03</span><div><b>You get a recommendation and quote</b><p>sized for your home or business.</p></div></li>
      </ol>
    </div>
    <form class="cf" id="enqForm" name="enquiry" method="post" data-netlify="true" netlify-honeypot="bot-field" novalidate>
      <input type="hidden" name="form-name" value="enquiry">
      <p class="cf-hp" aria-hidden="true"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
      <p class="cf-req"><span aria-hidden="true">*</span> Required</p>
      <div class="cf-row">
        <div class="cf-f"><label for="fName">Full name <span class="star" aria-hidden="true">*</span></label><input id="fName" name="name" autocomplete="name" required aria-required="true"><p class="cf-err" id="fNameErr" hidden>Please enter your name.</p></div>
        <div class="cf-f"><label for="fPhone">Phone number <span class="star" aria-hidden="true">*</span></label><input id="fPhone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required aria-required="true" aria-describedby="fPhoneHint"><p class="cf-hint" id="fPhoneHint">10-digit mobile number, with or without +91</p><p class="cf-err" id="fPhoneErr" hidden>Please enter a valid phone number, for example 99462 07738.</p></div>
      </div>
      <div class="cf-f"><label for="fEmail">Email <small>(optional)</small></label><input id="fEmail" name="email" type="email" autocomplete="email"><p class="cf-err" id="fEmailErr" hidden>Please check the email address, for example name@example.com.</p></div>
      <fieldset class="cf-f its">
        <legend>I’m interested in</legend>
        <div class="it-grid">
{radios}
        </div>
      </fieldset>
      <div class="cf-f"><label for="fMsg">Project requirements <small>(optional)</small></label><textarea id="fMsg" name="message" rows="4" placeholder="Monthly bill, roof or site size, anything we should know"></textarea></div>
      <p class="cf-consent">By sending this form you agree that Sinelab Technologies may contact you about your enquiry.</p>
      <div class="cf-send"><button class="btn btn-sun" type="submit">Send enquiry {ARR}</button></div>
      <p class="cf-sum" id="cfSum" role="alert" hidden></p>
    </form>
    <div class="cf-ok" id="cfOk" role="status" hidden tabindex="-1">
      <span class="cf-ok-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span>
      <h3>Thank you, <span id="cfOkName"></span></h3>
      <p>We’ve got your enquiry. Our team will call you back to talk it through.</p>
      <p class="cf-ok-note">Preview only: on the live site this sends your details to info@sinelabtechnologies.com.</p>
      <button type="button" class="btn ab-btn-ghost cf-again" id="cfAgain">Send another enquiry</button>
    </div>
  </div>
</section>

<!-- ======= OFFICES: one map with both offices pinned ======= -->
<section class="ct-off band" id="offices" aria-labelledby="offTitle">
  <div class="wrap">
    <div class="sec-head">
      <div><div class="eyebrow">Offices</div><h2 id="offTitle">Find us in <em>Kerala</em></h2></div>
      <p>Sinelab Technologies Pvt. Ltd. has two offices, in Palakkad and Kochi. Tap a pin or a card for directions.</p>
    </div>
    <div class="locmap">
      <div class="loc-panel">
{locs}
      </div>
      <div class="kmap" id="kmap">
        <div class="kmap-in">
        {KERALA}
{mpins}
        </div>
        <span class="kmap-note">Simplified map · coastline: Natural Earth</span>
      </div>
    </div>
  </div>
</section>

</main>

{foot}'''

CSS = ABOUT_CSS + '''
/* ================= Contact page ================= */
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.ct-hero{position:relative;isolation:isolate;overflow:hidden;background:var(--navy-deep);color:#fff;padding:clamp(140px,16vh,190px) 0 clamp(70px,9vw,120px)}
.ct-hero::before{content:"";position:absolute;inset:0;z-index:-1;background:radial-gradient(50% 70% at 85% 30%,rgba(249,194,46,.12) 0%,rgba(249,194,46,0) 60%),radial-gradient(rgba(255,255,255,.07) 1px,transparent 1.2px) 0 0/24px 24px}
.ct-hero-in{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:clamp(40px,6vw,100px);align-items:end}
.ct-hero.in .ab-crumb{opacity:1;transform:none}
.ct-hero.in .ab-h1 .ln:nth-child(1)>span{transform:none;transition-delay:.1s}
.ct-hero.in .ab-h1 .ln:nth-child(2)>span{transform:none;transition-delay:.45s}
.ct-hero .ab-h1{font-size:clamp(40px,5vw,76px)}
.ct-intro{margin:26px 0 0;max-width:48ch;font-size:clamp(16.5px,1.25vw,19px);line-height:1.6;color:var(--on-dark-muted);opacity:0;transform:translateY(14px);transition:opacity .9s ease .7s,transform 1.1s cubic-bezier(.2,.7,.2,1) .7s}
.ct-hero.in .ct-intro{opacity:1;transform:none}
.qcs{display:grid;gap:12px}
.qc{position:relative;display:grid;grid-template-columns:52px minmax(0,1fr) 40px;align-items:center;gap:16px;padding:18px 20px;border-radius:18px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);color:#fff;text-decoration:none;overflow:hidden;isolation:isolate;opacity:0;transform:translateY(18px);transition:opacity .8s ease,transform 1s cubic-bezier(.2,.7,.2,1),border-color .3s,color .35s}
.ct-hero.in .qc{opacity:1;transform:none}
.ct-hero.in .qc:nth-child(1){transition-delay:.55s,.55s,0s,0s}.ct-hero.in .qc:nth-child(2){transition-delay:.68s,.68s,0s,0s}.ct-hero.in .qc:nth-child(3){transition-delay:.81s,.81s,0s,0s}
.qc::before{content:"";position:absolute;inset:0;z-index:-1;background:var(--sun);transform:scaleX(0);transform-origin:0 50%;transition:transform .55s cubic-bezier(.2,.7,.2,1)}
.qc:hover::before,.qc:focus-visible::before{transform:none}
.qc:hover,.qc:focus-visible{color:var(--ink);border-color:var(--sun)}
.qc:focus-visible{outline:2px solid #fff;outline-offset:3px;box-shadow:0 0 0 3px var(--sun)}
.qc-ico{display:grid;place-items:center;width:52px;height:52px;border-radius:50%;background:rgba(255,255,255,.08);color:var(--sun);transition:background .35s,color .35s}
.qc-ico svg{width:24px;height:24px}
.qc:hover .qc-ico,.qc:focus-visible .qc-ico{background:var(--ink);color:var(--sun)}
.qc-txt{display:flex;flex-direction:column;min-width:0}
.qc-k{font:500 11.5px var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.7);transition:color .35s}
.qc b{margin-top:4px;font-size:clamp(17px,1.5vw,21px);font-weight:400;letter-spacing:-0.01em;overflow-wrap:anywhere}
.qc-d{margin-top:3px;font-size:14px;color:rgba(255,255,255,.7);transition:color .35s}
.qc:hover .qc-k,.qc:hover .qc-d,.qc:focus-visible .qc-k,.qc:focus-visible .qc-d{color:rgba(9,9,11,.75)}
.qc-go{display:grid;place-items:center;width:40px;height:40px;border-radius:50%;border:1px solid rgba(255,255,255,.25);transition:transform .45s cubic-bezier(.2,.7,.2,1),border-color .35s}
.qc-go svg{width:16px;height:16px}
.qc:hover .qc-go,.qc:focus-visible .qc-go{transform:translateX(4px);border-color:rgba(9,9,11,.35)}

.ct-enq{padding-block:clamp(90px,11vw,150px)}
.ct-enq-in{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:clamp(40px,6vw,100px);align-items:start}
.ct-side{position:sticky;top:120px}
.ct-side h2{margin-top:14px;font-size:clamp(32px,3.6vw,52px);color:var(--navy)}
.ct-side>p{margin:18px 0 0;max-width:40ch;font-size:17px;line-height:1.6;color:var(--muted)}
.ct-steps{list-style:none;margin:clamp(30px,4vw,48px) 0 0;padding:0}
.ct-steps li{display:grid;grid-template-columns:44px minmax(0,1fr);gap:14px;padding:18px 0;border-top:1px solid var(--line)}
.ct-steps li:last-child{border-bottom:1px solid var(--line)}
.ct-steps span{font:500 12px var(--f-mono);letter-spacing:.08em;color:var(--accent-ink);padding-top:3px}
.ct-steps b{font-size:17px;font-weight:500;color:var(--ink)}
.ct-steps p{margin:4px 0 0;font-size:15px;line-height:1.5;color:var(--muted)}
.cf,.cf-ok{padding:clamp(24px,3vw,44px);border-radius:24px;background:var(--paper)}
.cf-hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.cf-req{margin:0 0 6px;font-size:13.5px;color:var(--muted)}
.cf-req span,.star{color:#B42318}
.cf-row{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.cf-f{margin:0 0 20px;padding:0;border:0;min-width:0}
.cf label,.cf legend{display:block;margin-bottom:8px;font-size:15px;font-weight:500;color:var(--ink)}
.cf legend{padding:0}
.cf label small,.cf legend small{font-weight:400;color:var(--muted)}
.cf input:not([type=radio]),.cf textarea{display:block;width:100%;min-height:52px;padding:14px 16px;border:1px solid #8A8A93;border-radius:12px;background:#fff;font:inherit;font-size:16px;color:var(--ink);transition:border-color .2s,box-shadow .2s}
.cf textarea{min-height:120px;resize:vertical;line-height:1.5}
.cf input::placeholder,.cf textarea::placeholder{color:#6E6E78}
.cf input:not([type=radio]):hover,.cf textarea:hover{border-color:var(--ink)}
.cf input:not([type=radio]):focus-visible,.cf textarea:focus-visible{outline:2px solid var(--ink);outline-offset:2px;box-shadow:0 0 0 5px var(--sun);border-color:var(--ink)}
.cf [aria-invalid="true"]{border-color:#B42318!important;box-shadow:0 0 0 1px #B42318}
.cf-hint{margin:6px 0 0;font-size:13.5px;color:var(--muted)}
.cf-err{display:flex;align-items:center;gap:6px;margin:6px 0 0;font-size:14px;font-weight:500;color:#B42318}
.cf-err::before{content:"!";display:grid;place-items:center;flex:none;width:18px;height:18px;border-radius:50%;background:#B42318;color:#fff;font-size:12px;font-weight:700}
.it-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.it{position:relative;display:block;margin:0;cursor:pointer}
.it input{position:absolute;opacity:0;width:1px;height:1px}
.it-box{display:grid;grid-template-columns:40px minmax(0,1fr);grid-template-rows:auto auto;column-gap:12px;align-items:center;min-height:72px;padding:12px 14px;border:1px solid #C8C8CE;border-radius:14px;background:#fff;transition:border-color .25s,background .25s,box-shadow .25s}
.it-ico{grid-row:1/3;display:grid;place-items:center;width:40px;height:40px;border-radius:10px;background:var(--paper);color:var(--ink);transition:background .25s}
.it-ico svg{width:24px;height:24px}
.it-box b{font-size:15px;font-weight:500;line-height:1.25;color:var(--ink)}
.it-box small{font-size:13px;color:var(--muted)}
.it:hover .it-box{border-color:var(--ink)}
.it input:checked+.it-box{border-color:var(--ink);box-shadow:inset 0 0 0 1px var(--ink)}
.it input:checked+.it-box .it-ico{background:var(--sun)}
.it input:focus-visible+.it-box{outline:2px solid var(--ink);outline-offset:3px;box-shadow:0 0 0 3px var(--sun)}
.cf-consent{margin:4px 0 0;font-size:14px;line-height:1.55;color:var(--muted)}
.cf-send{margin-top:20px}
.cf-send .btn{min-height:52px;padding-inline:26px}
.cf-sum{margin:16px 0 0;padding:12px 14px;border-radius:12px;background:#FEF3F2;border:1px solid #FDA29B;font-size:15px;color:#912018}
.cf-ok{display:flex;flex-direction:column;align-items:flex-start;gap:6px;min-height:420px;justify-content:center}
.cf-ok[hidden]{display:none}
.cf-ok:focus{outline:none}
.cf-ok-ico{display:grid;place-items:center;width:64px;height:64px;margin-bottom:10px;border-radius:50%;background:var(--sun);color:var(--ink);animation:okPop .6s cubic-bezier(.2,.7,.2,1)}
.cf-ok-ico svg{width:30px;height:30px}
@keyframes okPop{from{transform:scale(.4);opacity:0}to{transform:none;opacity:1}}
.cf-ok h3{margin:0;font-size:clamp(26px,2.4vw,34px);font-weight:300;letter-spacing:-0.03em;color:var(--ink)}
.cf-ok p{margin:4px 0 0;max-width:44ch;font-size:16.5px;line-height:1.6;color:var(--muted)}
.cf-ok .cf-ok-note{font-size:14px}
.cf-again{margin-top:18px;color:var(--ink);border-color:var(--ink);background:transparent}

.ct-off{background:var(--paper);padding-block:clamp(90px,11vw,150px)}
.locmap{display:grid;grid-template-columns:minmax(0,380px) minmax(0,1fr);gap:clamp(14px,1.6vw,22px);align-items:stretch}
.loc-panel{display:flex;flex-direction:column;gap:12px}
.loc{padding:18px 18px 18px;border:1px solid var(--line);border-radius:20px;background:#fff;transition:border-color .3s,box-shadow .3s}
.loc.is-hl{border-color:var(--ink);box-shadow:inset 0 0 0 1px var(--ink)}
.loc-hd{display:grid;grid-template-columns:auto minmax(0,1fr) 38px;align-items:center;gap:12px}
.loc-n{font:500 12px var(--f-mono);letter-spacing:.08em;color:var(--accent-ink)}
.loc-t{display:flex;flex-direction:column;min-width:0}
.loc-k{font:500 11px var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.loc-t b{margin-top:3px;font-size:18px;font-weight:500;letter-spacing:-0.01em;color:var(--ink)}
.loc-pin{display:grid;place-items:center;width:38px;height:38px;border-radius:50%;background:var(--sun);color:var(--ink)}
.loc-pin svg{width:19px;height:19px}
.loc-addr{margin:14px 0 0;padding-top:12px;border-top:1px solid var(--line);font-size:15.5px;line-height:1.55;color:var(--ink)}
.loc-hrs{display:flex;align-items:center;gap:8px;margin:10px 0 0;font-size:14.5px;color:var(--muted)}
.loc-hrs svg{width:17px;height:17px;color:var(--accent-ink)}
.loc-links{display:flex;flex-wrap:wrap;align-items:center;gap:8px 16px;margin-top:14px}
.loc-go{min-height:44px;padding:0 18px;font-size:14.5px;gap:8px}
.loc-go svg{width:17px;height:17px}
.loc-open{padding:10px 0;font-size:14.5px;color:var(--ink);text-decoration:underline;text-decoration-color:var(--sun);text-decoration-thickness:2px;text-underline-offset:5px}
/* the map: drawn coastline, NH 544 between the offices, both offices pinned */
.kmap{position:relative;align-self:start;width:100%;aspect-ratio:1000/678;border-radius:24px;overflow:hidden;background:#E3E8EE;isolation:isolate}   /* same shape as the drawing, so the pins sit exactly on their spots */
.kmap-in{position:absolute;inset:0}
.km{position:absolute;inset:0;width:100%;height:100%}
.km .km-sea{fill:#E3E8EE}
.km .km-land{fill:#F7F7F8;stroke:#fff;stroke-width:3;stroke-linejoin:round}
.km .km-dots{fill:url(#kmDots);opacity:.8}
.km .km-sea-l{font:italic 400 20px var(--f-body);letter-spacing:.3em;fill:#8A93A0}
.km .km-road-c{fill:none;stroke:#fff;stroke-width:12;stroke-linecap:round;stroke-linejoin:round}
.km .km-road{fill:none;stroke:var(--sun);stroke-width:5;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1 0}
.km .km-nh rect{fill:#fff;stroke:#D4D4D8}
.km .km-nh text{font:600 13px var(--f-mono);letter-spacing:.04em;fill:var(--ink);text-anchor:middle}
.km .km-town circle{fill:#fff;stroke:#8A8A93;stroke-width:2.5}
.km .km-town text{font:500 17px var(--f-body);fill:#55555D}
.kpin{position:absolute;z-index:2;display:flex;align-items:flex-end;gap:8px;transform:translate(-18px,-100%);color:var(--ink);text-decoration:none}
.kpin-mark{position:relative;flex:none;width:36px;height:48px}
.kpin-mark svg{position:relative;z-index:1;width:100%;height:100%;filter:drop-shadow(0 6px 10px rgba(9,9,11,.3));transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.kpin-mark path{fill:var(--navy-deep)}.kpin-mark circle{fill:var(--sun)}
.kpin-mark i{position:absolute;left:50%;bottom:-5px;width:18px;height:8px;margin-left:-9px;border-radius:50%;background:rgba(249,194,46,.65);animation:pinPulse 2.4s ease-out infinite}
@keyframes pinPulse{0%{transform:scale(.6);opacity:.9}100%{transform:scale(3.4);opacity:0}}
.kpin-l{display:flex;flex-direction:column;margin-bottom:22px;padding:8px 12px;border-radius:12px;background:#fff;box-shadow:0 10px 30px -12px rgba(9,9,11,.35);white-space:nowrap;transition:background .3s,color .3s}
.kpin-l b{font-size:14.5px;font-weight:600}
.kpin-l span{font-size:12.5px;color:var(--muted);transition:color .3s}
.kpin:hover .kpin-mark svg,.kpin:focus-visible .kpin-mark svg,.kpin.is-hl .kpin-mark svg{transform:translateY(-4px) scale(1.08)}
.kpin:hover .kpin-l,.kpin:focus-visible .kpin-l,.kpin.is-hl .kpin-l{background:var(--navy-deep);color:#fff}
.kpin:hover .kpin-l span,.kpin:focus-visible .kpin-l span,.kpin.is-hl .kpin-l span{color:rgba(255,255,255,.75)}
.kpin:focus-visible{outline:none}
.kpin:focus-visible .kpin-l{outline:2px solid var(--ink);outline-offset:3px;box-shadow:0 0 0 6px var(--sun)}
.kmap-note{position:absolute;right:12px;bottom:10px;font:500 10.5px var(--f-mono);letter-spacing:.04em;color:#5F5F69;background:rgba(255,255,255,.75);padding:3px 8px;border-radius:6px}
@media (max-width:760px){
  .locmap{grid-template-columns:1fr}
  .kmap{order:-1;border-radius:20px;aspect-ratio:600/678}
  .kmap-in{left:-41.667%;right:auto;width:166.667%}   /* phones: crop to the strip between the two offices, pins stay on their spots */
  .kpin-l{padding:6px 10px}.kpin-l b{font-size:13px}.kpin-l span{display:none}
}
@media (prefers-reduced-motion: reduce){.kpin-mark i{animation:none}.kpin-mark svg,.kpin-l{transition:none}}

@media (max-width:1000px){
  .ct-hero-in{grid-template-columns:1fr;align-items:start}
  .ct-enq-in{grid-template-columns:1fr}
  .ct-side{position:static}
}
@media (max-width:700px){
  .ct-hero{padding-top:120px}
  .cf-row,.it-grid,.ofs{grid-template-columns:1fr}
  .cf-row{gap:0}
  .cf-send .btn{width:100%;justify-content:center}
  .qc{grid-template-columns:44px minmax(0,1fr) 34px;gap:12px;padding:14px 14px}
  .qc-ico{width:44px;height:44px}.qc-go{width:34px;height:34px}
}
@media (prefers-reduced-motion: reduce){
  .ct-intro,.qc{opacity:1;transform:none;transition:none}
  .cf-ok-ico{animation:none}
}
'''
head = head[:head.rindex('</style>')] + CSS + head[head.rindex('</style>'):]

JS = r'''/* ---------- Hero: headline lines rise in, then the intro and the three contact tiles ---------- */
(function(){ const h = document.getElementById('ct-hero'); if (!h) return; requestAnimationFrame(() => setTimeout(() => h.classList.add('in'), 60)); })();

/* ---------- Offices: an office card and its pin light up together ---------- */
(function(){
  const cards = [...document.querySelectorAll('.loc')], pins = [...document.querySelectorAll('.kpin')];
  const hl = (k, on) => { cards.forEach(c => c.classList.toggle('is-hl', on && c.dataset.k === k)); pins.forEach(p => p.classList.toggle('is-hl', on && p.dataset.k === k)); };
  [...cards, ...pins].forEach(el => { el.addEventListener('mouseenter', () => hl(el.dataset.k, true)); el.addEventListener('mouseleave', () => hl(el.dataset.k, false));
    el.addEventListener('focusin', () => hl(el.dataset.k, true)); el.addEventListener('focusout', () => hl(el.dataset.k, false)); });
})();

/* ---------- Enquiry form: checks name and phone (and email if given), explains each problem next to its field ---------- */
(function(){
  const form = document.getElementById('enqForm'); if (!form) return;
  const $ = id => document.getElementById(id), ok = $('cfOk'), sum = $('cfSum');
  const fields = [
    { el: $('fName'), err: $('fNameErr'), hint: null, test: v => v.trim().length > 1 },
    { el: $('fPhone'), err: $('fPhoneErr'), hint: 'fPhoneHint', test: v => /^(\+?91[\s-]?)?0?[6-9]\d{4}[\s-]?\d{5}$/.test(v.trim()) },
    { el: $('fEmail'), err: $('fEmailErr'), hint: null, test: v => !v.trim() || /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) }
  ];
  const mark = (f, bad) => {
    f.el.setAttribute('aria-invalid', String(bad)); f.err.hidden = !bad;
    f.el.setAttribute('aria-describedby', [f.hint, bad ? f.err.id : null].filter(Boolean).join(' ') || ''); if (!f.el.getAttribute('aria-describedby')) f.el.removeAttribute('aria-describedby');
  };
  // after a first try, fix-ups clear as soon as the field becomes valid
  fields.forEach(f => f.el.addEventListener('input', () => { if (f.el.getAttribute('aria-invalid') === 'true' && f.test(f.el.value)) mark(f, false); }));
  form.addEventListener('submit', e => {
    e.preventDefault();
    if (form.querySelector('[name="bot-field"]').value) return;          // spam trap
    const bad = fields.filter(f => !f.test(f.el.value));
    fields.forEach(f => mark(f, bad.includes(f)));
    if (bad.length){
      sum.textContent = bad.length === 1 ? 'Please fix 1 field above.' : 'Please fix ' + bad.length + ' fields above.'; sum.hidden = false;
      bad[0].el.focus(); return;
    }
    sum.hidden = true;
    $('cfOkName').textContent = $('fName').value.trim().split(/\s+/)[0];
    form.hidden = true; ok.hidden = false; ok.focus();
  });
  $('cfAgain').addEventListener('click', () => { form.reset(); ok.hidden = true; form.hidden = false; $('fName').focus(); });
})();

'''
script = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>\n'
          '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>\n'
          '<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>\n<script>\n'
          + js_core + js_nav + JS + '})();\n</script>\n')
src = (head + body + script).replace('index.html#contact', 'contact.html')
open(d + 'contact_src.html', 'w').write(src)

mime = {'png':'image/png','jpg':'image/jpeg','webp':'image/webp'}
import sys; sys.path.insert(0, d); from webp_cache import webp   # all images as WebP
def uri(path): path = webp(path); return 'data:' + mime[path.rsplit('.',1)[1]] + ';base64,' + base64.b64encode(open(path,'rb').read()).decode()
out = re.sub(r'\{\{L:([^}]+)\}\}', lambda m: uri(d + 'layers/' + m.group(1)), src)
out = out.replace('{{LOGO_BLACK}}', uri(d + 'logo_black.png')).replace('{{LOGO_WHITE}}', uri(d + 'logo_white.png'))
assert '{{' not in out, re.findall(r'\{\{[^}]+\}\}', out)[:3]
hi = out.index('<!-- ======= NAV ======= -->')
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
       + out[:hi] + '</head>\n<body>\n' + out[hi:] + '</body>\n</html>\n')
open(d + 'contact.html', 'w').write(doc)
print('contact.html', len(doc) // 1024, 'KB')
