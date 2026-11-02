# Draft round 2 (on top of systems.py output):
#  1. "Our people" becomes role / name / quote rows (client request); the circuit drawing and bus lines go.
#  2. The systems model gets a more realistic, premium build: landscaped plot, two-storey villa with wood louvres,
#     raised GI panel frame, water tank, KSEB-style concrete pole, coconut palms, contact shadows, night lighting,
#     and light pulses running inside the cables instead of dots.
d = '/tmp/claude-0/site/'
s = open(d + 'src_draft.html').read()
def rep(a, b):
    global s
    assert s.count(a) == 1, ('COUNT', s.count(a), a[:100]); s = s.replace(a, b)

ARR = '<svg class="arr" width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 9h10M10 5l4 4-4 4"/></svg>'
SIL = '<svg viewBox="0 0 40 40" fill="currentColor" aria-hidden="true"><circle cx="20" cy="14" r="8"/><path d="M4 40c0-9 7-15 16-15s16 6 16 15z"/></svg>'

# ================= 1. Our people: role, name, quote =================
i = s.index('<!-- ======= TEAM + REVIEWS ======= -->'); j = s.index('<!-- =======', i + 10)
LEAD = [
  ('Managing Director', 'Sajeev Kumar K', 'Co-founded SARK Cables in 1996', 'We started out making cables in Kanjikode in 1996. Sinelab carries the same idea forward: build it properly, and stand behind it.'),
  ('Director', 'Sunil Joseph', 'Co-founder, SARK Group', 'Renewable energy was the natural next step for a group built on manufacturing. Every project still has to earn the customer’s trust.'),
  ('Chief Marketing Officer', 'Athul S. Krishna', 'Leads Kochi operations', 'Clean energy should be easy to understand and easy to own. Our job is to make the switch simple for every home and business.'),
]
rows = '\n'.join(f'''      <article class="leader" tabindex="0" aria-label="{n}, {r}">
        <div class="ld-ph">{SIL}<span class="ph-note">Portrait to be added</span></div>
        <div class="ld-txt">
          <blockquote class="ld-msg"><svg class="qm" viewBox="0 0 32 24" fill="currentColor" aria-hidden="true"><path d="M0 24V14C0 6.3 4.3 1.6 12 0l1.6 3C9.4 4.3 7.3 6.9 7 10.5h6V24H0zm18 0V14c0-7.7 4.3-12.4 12-14l1.6 3c-4.2 1.3-6.3 3.9-6.6 7.5h6V24H18z"/></svg><p>{q}</p><span class="ld-tag">Draft quote · for approval</span></blockquote>
          <h3>{n}</h3><span class="ld-role">{r}</span>
        </div>
      </article>''' for r, n, sm, q in LEAD)
s = s[:i] + f'''<!-- ======= TEAM + REVIEWS ======= -->
<section class="people band" id="team">
  <div class="wrap">
    <div class="sec-head">
      <div><div class="eyebrow">Our people</div><h2>The people behind <em>the progress</em></h2></div>
      <p>Visionary founders. Experienced professionals. A new generation of leadership.</p>
    </div>
    <div class="leaders">
{rows}
    </div>
    <a class="text-link ld-more" href="#team">Meet the full team {ARR}</a>
  </div>
</section>


''' + s[j:]
rep('/* ---------- Solar systems: on-grid, off-grid, hybrid', '''/* ---------- Our people: three tall portrait cards in a row; the one you point at widens, its photo eases in and its message rises ---------- */
.leaders{display:flex;gap:16px;height:clamp(440px,40vw,560px)}
.leader{position:relative;flex:1 1 0;min-width:0;border-radius:16px;overflow:hidden;isolation:isolate;background:#D4D4D9;transition:flex-grow .8s cubic-bezier(.2,.7,.2,1)}
.leader.open{flex-grow:1.6}
.ld-ph{position:absolute;inset:0;display:grid;place-items:end center;background:linear-gradient(170deg,#EFEFF2,#CDCDD3);color:#A7A7AF;transform-origin:50% 100%;transition:transform 1s cubic-bezier(.2,.7,.2,1)}
.ld-ph svg{width:min(72%,300px);margin-bottom:-6%}
.leader.open .ld-ph{transform:scale(1.06)}
.ld-ph .ph-note{position:absolute;left:16px;top:16px;font:500 10.5px var(--f-mono);letter-spacing:.05em;text-transform:uppercase;color:#55555D}
.leader::after{content:"";position:absolute;z-index:1;left:0;right:0;bottom:0;height:64%;pointer-events:none;background:linear-gradient(180deg,rgba(9,9,11,0) 0%,rgba(9,9,11,.5) 42%,rgba(9,9,11,.92) 100%);transition:height .7s cubic-bezier(.2,.7,.2,1)}
.leader.open::after{height:82%;background:linear-gradient(180deg,rgba(9,9,11,0) 0%,rgba(9,9,11,.7) 34%,rgba(9,9,11,.94) 100%)}   /* deeper shade behind the message so it stays readable on any photo */
.ld-txt{text-shadow:0 1px 2px rgba(0,0,0,.4)}
.ld-txt{position:absolute;z-index:2;left:0;right:0;bottom:0;padding:clamp(18px,2vw,26px);color:#fff}
.leader h3{margin:0;font:600 clamp(17px,1.5vw,21px)/1.2 var(--f-display);letter-spacing:.02em;text-transform:uppercase;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ld-role{display:block;margin-top:6px;font:500 13px var(--f-body);color:var(--sun)}
.ld-msg{margin:0;max-height:0;opacity:0;overflow:hidden;transform:translateY(14px);transition:max-height .7s cubic-bezier(.2,.7,.2,1),opacity .4s ease,transform .7s cubic-bezier(.2,.7,.2,1),margin .7s cubic-bezier(.2,.7,.2,1)}
.leader.open .ld-msg{max-height:220px;opacity:1;transform:none;margin-bottom:18px;transition-delay:.18s}
.ld-msg .qm{display:block;width:18px;height:auto;margin-bottom:10px;color:var(--sun)}
.ld-msg p{margin:0;max-width:38ch;font-size:15.5px;font-weight:300;line-height:1.5;color:rgba(255,255,255,.94);text-wrap:pretty}
.ld-msg .ld-tag{display:inline-block;margin-top:10px;padding:2px 7px;border:1px dashed rgba(255,255,255,.5);border-radius:6px;font:500 9.5px var(--f-mono);letter-spacing:.06em;text-transform:uppercase;color:rgba(255,255,255,.85)}
.leader:focus-visible{outline:2px solid var(--ink);outline-offset:3px;box-shadow:0 0 0 3px var(--sun)}
.ld-more{display:flex;width:max-content;margin:clamp(30px,4vw,48px) auto 0}
@media (max-width:1100px){ .leaders{height:460px} .leader.open{flex-grow:2} .ld-msg p{font-size:14.5px} }
@media (max-width:700px){
  .leaders{height:auto;overflow-x:auto;scroll-snap-type:x mandatory;margin-inline:calc(-1 * var(--g, 20px));padding-inline:var(--g, 20px);scroll-padding-inline:var(--g, 20px);gap:12px;scrollbar-width:none}
  .leaders::-webkit-scrollbar{display:none}
  .leader,.leader.open{flex:0 0 82%;height:470px;scroll-snap-align:start}
  .leader .ld-ph,.leader.open .ld-ph{transform:none}
  .ld-msg,.leader.open .ld-msg{max-height:none;opacity:1;transform:none;margin-bottom:14px}
  .leader::after,.leader.open::after{height:82%;background:linear-gradient(180deg,rgba(9,9,11,0) 0%,rgba(9,9,11,.7) 34%,rgba(9,9,11,.94) 100%)}
  .ld-msg p{font-size:14px}
}
@media (prefers-reduced-motion: reduce){.leader,.ld-ph,.ld-msg{transition:none}}

/* ---------- Solar systems: on-grid, off-grid, hybrid''')
rep("gsap.utils.toArray('.sol-grid .sol, .team > *, .t-deck, .post, .why-card')", "gsap.utils.toArray('.sol-grid .sol, .team > *, .leader, .t-deck, .post, .why-card')")

# ================= 2. Systems model, realistic build =================
a = s.index("if (hasThree){\n  const canvas = document.getElementById('anatCanvas'), stage = canvas.parentElement;")
b = s.index("\nif (hasGsap && !reduce){\n  ScrollTrigger.create({ trigger:'#anatomy'")
s = s[:a] + r'''if (hasThree){
  const canvas = document.getElementById('anatCanvas'), stage = canvas.parentElement;
  const S = makeScene(canvas), { scene, camera, key } = S;
  key.position.set(7.5, 12, 8); key.target.position.set(1, 0, -.5); scene.add(key.target);
  key.shadow.mapSize.set(2048, 2048);
  Object.assign(key.shadow.camera, { left:-8.5, right:8.5, top:7.5, bottom:-7.5, near:2, far:34 }); key.shadow.camera.updateProjectionMatrix();
  key.shadow.bias = -.0004; key.shadow.normalBias = .02;
  const rim = scene.children.find(o => o.isDirectionalLight && o !== key);
  const hemi = new THREE.HemisphereLight(0xdde7ff, 0x3a4630, .6); scene.add(hemi);
  const dayKey = new THREE.Color(0xfff0d6), nightKey = new THREE.Color(0x7f95d8);

  // ---- textures, drawn once on small canvases ----
  let seed = 11; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const cv = (w, h, draw) => { const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h); return c; };
  const tex = (c, rx = 1, ry = 1, srgb = true) => { const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rx, ry); t.anisotropy = 8; if (srgb) t.encoding = THREE.sRGBEncoding; return t; };
  const noiseC = cv(256, 256, (g, w, h) => { g.fillStyle = '#808080'; g.fillRect(0, 0, w, h); for (let k = 0; k < 9000; k++){ const v = 105 + rnd() * 50 | 0; g.fillStyle = `rgb(${v},${v},${v})`; g.fillRect(rnd() * w, rnd() * h, 1 + rnd() * 2, 1 + rnd() * 2); } });
  const grassC = cv(512, 512, (g, w, h) => { g.fillStyle = '#304524'; g.fillRect(0, 0, w, h);
    for (let k = 0; k < 26000; k++){ const x = rnd() * w, y = rnd() * h, l = 2 + rnd() * 5, q = 55 + rnd() * 55 | 0; g.strokeStyle = `rgba(${q * .55 | 0},${q},${q * .38 | 0},.55)`; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (rnd() - .5) * 2, y - l); g.stroke(); } });
  const paveC = cv(256, 256, (g, w, h) => { const n = 4, z = w / n; for (let p = 0; p < n; p++) for (let q = 0; q < n; q++){ const v = 172 + rnd() * 24 | 0; g.fillStyle = `rgb(${v},${v - 5},${v - 14})`; g.fillRect(p * z, q * z, z, z); }
    for (let k = 0; k < 3000; k++){ g.fillStyle = `rgba(90,84,76,${rnd() * .18})`; g.fillRect(rnd() * w, rnd() * h, 2, 2); }
    g.strokeStyle = '#7a756c'; g.lineWidth = 3; for (let p = 0; p <= n; p++){ g.beginPath(); g.moveTo(p * z, 0); g.lineTo(p * z, h); g.stroke(); g.beginPath(); g.moveTo(0, p * z); g.lineTo(w, p * z); g.stroke(); } });
  const woodC = cv(256, 256, (g, w, h) => { const n = 8, z = w / n; for (let p = 0; p < n; p++){ const v = rnd() * 18; g.fillStyle = `rgb(${132 + v | 0},${86 + v * .7 | 0},${50 + v * .4 | 0})`; g.fillRect(p * z, 0, z, h);
      for (let k = 0; k < 14; k++){ const x = p * z + rnd() * z; g.strokeStyle = `rgba(70,40,20,${.08 + rnd() * .12})`; g.lineWidth = 1; g.beginPath(); g.moveTo(x, 0); g.bezierCurveTo(x + 3, h * .3, x - 3, h * .6, x + 2, h); g.stroke(); }
      g.fillStyle = 'rgba(40,24,12,.55)'; g.fillRect(p * z, 0, 2, h); } });
  const ringC = cv(16, 256, (g, w, h) => { g.fillStyle = '#6f6352'; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y += 7 + rnd() * 6){ g.fillStyle = `rgba(38,30,22,${.35 + rnd() * .3})`; g.fillRect(0, y, w, 2); } });
  const frondC = cv(512, 128, (g, w, h) => { g.strokeStyle = '#4b5a2a'; g.lineWidth = 5; g.beginPath(); g.moveTo(0, h / 2); g.lineTo(w, h / 2); g.stroke();
    for (let x = 12; x < w - 6; x += 6){ const t = x / w, L = (h / 2 - 4) * (1 - t * .55) * (.82 + rnd() * .18), q = 68 + rnd() * 42 | 0; g.strokeStyle = `rgb(${q * .5 | 0},${q + 22},${q * .32 | 0})`; g.lineWidth = 3.4 * (1 - t * .5);
      [-1, 1].forEach(sd => { g.beginPath(); g.moveTo(x, h / 2); g.quadraticCurveTo(x + 10, h / 2 + sd * L * .5, x + 20, h / 2 + sd * L); g.stroke(); }); } });
  const glowC = cv(64, 64, g => { const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(.22, 'rgba(255,255,255,.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 64); });
  const aoC = cv(128, 128, (g, w, h) => { for (let k = 0; k < 24; k++){ const m = 3 + k * 1.7; g.fillStyle = 'rgba(255,255,255,.075)'; g.fillRect(m, m, w - 2 * m, h - 2 * m); } });
  const vigC = cv(256, 256, (g, w, h) => { const gr = g.createRadialGradient(w / 2, h / 2, w * .03, w / 2, h / 2, w * .17); gr.addColorStop(0, '#18181b'); gr.addColorStop(1, '#09090B'); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  const lampC = cv(16, 128, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, '#fff'); gr.addColorStop(1, '#5a3d22'); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  const pulseC = cv(256, 8, (g, w, h) => { const gr = g.createLinearGradient(0, 0, w, 0); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(.5, 'rgba(255,255,255,.1)'); gr.addColorStop(.84, 'rgba(255,255,255,.9)'); gr.addColorStop(.88, 'rgba(255,255,255,1)'); gr.addColorStop(.93, 'rgba(255,255,255,0)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, w, h); });

  // ---- materials ----
  const mats = [];
  const M = (o, env = 1) => { const m = new THREE.MeshStandardMaterial(Object.assign({ roughness:.85, metalness:0 }, o)); m.userData.env = env; mats.push(m); return m; };
  const bumpT = tex(noiseC, 3, 3, false);
  const plaster = M({ color:0xEFEDE8, bumpMap:bumpT, bumpScale:.004 }), plaster2 = M({ color:0xE3E0D9, bumpMap:bumpT, bumpScale:.004 });
  const concrete = M({ color:0x9E9B94, bumpMap:bumpT, bumpScale:.006, roughness:.95 }), poleConc = M({ color:0xA9A69F, bumpMap:bumpT, bumpScale:.006, roughness:.9 });
  const charcoal = M({ color:0x2B2B2F, roughness:.6 }), alu = M({ color:0x34353a, roughness:.38, metalness:.6 }), steel = M({ color:0xC6CAD0, roughness:.3, metalness:.85 });
  const armM = M({ color:0x55575c, roughness:.5, metalness:.6 }), porcelain = M({ color:0xF2F2EE, roughness:.25 }), whiteM = M({ color:0xF4F4F1, roughness:.35 }), meterM = M({ color:0xD9D9D4, roughness:.5 });
  const wood = M({ map:tex(woodC, 1, 1), roughness:.7 }), grass = M({ map:tex(grassC, 5, 3.5), roughness:1 }), tankM = M({ color:0x18181b, roughness:.5 });
  const trunkM = M({ map:tex(ringC, 1, 9), roughness:.95 }), leafM = M({ color:0x2f4a27, roughness:.95 });
  const frondM = M({ map:tex(frondC), alphaTest:.45, side:THREE.DoubleSide, roughness:.85 });
  const roadM = new THREE.MeshBasicMaterial({ map:tex(vigC), toneMapped:false });   // unlit: its edge is exactly the page colour, so the canvas never shows a seam
  const darkGlass = M({ color:0x15181d, roughness:.1, metalness:.3 });
  const glassM = M({ color:0x1b2330, roughness:.06, metalness:.15, emissive:0xF2A65A, emissiveMap:tex(lampC), emissiveIntensity:0 }, 1.4); glassM.toneMapped = false;   // warm lamp-light at night, not washed out
  const cellM = new THREE.MeshPhysicalMaterial({ map:cellTexture(), roughness:.28, metalness:.1, clearcoat:.5, clearcoatRoughness:.08 }); cellM.userData.env = .7; mats.push(cellM);
  const screenM = new THREE.MeshBasicMaterial({ color:0xF9C22E, toneMapped:false });
  const lampM = new THREE.MeshBasicMaterial({ color:0x2a2a2a, toneMapped:false });
  const paveM = (rx, ry) => M({ map:tex(paveC, rx, ry), roughness:.9 });

  // ---- helpers ----
  const G = new THREE.Group(); scene.add(G);
  const V = (x, y, z) => new THREE.Vector3(x, y, z);
  const mesh = (geo, m, x, y, z, parent = G, cast = true) => { const o = new THREE.Mesh(geo, m); o.position.set(x, y, z); o.castShadow = cast; o.receiveShadow = true; parent.add(o); return o; };
  const BX = (w, h, dd) => new THREE.BoxGeometry(w, h, dd);
  const RB = (w, h, dd, bv = .02) => {             // box with softly rounded edges, so light catches the corners
    const r = Math.max(.0005, Math.min(bv * .8, (Math.min(w, h) - 2 * bv) / 2 - .0005));
    const g = new THREE.ExtrudeGeometry(roundedRect(w - 2 * bv, h - 2 * bv, r), { depth:Math.max(.001, dd - 2 * bv), bevelEnabled:true, bevelThickness:bv, bevelSize:bv, bevelSegments:2, curveSegments:3 });
    g.translate(0, 0, -(dd - 2 * bv) / 2); return g; };
  const glowT = tex(glowC, 1, 1, false);
  const glow = (x, y, z, sc, col, parent = G) => { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map:glowT, color:col, transparent:true, blending:THREE.AdditiveBlending, depthWrite:false, toneMapped:false, opacity:0 })); sp.position.set(x, y, z); sp.scale.set(sc, sc, sc); parent.add(sp); return sp; };
  const aoT = tex(aoC, 1, 1, false);
  const ao = (w, dd, x, z, o = .5) => { const m = new THREE.MeshBasicMaterial({ color:0x000000, transparent:true, opacity:o, alphaMap:aoT, depthWrite:false }); const p = new THREE.Mesh(new THREE.PlaneGeometry(w, dd).rotateX(-Math.PI / 2), m); p.position.set(x, .013, z); p.renderOrder = 1; G.add(p); return m; };

  // ---- ground and plot ----
  mesh(new THREE.PlaneGeometry(44, 44).rotateX(-Math.PI / 2), roadM, .85, -.04, .1, G, false);   // dark ground that fades into the page
  mesh(BX(10.3, .08, 7), grass, .85, -.04, .1, G, false);
  mesh(BX(1.0, .03, 2.25), paveM(1, 2.25), 1.5, .005, 2.45, G, false);          // path from the gate
  mesh(BX(4.2, .05, .85), paveM(4.2, .85), -1.2, .015, 1.72, G, false);         // sit-out
  mesh(BX(.75, .04, .95), paveM(.75, .95), 3.5, .01, .55, G, false);            // battery pad
  const wallH = .42;
  const cw = (w, dd, x, z) => { mesh(BX(w, wallH, dd), plaster2, x, wallH / 2, z); mesh(BX(w + .03, .035, dd + .03), charcoal, x, wallH + .017, z, G, false); };
  cw(10.3, .1, .85, -3.35); cw(.1, 7, -4.25, .1); cw(.1, 7, 5.95, .1); cw(5.2, .1, -1.65, 3.55); cw(3.9, .1, 4.0, 3.55);
  [.95, 2.05].forEach(x => { mesh(RB(.18, .62, .18, .02), plaster, x, .31, 3.55); mesh(BX(.22, .04, .22), charcoal, x, .64, 3.55, G, false); mesh(BX(.1, .05, .1), lampM, x, .685, 3.55, G, false); });
  // hedge and shrubs
  mesh(RB(3.6, .34, .32, .1), leafM, -2.2, .17, 3.25);
  const bush = (x, z, k) => [[0, 0, 1], [.2, .06, .8], [-.17, .04, .75]].forEach(([dx, dz, f]) => mesh(new THREE.IcosahedronGeometry(.26 * k * f, 2), leafM, x + dx * k, .2 * k * f, z + dz * k));
  bush(5.45, 3.0, 1); bush(5.5, -2.8, 1.1); bush(-3.8, -.6, .9);

  // ---- the house: a contemporary two-storey villa with a single-storey entrance block ----
  mesh(RB(4.0, 3.3, 3.0, .015), plaster, -1.2, 1.65, -.2);
  mesh(BX(4.04, .05, 3.04), charcoal, -1.2, 1.62, -.2, G, false);                 // floor line
  const win = (w, h, x, y, z, mull = []) => { mesh(BX(w + .1, h + .1, .05), alu, x, y, z, G, false); mesh(BX(w, h, .05), glassM, x, y, z + .012, G, false); mull.forEach(mx => mesh(BX(.03, h, .06), alu, mx, y, z + .016, G, false)); };
  win(1.45, 1.12, -2.25, .6, 1.3, [-2.25]);                                     // sliding door to the sit-out
  win(.85, .7, -.65, .85, 1.3);
  win(2.3, .65, -1.85, 2.35, 1.3, [-2.42, -1.85, -1.28]);                       // first-floor ribbon window
  mesh(BX(2.7, .06, .38), plaster, -1.85, 2.8, 1.48);                           // sunshade
  mesh(BX(1.15, 1.2, .04), darkGlass, .1, 2.4, 1.3, G, false);
  for (let k = 0; k < 10; k++) mesh(BX(.05, 1.3, .12), wood, -.45 + k * .125, 2.4, 1.36);   // timber louvres
  win(.06, .01, 0, 0, -9);                                                      // (keeps glass material warm-up simple)
  mesh(BX(.05, .65, 1.05), alu, .8, 2.35, -.65, G, false); mesh(BX(.05, .55, .95), glassM, .812, 2.35, -.65, G, false);   // side window
  mesh(BX(4.0, .04, 3.0), concrete, -1.2, 3.32, -.2, G, false);                 // roof slab
  const pp = (w, dd, x, z) => { mesh(BX(w, .24, dd), plaster, x, 3.42, z); mesh(BX(w + .03, .03, dd + .03), charcoal, x, 3.555, z, G, false); };
  pp(4.0, .08, -1.2, 1.26); pp(4.0, .08, -1.2, -1.66); pp(.08, 3.0, -3.16, -.2); pp(.08, 3.0, .76, -.2);
  mesh(BX(.6, .08, .6), charcoal, .38, 3.38, -1.25);                            // water tank on its stand
  mesh(new THREE.CylinderGeometry(.25, .25, .5, 28), tankM, .38, 3.67, -1.25);
  mesh(new THREE.CylinderGeometry(.11, .11, .05, 20), tankM, .38, 3.94, -1.25);
  // entrance block
  mesh(RB(1.8, 1.7, 2.2, .015), plaster2, 1.7, .85, .2);
  mesh(RB(2.15, .12, 2.65, .015), charcoal, 1.75, 1.76, .38);
  mesh(BX(.6, 1.18, .05), wood, 1.3, .59, 1.3, G, false); mesh(BX(.025, .3, .04), steel, 1.53, .62, 1.33, G, false);   // front door
  win(.22, 1.08, 1.83, .59, 1.3);
  mesh(BX(.52, 1.5, .04), wood, 2.3, .78, 1.31, G, false);                     // timber cladding
  mesh(BX(.07, .15, .05), lampM, .92, 1.15, 1.33, G, false);                    // wall lamp by the door
  // solar array on a raised GI frame (the Kerala way: the terrace stays usable underneath)
  const pGeo = BX(.6, .035, 1.2), pMats = [steel, steel, cellM, steel, steel, steel], tilt = .24, yP = 3.84;
  [-1.0, .35].forEach(zc => {
    for (let c = 0; c < 5; c++){ const g = new THREE.Group(); g.position.set(-2.95 + c * .66, yP, zc); g.rotation.x = tilt; G.add(g); mesh(pGeo, pMats, 0, 0, 0, g); }
    const dz = .52, yF = yP - .6 * Math.sin(tilt) - .035, yB = yP + .6 * Math.sin(tilt) - .035;
    mesh(BX(3.28, .035, .035), steel, -1.63, yF, zc + dz); mesh(BX(3.28, .035, .035), steel, -1.63, yB, zc - dz);
    [-3.22, -1.63, -.04].forEach(x => { mesh(BX(.035, yF - 3.34, .035), steel, x, (yF + 3.34) / 2, zc + dz); mesh(BX(.035, yB - 3.34, .035), steel, x, (yB + 3.34) / 2, zc - dz); });
  });
  // inverter, net meter, service bracket
  mesh(RB(.16, .6, .44, .02), whiteM, 2.69, 1.0, .45);
  mesh(BX(.01, .07, .18), screenM, 2.772, 1.14, .45, G, false);
  const meter = new THREE.Group(); G.add(meter);
  mesh(RB(.13, .34, .26, .015), meterM, 2.67, 1.0, -.4, meter); mesh(BX(.01, .1, .15), darkGlass, 2.737, 1.06, -.4, meter, false);
  mesh(BX(.1, .06, .25), charcoal, 2.65, 1.62, -.45, meter);
  // battery bank with a charge gauge
  const batt = new THREE.Group(); batt.position.set(3.5, .03, .55); G.add(batt);
  mesh(RB(.42, 1.04, .64, .03), whiteM, 0, .52, 0, batt);
  mesh(BX(.43, .025, .65), charcoal, 0, .9, 0, batt, false);
  const leds = [0, 1, 2, 3, 4].map(k => mesh(BX(.01, .1, .2), new THREE.MeshBasicMaterial({ color:0x2a2a2e, toneMapped:false }), .214, .2 + k * .13, 0, batt, false));
  // KSEB-style concrete pole on the road outside the compound wall
  const pole = new THREE.Group(); pole.position.set(6.75, 0, -2.0); G.add(pole);
  const pg = new THREE.CylinderGeometry(.055, .1, 4.9, 4, 1); pg.rotateY(Math.PI / 4); mesh(pg, poleConc, 0, 2.45, 0, pole);
  const arm = mesh(BX(1.3, .06, .07), armM, 0, 4.62, 0, pole); arm.rotation.y = Math.PI / 4;
  [-.55, .55].forEach(t => { mesh(new THREE.CylinderGeometry(.028, .045, .13, 10), porcelain, t * .707, 4.715, -t * .707, pole); });
  const ins = V(6.75 - .389, 4.79, -2.0 + .389), ins2 = V(6.75 + .389, 4.79, -2.0 - .389);
  // coconut palms
  const frondGeo = (() => { const L = 1.55, W = .62, g = new THREE.PlaneGeometry(L, W, 12, 2); g.translate(L / 2, 0, 0); g.rotateX(-Math.PI / 2); const p = g.attributes.position;
    for (let k = 0; k < p.count; k++){ const x = p.getX(k), z = p.getZ(k), t = x / L; p.setY(k, .42 * t - 1.05 * t * t - Math.abs(z) * .35 * (1 - t * .5)); p.setZ(k, z * (1 - t * .55)); }
    g.computeVertexNormals(); return g; })();
  const palm = (x, z, h, lean, dx, dz) => {
    const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = Math.atan2(-dz, dx); G.add(g);
    const tg = new THREE.CylinderGeometry(.05, .085, h, 10, 16, true); tg.translate(0, h / 2, 0);
    const p = tg.attributes.position; for (let k = 0; k < p.count; k++){ const y = p.getY(k); p.setX(k, p.getX(k) + lean * Math.pow(y / h, 2)); } tg.computeVertexNormals();
    mesh(tg, trunkM, 0, 0, 0, g);
    for (let k = 0; k < 13; k++){ const f = new THREE.Mesh(frondGeo, frondM); f.position.set(lean, h, 0); f.rotation.set(0, k / 13 * Math.PI * 2 + rnd() * .3, .35 - (k % 3) * .22); f.receiveShadow = true; g.add(f); }
    [[.08, 0], [-.06, .06], [0, -.08]].forEach(([ox, oz]) => mesh(new THREE.SphereGeometry(.065, 10, 8), M({ color:0x5d6a2c, roughness:.7 }), lean + ox, h - .1, oz, g));
  };
  palm(-3.6, -2.7, 4.4, .55, -.5, -.8); palm(-3.85, 2.75, 3.7, .7, -.75, .55);

  // ---- contact shadows: soft darkening where things meet the ground ----
  ao(4.7, 3.7, -1.2, -.2, .55); ao(2.4, 2.8, 1.7, .2, .5); ao(.6, .6, 6.75, -2.0, .45);
  const aoBatt = ao(.75, .95, 3.5, .55, .5);

  // ---- night lights ----
  const doorLight = new THREE.PointLight(0xffb468, 0, 3.2, 2); doorLight.position.set(1.15, 1.0, 1.75); G.add(doorLight);
  const spill1 = new THREE.PointLight(0xffb468, 0, 4.5, 2); spill1.position.set(-2.25, .8, .9); G.add(spill1);
  const spill2 = new THREE.PointLight(0xffb468, 0, 4.5, 2); spill2.position.set(-1.5, 2.35, .9); G.add(spill2);
  const glows = [glow(.92, 1.15, 1.4, .42, 0xffa64d), glow(.95, .7, 3.56, .32, 0xffa64d), glow(2.05, .7, 3.56, .32, 0xffa64d)];
  const invGlow = glow(2.79, 1.14, .45, .28, 0xF9C22E);

  // ---- cables, with light pulses running inside them ----
  const poly = pts => { const c = new THREE.CurvePath(); for (let k = 1; k < pts.length; k++) c.add(new THREE.LineCurve3(pts[k - 1], pts[k])); return c; };
  const pvC = poly([V(.05, 3.64, .45), V(.86, 3.64, .45), V(.86, 1.86, .45), V(2.87, 1.86, .45), V(2.87, 1.4, .45), V(2.71, 1.4, .45), V(2.71, 1.3, .45)]);
  const homeC = poly([V(2.69, .7, .6), V(2.66, .46, .6), V(2.66, .46, 1.36), V(1.99, .46, 1.36)]);
  const battC = poly([V(2.69, .7, .3), V(2.69, .06, .3), V(3.29, .06, .3)]);
  const gridC = poly([V(2.69, 1.05, .22), V(2.69, 1.05, -.4), V(2.69, 1.62, -.4)]);
  gridC.add(new THREE.QuadraticBezierCurve3(V(2.69, 1.62, -.4), V(4.53, 2.55, -1.0), ins));
  const neutralC = new THREE.QuadraticBezierCurve3(V(2.69, 1.62, -.5), V(4.92, 2.55, -1.44), ins2);
  const pulseT = tex(pulseC, 1, 1, false);
  const flows = [pvC, homeC, battC, gridC].map(curve => {
    const len = curve.getLength(), segs = Math.max(48, Math.round(len * 40));
    const cm = M({ color:0x1d1d20, roughness:.5, emissive:0xF9C22E, emissiveIntensity:0, transparent:true });
    mesh(new THREE.TubeGeometry(curve, segs, .02, 6, false), cm, 0, 0, 0, G, false);
    const t = pulseT.clone(); t.needsUpdate = true;
    const pm = new THREE.MeshBasicMaterial({ map:t, color:0xF9C22E, transparent:true, opacity:0, blending:THREE.AdditiveBlending, depthWrite:false, toneMapped:false });
    const pt = new THREE.Mesh(new THREE.TubeGeometry(curve, segs, .038, 8, false), pm); pt.renderOrder = 4; G.add(pt);
    return { len, cm, pm, t, off: rnd() };
  });
  const neutralM = M({ color:0x1d1d20, roughness:.5, transparent:true }); mesh(new THREE.TubeGeometry(neutralC, 64, .016, 6, false), neutralM, 0, 0, 0, G, false);
  const YEL = new THREE.Color(0xF9C22E), WHT = new THREE.Color(0xF4F4F5), col = new THREE.Color(), tmp = V(0, 0, 0);
  const lampOff = new THREE.Color(0x2a2a2a), lampOn = new THREE.Color(0xffc27a);
  const anchors = { meter:V(2.74, 1.0, -.4), pole:ins, batt:V(3.72, .85, .55), inv:V(2.78, 1.05, .45) };

  const tag = document.getElementById('anatTag'), tagB = tag.querySelector('b'), tagS = tag.querySelector('span');
  const clock = document.getElementById('sysClock'), clockT = document.getElementById('sysTime'), clockS = document.getElementById('sysSolar');
  let tagKey = '', tagTpl = '', swapAt = 0, lastT = performance.now(), visible = false;
  const cam = { az:.32, el:.5, r:26, init:false };
  new IntersectionObserver(es => { visible = es[0].isIntersecting; if (visible) S.resize(); }, { rootMargin:'600px 0px' }).observe(canvas);   // start drawing (and compiling) a little before it scrolls in
  (function loop(now){
    requestAnimationFrame(loop); if (!visible) return;
    now = now || performance.now(); const dt = Math.min(.05, (now - lastT) / 1000); lastT = now;
    const st = sysState(sys.p), n = st.night, mob = isMobile();
    // light: warm midday sun, then a cool moonlit evening with the house lights on
    key.intensity = 2.1 - 1.8 * n; key.color.copy(dayKey).lerp(nightKey, n);
    if (rim) rim.intensity = .45 * (1 - n);
    hemi.intensity = .6 - .45 * n;
    mats.forEach(m => m.envMapIntensity = m.userData.env * (1 - .75 * n));
    const lit = ss(.25, 1, n);
    glassM.emissiveIntensity = 1.1 * lit;
    doorLight.intensity = 3.2 * lit; spill1.intensity = 5 * lit; spill2.intensity = 4 * lit;
    lampM.color.copy(lampOff).lerp(lampOn, lit);
    glows.forEach(g => g.material.opacity = .6 * lit);
    invGlow.material.opacity = .35 + .25 * n;
    // the battery and the grid connection appear only in the systems that have them
    const vb = ss(0, 1, st.vb), vg = ss(0, 1, st.vg);
    batt.visible = vb > .01; batt.scale.set(1, Math.max(.001, vb), 1); aoBatt.opacity = .5 * vb;
    pole.visible = vg > .01; pole.scale.set(1, Math.max(.001, vg), 1);
    meter.visible = vg > .01; meter.scale.set(Math.max(.001, vg), 1, 1);
    const wire = ss(.4, 1, vg); neutralM.opacity = wire; flows[3].cm.opacity = wire;
    const level = Math.round(st.charge / 20 + .3);
    leds.forEach((l, k) => l.material.color.set(k < level ? 0xF9C22E : 0x2a2a2e));
    // power moving through the cables
    const gridHome = st.w[0] * n;
    flows.forEach((fl, k) => {
      const v = st.f[k], a = Math.min(1, Math.abs(v)) * (k === 3 ? wire : 1), dir = v >= 0 ? 1 : -1;
      fl.cm.emissiveIntensity = .3 * a;
      fl.pm.opacity = a; fl.pm.visible = a > .01;
      if (k === 1) col.copy(YEL).lerp(WHT, gridHome); else if (k === 3 && dir < 0) col.copy(WHT); else col.copy(YEL);
      fl.pm.color.copy(col);
      if (!reduce) fl.off -= dt * 1.5;
      fl.t.repeat.x = dir * fl.len / .6; fl.t.offset.x = fl.off;
    });
    // camera: a slow orbit across the whole scroll, fitted to the stage
    const r = stage.getBoundingClientRect(), asp = r.width / Math.max(1, r.height), tf = .2493;
    const tAz = mob ? .26 + .22 * sys.p : .3 + .5 * sys.p, tEl = mob ? .6 : .48 - .06 * sys.p;
    const tR = Math.max((mob ? 5.4 : 6.9) / (tf * asp), (mob ? 3.9 : 4.6) / tf);
    if (!cam.init) Object.assign(cam, { az:tAz, el:tEl, r:tR, init:true });
    const e = 1 - Math.exp(-dt * 5);
    cam.az += (tAz - cam.az) * e; cam.el += (tEl - cam.el) * e; cam.r += (tR - cam.r) * e;
    const tx = mob ? 1.4 : 1.1, ty = mob ? 1.15 : 1.45, tz = -.15;
    camera.position.set(tx + cam.r * Math.cos(cam.el) * Math.sin(cam.az), ty + cam.r * Math.sin(cam.el), tz + cam.r * Math.cos(cam.el) * Math.cos(cam.az));
    camera.lookAt(tx, ty, tz);
    S.renderer.render(scene, camera);
    // clock
    const h = st.hour, hh = Math.floor(h), mm = Math.floor((h - hh) * 4) * 15;
    const tt = String(hh).padStart(2, '0') + ':' + String(mm).padStart(2, '0'), ts = 'Solar ' + st.solar.toFixed(1) + ' kW';
    if (clockT.textContent !== tt) clockT.textContent = tt;
    if (clockS.textContent !== ts) clockS.textContent = ts;
    clock.classList.toggle('night', n > .5);
    // label on the part doing the work right now
    const kk = st.step + (n > .5 ? 'n' : 'd'), T = SYS_TAGS[st.step][n > .5 ? 1 : 0];
    if (kk !== tagKey){ tagKey = kk; swapAt = now + 180; tag.style.opacity = 0; }
    if (swapAt && now >= swapAt){ swapAt = 0; tagB.textContent = T[1]; tagTpl = T[2]; }
    if (tagTpl){ const txt = tagTpl.replace('{b}', st.charge); if (tagS.textContent !== txt) tagS.textContent = txt; }
    const hidden = (T[0] === 'batt' && vb < .9) || ((T[0] === 'meter' || T[0] === 'pole') && vg < .9) || (st.u < .16 && st.step > 0);
    if (!swapAt) tag.style.opacity = hidden || (sys.p < .003 && !reduce) ? 0 : 1;
    tmp.copy(anchors[T[0]]).project(camera);
    let x = (tmp.x + 1) / 2 * r.width; const y = (1 - tmp.y) / 2 * r.height;
    const flip = x + tag.offsetWidth > r.width - 8; tag.classList.toggle('flip', flip);
    if (flip) x = Math.max(4, x - tag.offsetWidth);
    tag.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px)`;
  })();
}''' + s[b:]

# ================= 3. Solutions: titles only, no descriptions (client request) =================
import re
i = s.index('<div class="sol-grid">'); j = s.index('</section>', i)
seg, k = re.subn(r'(<article class="sol">.*?</h3>)<p>.*?</p>', r'\1', s[i:j], flags=re.S); assert k == 8, k
s = s[:i] + seg + s[j:]
a = s.index('/* ---------- Solutions on phones: tap a row to open its description (one open at a time) ---------- */')
b = s.index("  setup();\n})();\n", a) + len("  setup();\n})();\n")
s = s[:a] + s[b:]
rep('.sol{min-height:300px}', '.sol{min-height:230px}')
rep("  /* solutions on phones: a compact list, tap a row to read more */", "  /* solutions on phones: a compact list of services */")
rep("  .sol{display:grid;grid-template-columns:36px minmax(0,1fr) 20px;column-gap:14px;align-items:center;min-height:0;padding:16px 2px;border:0;border-bottom:1px solid var(--line);border-radius:0;background:transparent;cursor:pointer;-webkit-tap-highlight-color:transparent}",
    "  .sol{display:grid;grid-template-columns:36px minmax(0,1fr);column-gap:14px;align-items:center;min-height:0;padding:16px 2px;border:0;border-bottom:1px solid var(--line);border-radius:0;background:transparent}")
rep('  .sol::after{content:"";grid-column:3;grid-row:1;justify-self:center;width:9px;height:9px;border-right:1.5px solid var(--ink);border-bottom:1.5px solid var(--ink);transform:translateY(-3px) rotate(45deg);transition:transform .35s ease}\n  .sol.open::after{transform:translateY(2px) rotate(225deg)}\n', '')

# ================= 4. Accessibility pass (WCAG 2.2 AA, A11y Enforcer + axe-core) =================
rep('  --slate:#71717A', '  --slate:#66666E')                                                       # 1.4.3: 5.2:1 on the grey panels (was 4.4:1)
rep('.nav.on-dark~.mnav a span{color:#71717A}', '.nav.on-dark~.mnav a span{color:#A1A1AA}')        # 1.4.3 on the dark menu
rep('background:#128C4A;color:#fff', 'background:#128748;color:#fff')                              # 1.4.3: 4.6:1 (was 4.3:1)
rep('.btn:focus-visible,a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{outline:2px solid var(--amber);outline-offset:3px}',
    '.btn:focus-visible,a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible,[tabindex]:focus-visible{outline:2px solid var(--ink);outline-offset:3px;box-shadow:0 0 0 3px var(--sun)}   /* two-tone ring: visible on light and dark sections (1.4.11, 2.4.7) */')
rep('.bill input:hover,.bill input:focus{border-bottom-color:rgba(255,255,255,.3)}', '.bill input:hover,.bill input:focus{border-bottom-color:rgba(255,255,255,.3)}\n.bill input:focus-visible{border-bottom:2px solid var(--sun)}')
rep('input[type=range]:focus-visible::-webkit-slider-thumb{', 'input[type=range]:focus-visible::-moz-range-thumb{box-shadow:0 0 0 1px var(--sun),0 0 0 8px rgba(249,194,46,.3)}\ninput[type=range]:focus-visible::-webkit-slider-thumb{')
rep('.foot-top h4{', '.foot-top h3{')
for k in ('Company', 'Solutions', 'Contact'):
    rep(f'<div><h4>{k}</h4>', f'<div><h3>{k}</h3>')                                                 # 1.3.1 heading order
rep('<a class="wa" href="https://wa.me/919946207738"', '<aside aria-label="WhatsApp chat"><a class="wa" href="https://wa.me/919946207738"')
a = s.index('<aside aria-label="WhatsApp chat"><a class="wa"'); b = s.index('</a>', a) + 4
s = s[:b] + '</aside>' + s[b:]                                                                       # content inside a landmark
rep('<div class="proj-track" id="projTrack">', '<div class="proj-track" id="projTrack" tabindex="0" role="region" aria-label="Featured projects, scroll sideways">')   # 2.1.1 keyboard scrolling
rep('html{scroll-behavior:auto}', 'html{scroll-behavior:auto;scroll-padding-top:110px}   /* focused items never hide under the floating nav (2.4.11) */')
rep('<div class="form-ok" id="formOk" hidden>', '<p class="form-err" id="formErr" role="alert" hidden>Please add your name and phone number so we can call you back.</p>\n      <div class="form-ok" id="formOk" role="status" hidden>')
rep('.form-ok{grid-column:1/-1;', '.form-err{grid-column:1/-1;margin:0;font-size:14px;font-weight:500;color:#B42318}\n.form-ok{grid-column:1/-1;')
rep("""  const n = document.getElementById('fName'), p = document.getElementById('fPhone');
  if (!n.value.trim() || !p.value.trim()) { (n.value.trim() ? p : n).focus(); return; }
  document.getElementById('formOk').hidden = false;""",
"""  const n = document.getElementById('fName'), p = document.getElementById('fPhone'), err = document.getElementById('formErr');
  const bad = [n, p].filter(f => !f.value.trim());
  [n, p].forEach(f => { const b = bad.includes(f); f.setAttribute('aria-invalid', String(b)); if (b) f.setAttribute('aria-describedby', 'formErr'); else f.removeAttribute('aria-describedby'); });
  err.hidden = !bad.length;                                         // 3.3.1: say what is missing, not just move focus
  if (bad.length){ bad[0].focus(); return; }
  document.getElementById('formOk').hidden = false;""")
rep("  if (open && !reduce){ navPill.classList.remove('jelly'); void navPill.offsetWidth; navPill.classList.add('jelly'); }\n}",
    "  if (open && !reduce){ navPill.classList.remove('jelly'); void navPill.offsetWidth; navPill.classList.add('jelly'); }\n  if (open) setTimeout(() => { const f = mnav.querySelector('a'); if (f) f.focus({ preventScroll:true }); }, 60);   // keyboard users land in the menu\n}")
rep("const hasGsap = !!window.gsap, hasThree = !!window.THREE;", "if (!document.documentElement.lang) document.documentElement.lang = 'en';   // 3.1.1 language of page\nconst hasGsap = !!window.gsap, hasThree = !!window.THREE;")

# ---- accessibility pass, round 2: text over video/photos, form fields, chart label, target size ----
rep('.film-kick{display:block;font:500 12px var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.8)}',
    '.film-kick{display:block;font:500 12px var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:#fff;text-shadow:0 1px 10px rgba(0,0,0,.55)}')
rep('.film::after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(5,7,12,0) 45%,rgba(5,7,12,.82) 100%)}',
    '.film::after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(5,7,12,0) 34%,rgba(5,7,12,.55) 58%,rgba(5,7,12,.88) 100%)}   /* keeps the caption readable over any frame (1.4.3) */')
rep('.ga-label span{font:500 12px var(--f-mono);letter-spacing:.06em;color:rgba(255,255,255,.7)}', '.ga-label span{font:500 12px var(--f-mono);letter-spacing:.06em;color:rgba(255,255,255,.92)}')
rep('.ga-kick{display:block;font:500 12px var(--f-mono);letter-spacing:.08em;color:rgba(255,255,255,.7)}', '.ga-kick{display:block;font:500 12px var(--f-mono);letter-spacing:.08em;color:rgba(255,255,255,.92)}')
rep('.ga-label{opacity:0}', '.ga-label{opacity:0}\n.ga-label,.ga-body,.film-copy{text-shadow:0 1px 2px rgba(0,0,0,.55),0 0 14px rgba(0,0,0,.45)}\n.ga-body .btn,.film-copy .btn{text-shadow:none}   /* soft halo: small labels stay readable over bright parts of a photo or video (1.4.3) */')
rep('.cost-lbl{fill:var(--on-dark-muted);font:500 11px var(--f-body)}', '.cost-lbl{fill:#D4D4D8;font:500 11px var(--f-body)}')
rep('form.enq input,form.enq select,form.enq textarea{width:100%;font:400 16px var(--f-body);color:var(--ink);background:var(--paper);border:1px solid var(--line);',
    'form.enq input,form.enq select,form.enq textarea{width:100%;font:400 16px var(--f-body);color:var(--ink);background:var(--paper);border:1px solid #8A8A93;')   # 1.4.11: field edges 3.4:1
rep('.contact-info a{color:inherit;text-decoration:none;overflow-wrap:anywhere}', '.contact-info a{color:inherit;text-decoration:none;overflow-wrap:anywhere;display:inline-block;padding-block:2px}\nform.enq ::placeholder{color:var(--muted);opacity:1}')

# ================= 5. Logo on light backgrounds: black instead of blue (user, 23 Oct) =================
rep('<img class="lg-c" src="{{LOGO}}"', '<img class="lg-c" src="{{LOGO_BLACK}}"')

# ---- Our people: interaction for the reference layout (hover, tap or tab opens a card) ----
rep("/* ---------- Enquiry form (preview) ---------- */", """/* ---------- Our people: the card you point at, tap or tab to opens wider and shows its message ---------- */
(function(){
  const wrap = document.querySelector('.leaders'); if (!wrap) return;
  const cards = [...wrap.querySelectorAll('.leader')];
  const open = c => cards.forEach(k => k.classList.toggle('open', k === c));
  cards.forEach(c => { c.addEventListener('mouseenter', () => open(c)); c.addEventListener('focusin', () => open(c)); c.addEventListener('click', () => open(c)); });
  wrap.addEventListener('mouseleave', () => { if (!wrap.contains(document.activeElement)) open(null); });
  wrap.addEventListener('focusout', e => { if (!wrap.contains(e.relatedTarget)) open(null); });
})();

/* ---------- Enquiry form (preview) ---------- */""")
rep("""prevent: node => !!(node.matches && node.matches('.proj-track, input[type="range"], .sav-chart, .film-tabs'))""",
    """prevent: node => !!(node.matches && (node.matches('.proj-track, input[type="range"], .sav-chart, .film-tabs') || (innerWidth <= 700 && node.matches('.leaders'))))""")

# ================= 6. Heading: "Reasons to choose us" becomes "About us" (user, 23 Oct) =================
rep('<h2>Reasons to <em>choose us</em></h2>', '<h2>About <em>us</em></h2>')

# ================= 7. Multi-page: About Us now has its own page =================
rep('<a href="#about">About Us</a>', '<a href="about.html">About Us</a>')
rep('<a href="#about" style="--i:0">About Us', '<a href="about.html" style="--i:0">About Us')
rep('<a class="text-link" href="#about">Discover our story', '<a class="text-link" href="about.html">Discover our story')
rep('<div><h3>Company</h3><a href="#about">About us</a>', '<div><h3>Company</h3><a href="about.html">About us</a>')
# ================= 8. Multi-page: Solutions has its own page =================
rep('<a href="#solutions">Solutions</a>', '<a href="solutions.html">Solutions</a>')
rep('<a href="#solutions" style="--i:1">Solutions', '<a href="solutions.html" style="--i:1">Solutions')
rep('<div><h3>Solutions</h3><a href="#solutions">Residential solar</a><a href="#solutions">Commercial &amp; industrial</a><a href="#solutions">Battery &amp; inverters</a><a href="#solutions">Lighting</a></div>',
    '<div><h3>Solutions</h3><a href="solutions.html#residential">Residential solar</a><a href="solutions.html#commercial">Commercial &amp; industrial</a><a href="solutions.html#storage">Battery &amp; inverters</a><a href="solutions.html#lighting">Lighting</a></div>')
for name, sid in [('Residential Solar', 'residential'), ('Commercial &amp; Industrial Solar', 'commercial'), ('Lithium Battery &amp; Inverter Solutions', 'storage'),
                  ('Hybrid Solar &amp; Energy Storage', 'hybrid'), ('Manufacturing', 'manufacturing'), ('Indoor &amp; Outdoor Lighting', 'lighting'),
                  ('Energy Consultancy', 'consultancy'), ('Operations &amp; Maintenance', 'maintenance')]:
    rep(f'</span><h3>{name}</h3>', f'</span><h3><a href="solutions.html#{sid}">{name}</a></h3>')
rep("""        <svg class="ico" viewBox="0 0 44 44" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M27 8a8 8 0 0 0-9.5 10.5L7 29l4 4 10.5-10.5A8 8 0 0 0 32 13l-5 5-4-1-1-4z"/></svg></article>
    </div>""", """        <svg class="ico" viewBox="0 0 44 44" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M27 8a8 8 0 0 0-9.5 10.5L7 29l4 4 10.5-10.5A8 8 0 0 0 32 13l-5 5-4-1-1-4z"/></svg></article>
    </div>
    <a class="text-link sol-all" href="solutions.html">Explore all solutions <svg class="arr" width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 9h10M10 5l4 4-4 4"/></svg></a>""")
rep('.sol .ico{width:44px;height:44px;margin-top:auto;color:var(--sun)}',
    '.sol .ico{width:44px;height:44px;margin-top:auto;color:var(--sun)}\n'
    '.sol{position:relative}.sol h3 a{color:inherit;text-decoration:none}\n'
    '.sol h3 a::after{content:"";position:absolute;inset:0;border-radius:14px}   /* the whole card opens its solution */\n'
    '.sol h3 a:focus-visible{outline:none;box-shadow:none}\n'
    '.sol:has(a:focus-visible){outline:2px solid var(--ink);outline-offset:3px;box-shadow:0 0 0 3px var(--sun)}\n'
    '.sol-all{margin-top:28px}')

# ================= 9. Keyboard fixes found on the Solutions audit (apply to every page) =================
# FAQ questions get the same two-tone focus ring as links and buttons (2.4.7)
rep('.btn:focus-visible,a:focus-visible,button:focus-visible,input:focus-visible,', '.btn:focus-visible,a:focus-visible,button:focus-visible,summary:focus-visible,input:focus-visible,')
# in-page links: re-sync smooth scroll with the real scroll position first (focus can move the page natively)
rep("if (lenis) lenis.scrollTo(el, { offset: -10,", "if (lenis) { lenis.scrollTo(scrollY, { immediate: true }); lenis.scrollTo(el, { offset: -10,")
rep("easing: t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2 }); else el.scrollIntoView", "easing: t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2 }); } else el.scrollIntoView")

# ================= 10. Tagline is "Powering your tomorrow" (user, 23 Oct) =================
rep('<div><h2>Powering<br><em style="color:var(--sun)">Tomorrow.</em></h2></div>', '<div><h2>Powering<br><em style="color:var(--sun)">Your Tomorrow.</em></h2></div>')
rep('<h1 id="heroTitle">Powering <em>Tomorrow</em></h1>', '<h1 id="heroTitle">Powering <em>Your Tomorrow</em></h1>')
rep('.hero-copy h1 em{color:var(--sun)}', '.hero-copy h1 em{color:var(--sun);white-space:nowrap}')   # keep "Your Tomorrow" together on phones

# ================= 11. Homepage solutions: index list + illustration plate (user: "make something creative") =================
import sys as _sys, re as _re
_sys.path.insert(0, d)
from iso import scenes as _scenes, ISO_CSS as _ISO_CSS
_SC = _scenes()
def _uniq(svg, suffix):
    for i in ('lgCone', 'lgBeam', 'omClip'): svg = svg.replace(f'id="{i}"', f'id="{i}{suffix}"').replace(f'url(#{i})', f'url(#{i}{suffix})')
    return svg
def _hide(svg): return _re.sub(r'role="img" aria-label="[^"]*"', 'aria-hidden="true" focusable="false"', svg)
_SI = [('residential', 'Homes', 'Residential Solar'), ('commercial', 'Businesses', 'Commercial &amp; Industrial Solar'),
       ('storage', 'Storage', 'Lithium Battery &amp; Inverter Solutions'), ('hybrid', 'Solar + storage', 'Hybrid Solar &amp; Energy Storage'),
       ('manufacturing', 'In-house', 'Manufacturing'), ('lighting', 'Lighting', 'Indoor &amp; Outdoor Lighting'),
       ('consultancy', 'Advisory', 'Energy Consultancy'), ('maintenance', 'Support', 'Operations &amp; Maintenance')]
_GO = '<svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 9h10M10 5l4 4-4 4"/></svg>'
_rows = '\n'.join(f'''        <li><a class="si-row{" on" if k == 0 else ""}" href="solutions.html#{sid}" data-k="{k}">
          <span class="si-media"><span class="sv-scene">{_uniq(_hide(_SC[sid]), "m" + str(k))}</span></span>
          <span class="si-n">{k + 1:02d}</span><span class="si-name">{name}</span><span class="si-tag">{tag}</span><span class="si-go">{_GO}</span>
        </a></li>''' for k, (sid, tag, name) in enumerate(_SI))
_plate = '\n'.join(f'          <div class="sv-scene" data-k="{k}">{_uniq(_hide(_SC[sid]), "h")}</div>' for k, (sid, *_r) in enumerate(_SI))
_new = f'''<div class="si" id="solIndex">
      <ol class="si-list" id="siList">
{_rows}
      </ol>
      <div class="si-stage" aria-hidden="true">
        <div class="si-plate" id="siPlate">
{_plate}
          <div class="si-count"><b id="siNum">01</b><span>/ 08</span></div>
          <span class="si-hint">Point at a solution</span>
        </div>
      </div>
    </div>
    <a class="text-link sol-all" href="solutions.html">Explore all solutions {ARR}</a>
  </div>
</section>'''
_i = s.index('<div class="sol-grid">'); _j = s.index('</section>', _i) + len('</section>')
assert s.count('<div class="sol-grid">') == 1
s = s[:_i] + _new + s[_j:]
rep("(innerWidth <= 700 && node.matches('.leaders'))))", "(innerWidth <= 700 && node.matches('.leaders')) || (innerWidth <= 900 && node.matches('.si-list'))))")
rep('.sol-all{margin-top:28px}', '.sol-all{margin-top:28px}\n' + _ISO_CSS + '''
/* homepage solutions: a numbered index; the plate shows the drawing for the row you point at */
.si{display:grid;grid-template-columns:minmax(0,1.08fr) minmax(0,1fr);gap:clamp(40px,6vw,96px);align-items:start}
.si-list{list-style:none;margin:0;padding:0;border-bottom:1px solid var(--line);counter-reset:none}
.si-row{position:relative;display:grid;grid-template-columns:52px minmax(0,1fr) auto 30px;align-items:center;column-gap:16px;padding:21px 4px;border-top:1px solid var(--line);color:var(--ink);text-decoration:none}
.si-row::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:var(--sun);transform:scaleX(0);transform-origin:0 50%;transition:transform .6s cubic-bezier(.2,.7,.2,1);z-index:1}
.si-row.on::after{transform:scaleX(1)}
.si-n{font:500 12px var(--f-mono);letter-spacing:.08em;color:var(--muted);transition:color .3s}
.si-name{font-size:clamp(21px,2vw,29px);font-weight:300;letter-spacing:-0.03em;line-height:1.15;transition:transform .55s cubic-bezier(.2,.7,.2,1)}
.si-tag{padding:5px 10px;border-radius:999px;background:var(--paper);font:500 11.5px var(--f-mono);letter-spacing:.04em;white-space:nowrap;transition:background .3s}
.si-go{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:var(--navy-deep);color:#fff;opacity:0;transform:translateX(-10px) rotate(-45deg);transition:opacity .35s,transform .55s cubic-bezier(.2,.7,.2,1)}
.si-go svg{width:15px;height:15px}
.si-row.on .si-n{color:var(--accent-ink)}
.si-row.on .si-name{transform:translateX(10px)}
.si-row.on .si-tag{background:var(--sun)}
.si-row.on .si-go{opacity:1;transform:none}
.si-row:focus-visible{outline-offset:-2px}
.si-media{display:none}
.si-stage{position:sticky;top:110px}
.si-plate{position:relative;width:100%;aspect-ratio:560/440;border-radius:24px;overflow:hidden;isolation:isolate;
  background:radial-gradient(90% 80% at 50% 45%,#1A1A20 0%,#0D0D10 72%);box-shadow:0 30px 80px -40px rgba(9,9,11,.6)}
.si-plate::before,.si-media::before{content:"";position:absolute;inset:0;z-index:-1;opacity:.55;
  background-image:radial-gradient(rgba(255,255,255,.09) 1px,transparent 1.2px);background-size:22px 22px;
  -webkit-mask-image:radial-gradient(75% 70% at 50% 50%,#000 30%,transparent 100%);mask-image:radial-gradient(75% 70% at 50% 50%,#000 30%,transparent 100%)}
.si-plate .sv-scene{position:absolute;inset:0;opacity:0;transition:opacity .6s ease}
.si-plate .sv-scene.on{opacity:1}
.si-count{position:absolute;left:24px;top:22px;display:flex;align-items:baseline;gap:8px;font:500 12px var(--f-mono);letter-spacing:.06em;color:rgba(255,255,255,.75)}
.si-count b{font-weight:500;color:#fff}
.si-hint{position:absolute;right:22px;bottom:18px;font:500 10.5px var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.62)}
.sv-scene .pc{opacity:0;transform:translateY(-14px);transition:opacity .5s ease calc(var(--i) * 90ms),transform .8s cubic-bezier(.2,.7,.2,1) calc(var(--i) * 90ms)}
.sv-scene.on .pc{opacity:1;transform:none}
.sv-scene.on .fl,.sv-scene.on .fg{animation:svFlow 1.1s linear infinite}
.sv-scene.on .scan{animation:svScan 3.6s cubic-bezier(.45,0,.55,1) infinite alternate}
@keyframes svFlow{to{stroke-dashoffset:-18}}
@keyframes svScan{from{transform:translate(0,0)}to{transform:translate(204px,118px)}}
@media (max-width:900px){
  .si{display:block}
  .si-stage{display:none}
  .si-list{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;margin-inline:calc(clamp(16px,4vw,48px) * -1);padding:0 clamp(16px,4vw,48px) 8px;border:0;scrollbar-width:none;scroll-padding-inline:clamp(16px,4vw,48px)}
  .si-list::-webkit-scrollbar{display:none}
  .si-list li{flex:0 0 min(78%,340px);scroll-snap-align:start}
  .si-row,.si-row.on{display:flex;flex-direction:column;align-items:flex-start;height:100%;padding:0;border:0}
  .si-row::after,.si-go{display:none}
  .si-row.on .si-name{transform:none}
  .si-row.on .si-tag{background:var(--paper)}
  .si-media{display:block;position:relative;isolation:isolate;width:100%;aspect-ratio:560/440;border-radius:18px;overflow:hidden;background:radial-gradient(90% 80% at 50% 45%,#1A1A20 0%,#0D0D10 72%)}
  .si-media .sv-scene{position:absolute;inset:0}
  .si-n{margin-top:16px}
  .si-name{margin-top:6px;font-size:21px}
  .si-tag{margin-top:12px}
}
@media (prefers-reduced-motion: reduce){
  .sv-scene .pc{opacity:1;transform:none;transition:none}
  .sv-scene.on .fl,.sv-scene.on .fg,.sv-scene.on .scan{animation:none}
  .si-row::after,.si-name,.si-go,.si-plate .sv-scene{transition:none}
}''')
rep("/* ---------- Enquiry form (preview) ---------- */", """/* ---------- Solutions index: point at (or tab to) a solution and the plate draws it ---------- */
(function(){
  const wrap = document.getElementById('solIndex'); if (!wrap) return;
  const rows = [...wrap.querySelectorAll('.si-row')], plate = document.getElementById('siPlate');
  const scenes = [...plate.querySelectorAll('.sv-scene')], num = document.getElementById('siNum');
  let cur = 0, shown = false;
  const set = k => {
    cur = k; rows.forEach((r, i) => r.classList.toggle('on', i === k));
    if (shown) scenes.forEach((s, i) => s.classList.toggle('on', i === k));
    num.textContent = String(k + 1).padStart(2, '0');
  };
  rows.forEach((r, i) => { r.addEventListener('mouseenter', () => set(i)); r.addEventListener('focus', () => set(i)); });
  const show = () => { shown = true; set(cur); };
  const mob = [...wrap.querySelectorAll('.si-media .sv-scene')];
  if (reduce || !('IntersectionObserver' in window)) { show(); mob.forEach(s => s.classList.add('on')); return; }
  const io = new IntersectionObserver(es => { if (es[0].isIntersecting){ show(); io.disconnect(); } }, { rootMargin:'0px 0px -25% 0px' }); io.observe(plate);
  mob.forEach(s => { const o = new IntersectionObserver(es => { if (es[0].isIntersecting){ s.classList.add('on'); o.disconnect(); } }, { threshold:.5 }); o.observe(s); });
})();

/* ---------- Enquiry form (preview) ---------- */""")

# ================= 12. Calculator: the bill amount was clipped (measured before the web font loaded) =================
rep("  const meas = $('billMeasure'); meas.textContent = billInput.value || '0'; billInput.style.width = (meas.offsetWidth + 4) + 'px';",
    "  sizeBill();")
rep("const range = $('billRange'), billInput = $('billInput');",
    """const range = $('billRange'), billInput = $('billInput');
// size the amount box to its text; re-measure once Inter Tight has loaded and when the screen size changes the font size
function sizeBill(){ const meas = $('billMeasure'); meas.textContent = billInput.value || '0'; billInput.style.width = Math.ceil(meas.getBoundingClientRect().width) + 8 + 'px'; }
if (document.fonts){ document.fonts.ready.then(sizeBill); document.fonts.addEventListener && document.fonts.addEventListener('loadingdone', sizeBill); }
addEventListener('resize', sizeBill);
if (window.ResizeObserver) new ResizeObserver(sizeBill).observe(billInput.parentNode);   // also catches font-size changes inside resized frames
billInput.addEventListener('input', sizeBill);""")

# ================= 13. Multi-page: Projects has its own page =================
rep('<a href="solutions.html">Solutions</a><a href="#projects">Projects</a>', '<a href="solutions.html">Solutions</a><a href="projects.html">Projects</a>')
rep('<a href="#projects" style="--i:2">Projects', '<a href="projects.html" style="--i:2">Projects')
rep('<a href="#team">Our people</a><a href="#projects">Projects</a>', '<a href="#team">Our people</a><a href="projects.html">Projects</a>')
rep('<span class="ct"><b id="projCount">01</b> / 06</span></div>\n  </div>\n</section>',
    '<span class="ct"><b id="projCount">01</b> / 06</span></div>\n  </div>\n  <div class="wrap"><a class="text-link proj-all" href="projects.html">View all projects ' + ARR + '</a></div>\n</section>')
rep('.proj-progress .bar{', '.proj-all{margin-top:26px}\n.proj-progress .bar{')

# ================= 14. Navbar without "Our People" (user, 23 Oct; the team stays on the homepage and in the footer) =================
rep('<a href="#gallery">Gallery</a><a href="#team">Our People</a><a href="#contact">Contact</a>', '<a href="#gallery">Gallery</a><a href="#contact">Contact</a>')
rep('  <a href="#team" style="--i:4">Our People<span aria-hidden="true">05</span></a>\n', '')
rep('<a href="#contact" style="--i:5">Contact<span aria-hidden="true">06</span></a>', '<a href="#contact" style="--i:4">Contact<span aria-hidden="true">05</span></a>')

# ================= 15. Multi-page: Gallery has its own page =================
rep('<a href="#gallery">Gallery</a><a href="#contact">Contact</a>', '<a href="gallery.html">Gallery</a><a href="#contact">Contact</a>')
rep('<a href="#gallery" style="--i:3">Gallery', '<a href="gallery.html" style="--i:3">Gallery')
rep('<a href="projects.html">Projects</a><a href="#gallery">Gallery</a>', '<a href="projects.html">Projects</a><a href="gallery.html">Gallery</a>')
for _cat, _h in [('installations', '<h3>Solar installations</h3>'), ('manufacturing', '<h3>Manufacturing &amp; innovation</h3>'),
                 ('people', '<h3>People at work</h3>'), ('milestones', '<h3>Milestones &amp; recognition</h3>')]:
    _i = s.index(_h); _j = s.index('href="#gallery"', _i); assert _j - _i < 400
    s = s[:_j] + f'href="gallery.html#{_cat}"' + s[_j + len('href="#gallery"'):]
rep('<a class="btn btn-ghost" href="#gallery">View full gallery', '<a class="btn btn-ghost" href="gallery.html">View full gallery')

# ================= 16. Multi-page: Contact has its own page =================
rep('<a href="gallery.html">Gallery</a><a href="#contact">Contact</a>', '<a href="gallery.html">Gallery</a><a href="contact.html">Contact</a>')
rep('<a class="btn btn-sun" href="#contact">Get a free quote</a>', '<a class="btn btn-sun" href="contact.html">Get a free quote</a>')
rep('<a href="#contact" style="--i:4">Contact', '<a href="contact.html" style="--i:4">Contact')
rep('<a class="btn btn-sun mnav-cta" href="#contact"', '<a class="btn btn-sun mnav-cta" href="contact.html"')
rep('<a href="#contact">Palakkad · Kochi</a>', '<a href="contact.html#offices">Palakkad · Kochi</a>')

s = s.replace("  win(.06, .01, 0, 0, -9);                                                      // (keeps glass material warm-up simple)\n", "")
open(d + 'src_draft.html', 'w').write(s)
print('ok', len(s))
