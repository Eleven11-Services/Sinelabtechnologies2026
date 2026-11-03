# Homepage "Featured projects" (user comment, 3 Nov): no sideways scrolling. Show four projects at one glance
# (Bava Metals large, Grand Bajaj, Salim Hybrid Residence, Bala Cinemas) plus a "View all projects" tile.
# Replaces the pinned horizontal slider (#projTrack), its CSS, phone CSS and JS. Backup: src_v61_pre_pgrid.html
import re, shutil
from PIL import Image, ImageOps
d = '/tmp/claude-0/site/'
SRC = d + 'src_draft.html'
shutil.copy(SRC, d + 'src_v61_pre_pgrid.html')
s = open(SRC).read()

def rp(s, a, b, label):
    assert s.count(a) == 1, (label, s.count(a)); return s.replace(a, b)

# ---------- images ----------
L = d + 'layers/'
P = '/tmp/claude-0/handover/sinelab-website/assets-source/photos/projects/'
Image.open(P + 'bava-metals.jpg').convert('RGB').save(L + 'real_bava_feat.jpg', quality=90)            # full frame; the card crops it
for k in ('bajaj', 'salim', 'bala'):
    Image.open(L + f'real_{k}_slide.jpg').convert('RGB').resize((1000, 625), Image.LANCZOS).save(L + f'real_{k}_tile.jpg', quality=88)
for k in ('jamal', 'psurg', 'sinicon'):
    ImageOps.fit(Image.open(L + f'real_{k}_card.jpg').convert('RGB'), (160, 160), Image.LANCZOS).save(L + f'real_{k}_dot.jpg', quality=86)

# ---------- HTML ----------
a = s.index('  <div class="proj-pin" id="projPin">')
b = s.index('<!-- ======= TEAM + REVIEWS ======= -->')
old = s[a:b]
assert old.count('<article class="proj">') == 7
NEW = '''    <div class="pjg" id="projGrid">
      <article class="pjc pjc--lead">
        <div class="pjc-img"><img src="{{L:real_bava_feat.jpg}}" style="object-position:42% 50%" alt="Drone view of the Bava Metals building, with solar panels along its metal roofs" loading="lazy"></div>
        <div class="pjc-cap"><span class="pjc-n">01</span><div><h3><a class="pjc-a" href="projects.html#bava-metals">Bava Metals</a></h3>
          <p class="pjc-d">Rooftop solar set along the metal roofs of a busy town-centre building.</p><p class="pjc-t">Rooftop solar · Commercial</p></div></div>
      </article>
      <article class="pjc">
        <div class="pjc-img"><img src="{{L:real_bajaj_tile.jpg}}" alt="Solar panels on a raised steel frame above the Grand Bajaj showroom" loading="lazy"></div>
        <div class="pjc-cap"><span class="pjc-n">02</span><div><h3><a class="pjc-a" href="projects.html#grand-bajaj">Grand Bajaj Showroom</a></h3><p class="pjc-t">Rooftop solar · Showroom</p></div></div>
      </article>
      <article class="pjc">
        <div class="pjc-img"><img src="{{L:real_salim_tile.jpg}}" alt="Top-down drone view of the Salim residence, with solar panels on two of its flat roofs" loading="lazy"></div>
        <div class="pjc-cap"><span class="pjc-n">03</span><div><h3><a class="pjc-a" href="projects.html#salim-residence">Salim Hybrid Residence</a></h3><p class="pjc-t">Hybrid solar · Residential</p></div></div>
      </article>
      <article class="pjc">
        <div class="pjc-img"><img src="{{L:real_bala_tile.jpg}}" alt="Drone view of the Bala Cinemas building with a solar array on its roof" loading="lazy"></div>
        <div class="pjc-cap"><span class="pjc-n">04</span><div><h3><a class="pjc-a" href="projects.html#bala-cinemas">Bala Cinemas</a></h3><p class="pjc-t">Rooftop solar · Cinema</p></div></div>
      </article>
      <a class="pjc-more" href="projects.html">
        <span class="pjc-stack" aria-hidden="true"><img src="{{L:real_jamal_dot.jpg}}" alt="" loading="lazy"><img src="{{L:real_psurg_dot.jpg}}" alt="" loading="lazy"><img src="{{L:real_sinicon_dot.jpg}}" alt="" loading="lazy"><i>+3</i></span>
        <span class="pjc-more-txt"><b>View all 7 projects</b><span>Rooftops from family homes to factories.</span></span>
        <span class="pjc-go" aria-hidden="true"><svg width="20" height="20" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M4 9h10M10 5l4 4-4 4"/></svg></span>
      </a>
    </div>
  </div>
</section>

'''
# the grid sits inside the section's .wrap (which closed right after the heading)
head_close = '''      <p>Solar Sinelab has built for businesses, factories and homes, photographed from the air.</p>
    </div>
  </div>
'''
assert s[:a].endswith(head_close), 'heading block changed'
s = s[:a - len(head_close)] + head_close[:-len('  </div>\n')] + NEW + s[b:]

# ---------- CSS: drop the slider styles, add the grid ----------
c0 = s.index('/* ---------- Projects (horizontal) ---------- */')
c1 = s.index('/* ---------- Placeholder art')
CSS = '''/* ---------- Featured projects: four at one glance + "view all" tile (user, 3 Nov: no sideways scrolling) ---------- */
.projects{padding-block:clamp(90px,11vw,150px) clamp(60px,8vw,110px)}
.projects .sec-head{margin-bottom:clamp(32px,3.6vw,52px)}
.pjg{display:grid;grid-template-columns:1.32fr 1fr 1fr;grid-template-rows:auto auto;gap:clamp(16px,1.7vw,24px)}
.pjc{position:relative;display:flex;flex-direction:column;gap:14px;min-width:0}
.pjc--lead{grid-row:1 / span 2}
.pjc-img{position:relative;overflow:hidden;border-radius:10px;background:var(--paper);aspect-ratio:16/10}
.pjc--lead .pjc-img{aspect-ratio:auto;flex:1 1 auto;min-height:300px}
.pjc-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:scale 1.2s cubic-bezier(.2,.7,.2,1)}
.pjc:hover .pjc-img img,.pjc:focus-within .pjc-img img{scale:1.045}
/* sunlight glint: sweeps across the panels once as a card appears, again on hover */
.pjc-img::after{content:"";position:absolute;z-index:1;top:-20%;bottom:-20%;left:0;width:45%;pointer-events:none;mix-blend-mode:screen;opacity:0;
  background:linear-gradient(90deg,rgba(255,236,190,0),rgba(255,236,190,.36) 50%,rgba(255,236,190,0));transform:translateX(-120%) skewX(-14deg)}
.pjc.lit .pjc-img::after{animation:projGlint 1.7s cubic-bezier(.3,.6,.3,1) .6s both}
.pjc.lit:hover .pjc-img::after{animation:projGlint2 1.3s cubic-bezier(.3,.6,.3,1) both}
@keyframes projGlint{0%{opacity:0;transform:translateX(-120%) skewX(-14deg)}20%{opacity:1}100%{opacity:0;transform:translateX(340%) skewX(-14deg)}}
@keyframes projGlint2{0%{opacity:0;transform:translateX(-120%) skewX(-14deg)}20%{opacity:1}100%{opacity:0;transform:translateX(340%) skewX(-14deg)}}
.pjc-cap{display:flex;gap:14px;align-items:baseline}
.pjc-n{flex:none;min-width:22px;font:500 12px var(--f-mono);letter-spacing:.04em;color:var(--muted);font-variant-numeric:tabular-nums}
.pjc h3{font-size:21px;font-weight:400;line-height:1.2}
.pjc--lead h3{font-size:clamp(24px,2.1vw,30px)}
.pjc-a{color:inherit;text-decoration:underline;text-decoration-color:transparent;text-decoration-thickness:2px;text-underline-offset:6px;transition:text-decoration-color .3s}
.pjc-a::after{content:"";position:absolute;inset:0;z-index:2}   /* the whole card opens the project */
.pjc:hover .pjc-a{text-decoration-color:var(--sun)}
.pjc-a:focus-visible{outline:none;box-shadow:none;text-decoration-color:var(--sun)}
.pjc:has(.pjc-a:focus-visible){outline:2px solid var(--ink);outline-offset:4px;box-shadow:0 0 0 4px #fff,0 0 0 7px var(--sun);border-radius:12px}
.pjc-d{margin:8px 0 0;max-width:44ch;font-size:15px;color:var(--muted)}
.pjc-t{margin:6px 0 0;font:500 12px var(--f-mono);letter-spacing:.03em;color:var(--muted)}
/* "view all" tile */
.pjc-more{position:relative;display:flex;flex-direction:column;justify-content:space-between;gap:20px;min-height:200px;padding:clamp(20px,2vw,28px);border-radius:10px;
  background:var(--ink);color:#fff;text-decoration:none;overflow:hidden;transition:background .4s}
.pjc-more::before{content:"";position:absolute;right:-30%;bottom:-60%;width:90%;aspect-ratio:1;border-radius:50%;background:radial-gradient(closest-side,rgba(249,194,46,.20),rgba(249,194,46,0));pointer-events:none;transition:transform .8s cubic-bezier(.2,.7,.2,1)}
.pjc-more:hover::before{transform:scale(1.25)}
.pjc-stack{display:flex;align-items:center}
.pjc-stack img,.pjc-stack i{width:46px;height:46px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 3px var(--ink)}
.pjc-stack img+img,.pjc-stack img+i{margin-left:-12px}
.pjc-stack i{display:grid;place-items:center;background:#27272A;font:500 13px var(--f-mono);font-style:normal;color:#fff}
.pjc-more-txt{position:relative;display:grid;gap:6px;padding-right:56px}
.pjc-more-txt b{font-size:clamp(21px,1.8vw,26px);font-weight:400;line-height:1.15}
.pjc-more-txt span{font-size:14px;color:var(--on-dark-muted)}
.pjc-go{position:absolute;right:clamp(20px,2vw,28px);bottom:clamp(20px,2vw,28px);display:grid;place-items:center;width:46px;height:46px;border-radius:50%;background:var(--sun);color:var(--ink);transition:transform .45s cubic-bezier(.2,.7,.2,1)}
.pjc-more:hover .pjc-go,.pjc-more:focus-visible .pjc-go{transform:translateX(4px) rotate(-45deg)}
/* soft reveal as the grid comes into view (only when motion is allowed) */
.pjg.rv .pjc-img{clip-path:inset(100% 0 0 0 round 10px);transition:clip-path 1.1s cubic-bezier(.65,0,.25,1) var(--dl,0s)}
.pjg.rv .pjc-img img{scale:1.14;transition:scale 1.6s cubic-bezier(.2,.7,.2,1) var(--dl,0s)}
.pjg.rv .pjc-cap,.pjg.rv .pjc-more{opacity:0;transform:translateY(16px);transition:opacity .8s calc(var(--dl,0s) + .3s),transform .8s calc(var(--dl,0s) + .3s) cubic-bezier(.2,.7,.2,1)}
.pjg.rv .in .pjc-img{clip-path:inset(0 0 0 0 round 10px)}
.pjg.rv .in .pjc-img img{scale:1}
.pjg.rv .in:hover .pjc-img img,.pjg.rv .in:focus-within .pjc-img img{scale:1.045;transition-delay:0s}
.pjg.rv .in .pjc-cap,.pjg.rv .pjc-more.in{opacity:1;transform:none}
@media (prefers-reduced-motion: reduce){.pjc-img::after{display:none}.pjc-img img,.pjc-go,.pjc-more::before{transition:none}}
/* tablets: the lead project across the top, three below, the tile as a bar */
@media (max-width:1023px){
  .pjg{grid-template-columns:repeat(3,minmax(0,1fr))}
  .pjc--lead{grid-column:1 / -1;grid-row:auto}
  .pjc--lead .pjc-img{flex:none;aspect-ratio:16/8;min-height:0}
  .pjc-more{grid-column:1 / -1;flex-direction:row;align-items:center;min-height:0;padding-right:96px}
  .pjc-go{top:50%;bottom:auto;margin-top:-23px}
  .pjc-more:hover .pjc-go,.pjc-more:focus-visible .pjc-go{transform:translateX(4px) rotate(-45deg)}
  .pjc-more-txt{padding-right:0}
}
/* phones: the lead project, then a compact list, then the tile */
@media (max-width:700px){
  .pjg{grid-template-columns:minmax(0,1fr);gap:0}
  .pjc--lead{grid-column:auto;margin-bottom:22px}
  .pjc--lead .pjc-img{aspect-ratio:4/3}
  .pjc:not(.pjc--lead){display:grid;grid-template-columns:112px minmax(0,1fr);align-items:center;gap:14px;padding:12px 0;border-top:1px solid var(--line)}
  .pjc:not(.pjc--lead) .pjc-img{aspect-ratio:4/3;border-radius:8px}
  .pjc:not(.pjc--lead) .pjc-cap{gap:10px}
  .pjc:not(.pjc--lead) h3{font-size:18px}
  .pjc:has(.pjc-a:focus-visible){outline-offset:2px}
  .pjc-more{margin-top:18px;flex-direction:column;align-items:flex-start;gap:16px;padding:20px 84px 20px 20px}
  .pjc-stack img,.pjc-stack i{width:40px;height:40px}
  .pjc-go{right:20px}
}

'''
s = s[:c0] + CSS + s[c1:]

# old slider tweaks elsewhere in the CSS
for line in ['.proj-meta .loc{margin:6px 0 0;max-width:40ch;font-size:14px;color:var(--muted)}\n',
             '.proj-meta .save span,.proj-meta .save b{white-space:nowrap}\n',
             '  .proj-meta .loc{font-size:13.5px}\n']:
    s = rp(s, line, '', line[:30])
p0 = s.index('  /* projects: cards start on the text edge, the next card peeks in, no native scroll bar */')
p1 = s.index('  .proj-progress{margin:22px var(--gR) 0 var(--g);gap:12px}\n') + len('  .proj-progress{margin:22px var(--gR) 0 var(--g);gap:12px}\n')
assert p1 - p0 < 800
s = s[:p0] + s[p1:]
s = rp(s, "node.matches('.proj-track, input[type=\"range\"]", "node.matches('input[type=\"range\"]", 'lenis prevent')

# ---------- JS: replace the slider script ----------
j0 = s.index('/* ---------- Projects: slide, progress line, soft reveal, glint and count-up ---------- */')
j1 = s.index('/* ---------- Testimonials: one quote at a time')
JS = '''/* ---------- Featured projects: the cards wipe in one after another, sunlight sweeps across each photo ---------- */
(function(){
  const grid = $('projGrid');
  if (!grid || reduce || !('IntersectionObserver' in window)) return;
  const items = [...grid.children];
  items.forEach((el, i) => el.style.setProperty('--dl', (innerWidth > 700 ? i * .12 : 0) + 's'));
  grid.classList.add('rv');
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.classList.add('in', 'lit'); io.unobserve(e.target);
  }), { rootMargin: '0px 0px -12% 0px', threshold: .15 });
  items.forEach(el => io.observe(el));
})();

'''
s = s[:j0] + JS + s[j1:]
assert 'projTrack' not in s and 'proj-track' not in s and 'projBar' not in s, 'leftovers'
open(SRC, 'w').write(s)
print('ok', len(s))
