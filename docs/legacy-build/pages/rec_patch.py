# About › Recognition (user, 29 Oct: "pls add some background elements here, it feels so gap"):
# dotted backdrop with a warm glow and slow-drifting line icons; the award becomes a dark card with a drawn
# laurel-and-trophy emblem and a large outlined "2018" behind the text. Placeholder note kept for the real award photo.
import math
p = '/tmp/claude-0/site/about.py'; s = open(p).read()
def rp(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90]); s = s.replace(a, b)

# ---- emblem: rays, laurel wreath, trophy (drawn here, inlined as SVG) ----
cx, cy, R = 200, 160, 98
def leaf(x, y, ang, rx=14, ry=5.6):
    return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx}" ry="{ry}" transform="rotate({ang:.1f} {x:.1f} {y:.1f})"/>'
leaves = []
for side in (-1, 1):
    a0, a1 = (100, 252) if side < 0 else (80, -72)
    n = 10
    for k in range(n):
        t = k / (n - 1); a = math.radians(a0 + (a1 - a0) * t)
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        tang = math.degrees(a) + (90 if side < 0 else -90)       # along the branch, pointing up
        sc = 1 - .35 * t                                         # leaves get smaller towards the tips
        for off in (-28, 28):
            ox, oy = x + 9 * math.cos(math.radians(tang + off)), y + 9 * math.sin(math.radians(tang + off))
            leaves.append(leaf(ox, oy, tang + off, round(14 * sc, 1), round(5.6 * sc, 1)))
stems = (f'<path d="M{cx + R * math.cos(math.radians(100)):.1f} {cy + R * math.sin(math.radians(100)):.1f} A{R} {R} 0 0 1 {cx + R * math.cos(math.radians(252)):.1f} {cy + R * math.sin(math.radians(252)):.1f}"/>'
         f'<path d="M{cx + R * math.cos(math.radians(80)):.1f} {cy + R * math.sin(math.radians(80)):.1f} A{R} {R} 0 0 0 {cx + R * math.cos(math.radians(-72)):.1f} {cy + R * math.sin(math.radians(-72)):.1f}"/>')
rays = ''.join(f'<line x1="{cx + 128 * math.cos(math.radians(a)):.1f}" y1="{cy + 128 * math.sin(math.radians(a)):.1f}" x2="{cx + 190 * math.cos(math.radians(a)):.1f}" y2="{cy + 190 * math.sin(math.radians(a)):.1f}"/>' for a in range(0, 360, 15))
sparks = ''.join(f'<path transform="translate({x} {y}) scale({sc})" d="M0 -10C.7 -4.6 4.6 -.7 10 0 4.6 .7 .7 4.6 0 10-.7 4.6-4.6 .7-10 0-4.6-.7-.7-4.6 0-10z"/>' for x, y, sc in [(92, 62, 1.1), (318, 92, .8), (300, 250, 1), (78, 236, .7)])
EMBLEM = ('<svg class="rec-emblem" viewBox="0 0 400 320" aria-hidden="true">'
          f'<g class="rec-rays" stroke="#F9C22E" stroke-width="1.2" stroke-linecap="round" stroke-dasharray="2 7">{rays}</g>'
          f'<circle cx="{cx}" cy="{cy}" r="74" fill="none" stroke="rgba(255,255,255,.12)" stroke-width="1"/>'
          f'<g class="rec-laurel" fill="none" stroke="#F9C22E" stroke-width="1.5">{stems}{"".join(leaves)}</g>'
          f'<g fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" transform="translate({cx - 40} {cy - 46}) scale(1.25)">'
          '<path d="M20 10h24v14a12 12 0 0 1-24 0z"/><path d="M20 15h-7a7 7 0 0 0 9 9M44 15h7a7 7 0 0 1-9 9M32 36v10M24 54h16M26 46h12v8H26z"/></g>'
          f'<g class="rec-sparks" fill="#F9C22E">{sparks}</g></svg>')
open('/tmp/claude-0/site/rec_emblem.svg', 'w').write(EMBLEM)

FL = {
 'sun': '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"><circle cx="24" cy="24" r="8.5"/><path d="M24 5v6M24 37v6M5 24h6M37 24h6M10.6 10.6l4.2 4.2M33.2 33.2l4.2 4.2M10.6 37.4l4.2-4.2M33.2 14.8l4.2-4.2"/></svg>',
 'spark': '<svg viewBox="0 0 48 48" fill="currentColor"><path d="M24 6c1.4 9.6 8.4 16.6 18 18-9.6 1.4-16.6 8.4-18 18-1.4-9.6-8.4-16.6-18-18 9.6-1.4 16.6-8.4 18-18z"/></svg>',
 'ring': '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.3"><circle cx="24" cy="24" r="17"/><circle cx="24" cy="24" r="9" stroke-dasharray="2 4"/></svg>',
 'leaf': '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"><path d="M9 39C9 19 22 9 40 8c0 19-11 31-31 31z"/><path d="M9 39C17 30 24 24 31 17"/></svg>',
 'medal': '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"><circle cx="24" cy="29" r="11"/><path d="M17 20 11 6h8l5 10M31 20l6-14h-8l-5 10M24 23l1.8 3.7 4 .6-2.9 2.8.7 4-3.6-1.9-3.6 1.9.7-4-2.9-2.8 4-.6z"/></svg>',
}
# [icon, left %, top %, size px, opacity, yellow]
POS = [('sun', 2.5, 4, 84, .10, 0), ('spark', 9, 70, 24, .5, 1), ('ring', 92, 2, 76, .08, 0), ('medal', 94, 58, 58, .10, 0),
       ('leaf', 47, 86, 40, .08, 0), ('spark', 86, 88, 18, .5, 1), ('spark', 30, -2, 16, .45, 1)]
fl = '\n'.join(f'''      <div class="flp" style="left:{x}%;top:{y}%;--s:{sz}px"><div class="fl{" y" if yel else ""}" style="--o:{o};--d:{9 + k % 5}s;--dl:-{k * 1.3:.1f}s;--dx:{(1 if k % 2 else -1) * (8 + k % 3 * 4)}px;--dy:{(-1 if k % 3 else 1) * (12 + k % 4 * 3)}px;--r0:{(k * 37) % 24 - 12}deg;--r1:{(k * 37) % 24 - 4}deg">{FL[ic]}</div></div>'''
               for k, (ic, x, y, sz, o, yel) in enumerate(POS))

rp('''<section class="ab-rec" id="recognition" aria-labelledby="recTitle">
  <div class="wrap">
    <div class="ab-award">
      <div class="ab-award-ph">{TROPHY}<span class="ph-note">Award photo to be added</span></div>''',
   '''<section class="ab-rec" id="recognition" aria-labelledby="recTitle">
  <div class="rec-bg" aria-hidden="true">
    <div class="floaters run">
''' + fl.replace('{', '{{').replace('}', '}}') + '''
    </div>
  </div>
  <div class="wrap">
    <div class="ab-award">
      <span class="rec-num" aria-hidden="true">2018</span>
      <div class="ab-award-ph">''' + EMBLEM.replace('{', '{{').replace('}', '}}') + '''<span class="ph-note">Award photo to be added</span></div>''')

a = s.index('.ab-rec{padding-block:0 clamp(90px,11vw,150px)}'); b = s.index('.ab-award-txt p{', a); b = s.index('\n', b) + 1
s = s[:a] + '''.ab-rec{position:relative;isolation:isolate;padding-block:clamp(40px,5vw,72px) clamp(90px,11vw,150px)}
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
''' + s[b:]
# phones: the outlined year sits smaller; floaters thin out (existing .flp rule hides the 5th onwards)
rp("  .ab-award{grid-template-columns:1fr}", "  .ab-award{grid-template-columns:1fr}\n  .rec-num{font-size:clamp(120px,34vw,180px)}")
open(p, 'w').write(s); print('patched')
