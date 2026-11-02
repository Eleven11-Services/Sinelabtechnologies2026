# Contact offices: one map with BOTH offices pinned (user). Drawn from Natural Earth coastline data (public domain),
# so it shows in the review preview and on the live site; each pin and office card links to Google Maps.
import json, math
p = '/tmp/claude-0/site/contact.py'; s = open(p).read()
land = json.load(open('/tmp/claude-0/geo/land.json'))
W, H = land['W'], land['H']
LON0, LON1, LAT0, LAT1 = 75.55, 77.35, 9.75, 10.95
C = math.cos(math.radians((LAT0 + LAT1) / 2)); K = W / ((LON1 - LON0) * C)
def P(lat, lon): return ((lon - LON0) * C * K, (LAT1 - lat) * K)
NH = [(9.9771, 76.3144), (10.0261, 76.3083), (10.0530, 76.3200), (10.1076, 76.3516), (10.1960, 76.3860), (10.3070, 76.3350),
      (10.4000, 76.2800), (10.5300, 76.2700), (10.5700, 76.3800), (10.5926, 76.4783), (10.6480, 76.5380), (10.6950, 76.5850),
      (10.7660, 76.6761), (10.8000, 76.7500), (10.8400, 76.8400), (10.9300, 76.9500)]
nh = ' '.join('%.1f,%.1f' % P(a, b) for a, b in NH)
mx, my = P(10.36, 76.31)
TOWNS = [('Thrissur', 10.5276, 76.2144, 'r'), ('Aluva', 10.1076, 76.3516, 'r'), ('Walayar', 10.8400, 76.8400, 'r')]
towns = ''.join(f'<g class="km-town"><circle cx="{P(a, b)[0]:.1f}" cy="{P(a, b)[1]:.1f}" r="5"/><text x="{P(a, b)[0] + 12:.1f}" y="{P(a, b)[1] + 5:.1f}">{n}</text></g>' for n, a, b, _ in TOWNS)
PINS = [(10.7660, 76.6761, 0), (9.9771, 76.3144, 1)]
kerala_svg = (f'<svg class="km" viewBox="0 0 {W} {H:.0f}" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
  f'<defs><pattern id="kmDots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="#D9D9DE"/></pattern></defs>'
  f'<rect class="km-sea" width="{W}" height="{H:.0f}"/>'
  f'<path class="km-land" d="{land["d"]}"/><path class="km-dots" d="{land["d"]}"/>'
  f'<text class="km-sea-l" x="70" y="{H * .62:.0f}">Arabian Sea</text>'
  f'<polyline class="km-road-c" points="{nh}"/><polyline class="km-road" points="{nh}"/>'
  f'<g class="km-nh" transform="translate({mx:.0f} {my:.0f})"><rect x="-30" y="-14" width="60" height="28" rx="6"/><text y="5">NH 544</text></g>'
  f'{towns}</svg>')
pins_js = json.dumps([[round(P(a, b)[0] / W * 100, 3), round(P(a, b)[1] / H * 100, 3)] for a, b, _ in PINS])

def rp(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80]); s = s.replace(a, b)

# ---- office cards: both always open (no choosing) ----
i = s.index("locs = '\\n'.join("); j = s.index("body = f'''{nav}")
s = s[:i] + """locs = '\\n'.join(f'''          <article class="loc" data-k="{k}">
            <div class="loc-hd"><span class="loc-n">{k + 1:02d}</span><span class="loc-t"><span class="loc-k">{city} office</span><b>{name}</b></span><span class="loc-pin" aria-hidden="true">{I_PIN}</span></div>
            <p class="loc-addr">{addr}</p>
            <p class="loc-hrs">{I_CLOCK}Mon – Sat, 9:00 am – 5:30 pm</p>
            <div class="loc-links">
              <a class="btn btn-sun loc-go" href="{gdir(daddr, pid)}" target="_blank" rel="noopener">{I_DIR}Get directions<span class="sr-only"> to the {city} office (opens Google Maps in a new tab)</span></a>
              <a class="loc-open" href="{gplace(name, pid)}" target="_blank" rel="noopener">Open in Google Maps<span class="sr-only"> ({city} office, new tab)</span></a>
            </div>
          </article>''' for k, (city, name, addr, q, pid, daddr) in enumerate(OFFICES))
KERALA = __KERALA__
PINPOS = __PINS__
mpins = '\\n'.join(f'''          <a class="kpin" data-k="{k}" href="{gplace(name, pid)}" target="_blank" rel="noopener" style="left:{PINPOS[k][0]}%;top:{PINPOS[k][1]}%">
            <span class="kpin-mark" aria-hidden="true"><svg viewBox="0 0 36 48"><path d="M18 2C9.2 2 2 9 2 17.6 2 29.4 18 46 18 46s16-16.6 16-28.4C34 9 26.8 2 18 2z"/><circle cx="18" cy="17.5" r="6"/></svg><i></i></span>
            <span class="kpin-l"><b>{city} office</b><span>{name}</span></span><span class="sr-only"> – open in Google Maps (new tab)</span>
          </a>''' for k, (city, name, addr, q, pid, daddr) in enumerate(OFFICES))

""".replace('__KERALA__', repr(kerala_svg)).replace('__PINS__', pins_js) + s[j:]

# ---- section markup ----
i = s.index("<!-- ======= OFFICES: one large Google Map; choose an office to pin it ======= -->"); j = s.index("</section>", i) + len("</section>")
s = s[:i] + """<!-- ======= OFFICES: one map with both offices pinned ======= -->
<section class="ct-off band" id="offices" aria-labelledby="offTitle">
  <div class="wrap">
    <div class="sec-head">
      <div><div class="eyebrow">Offices</div><h2 id="offTitle">Find us in <em>Kerala</em></h2></div>
      <p>Sinelab Technologies Pvt. Ltd. has two offices, about 100 km apart on NH 544: Palakkad and Kochi.</p>
    </div>
    <div class="locmap">
      <div class="loc-panel">
{locs}
      </div>
      <div class="kmap" id="kmap">
        {KERALA}
{mpins}
        <span class="kmap-note">Simplified map · coastline: Natural Earth</span>
      </div>
    </div>
  </div>
</section>""" + s[j:]

# ---- CSS: replace the old map block ----
a = s.index(".locmap{display:grid;"); b = s.index("@media (prefers-reduced-motion: reduce){.loc.on .loc-more{animation:none}.locmap-frame{transition:none}}")
b = s.index("\n", b) + 1
s = s[:a] + """.locmap{display:grid;grid-template-columns:minmax(0,380px) minmax(0,1fr);gap:clamp(14px,1.6vw,22px);align-items:stretch}
.loc-panel{display:flex;flex-direction:column;gap:12px}
.loc{padding:18px 18px 18px;border:1px solid var(--line);border-radius:20px;background:#fff;transition:border-color .3s,box-shadow .3s}
.loc.hl{border-color:var(--ink);box-shadow:inset 0 0 0 1px var(--ink)}
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
.kmap{position:relative;min-height:520px;border-radius:24px;overflow:hidden;background:#E3E8EE;isolation:isolate}
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
.kpin:hover .kpin-mark svg,.kpin:focus-visible .kpin-mark svg,.kpin.hl .kpin-mark svg{transform:translateY(-4px) scale(1.08)}
.kpin:hover .kpin-l,.kpin:focus-visible .kpin-l,.kpin.hl .kpin-l{background:var(--navy-deep);color:#fff}
.kpin:hover .kpin-l span,.kpin:focus-visible .kpin-l span,.kpin.hl .kpin-l span{color:rgba(255,255,255,.75)}
.kpin:focus-visible{outline:none}
.kpin:focus-visible .kpin-l{outline:2px solid var(--ink);outline-offset:3px;box-shadow:0 0 0 6px var(--sun)}
.kmap-note{position:absolute;right:12px;bottom:10px;font:500 10.5px var(--f-mono);letter-spacing:.04em;color:#5F5F69;background:rgba(255,255,255,.75);padding:3px 8px;border-radius:6px}
@media (max-width:760px){
  .locmap{grid-template-columns:1fr}
  .kmap{order:-1;min-height:0;aspect-ratio:4/5;border-radius:20px}
  .kpin-l{padding:6px 10px}.kpin-l b{font-size:13px}.kpin-l span{display:none}
}
@media (prefers-reduced-motion: reduce){.kpin-mark i{animation:none}.kpin-mark svg,.kpin-l{transition:none}}
""" + s[b:]

# ---- JS: hovering a card lifts its pin, and the other way round ----
a = s.index("/* ---------- Offices: choosing an office loads its pin on the big Google Map ---------- */")
b = s.index("/* ---------- Enquiry form: checks name and phone")
s = s[:a] + """/* ---------- Offices: an office card and its pin light up together ---------- */
(function(){
  const cards = [...document.querySelectorAll('.loc')], pins = [...document.querySelectorAll('.kpin')];
  const hl = (k, on) => { cards.forEach(c => c.classList.toggle('hl', on && c.dataset.k === k)); pins.forEach(p => p.classList.toggle('hl', on && p.dataset.k === k)); };
  [...cards, ...pins].forEach(el => { el.addEventListener('mouseenter', () => hl(el.dataset.k, true)); el.addEventListener('mouseleave', () => hl(el.dataset.k, false));
    el.addEventListener('focusin', () => hl(el.dataset.k, true)); el.addEventListener('focusout', () => hl(el.dataset.k, false)); });
})();

""" + s[b:]
open(p, 'w').write(s); print('patched')
