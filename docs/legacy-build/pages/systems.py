# Draft: replace "Panel anatomy" with a pinned 3D home showing how on-grid, off-grid and hybrid systems move power,
# by day and after sunset. Reads the approved v48 source, writes src_draft.html (src.html stays as approved).
d = '/tmp/claude-0/site/'
s = open(d + 'src_v48.html').read()
def rep(a, b):
    global s
    assert a in s, 'MISSING: ' + a[:100]; s = s.replace(a, b, 1)

ARR = '<svg class="arr" width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 9h10M10 5l4 4-4 4"/></svg>'

# ---------------- markup ----------------
i = s.index('<!-- ======= PANEL ANATOMY ======= -->'); j = s.index('<!-- =======', i + 10)
s = s[:i] + f'''<!-- ======= SOLAR SYSTEMS: ON-GRID, OFF-GRID, HYBRID ======= -->
<section class="anatomy systems" id="anatomy" aria-label="On-grid, off-grid and hybrid solar">
  <div class="anat-in">
    <div class="anat-copy">
      <h2>On-grid, <span class="nw">off-grid</span> <em>or hybrid?</em></h2>
      <p>Scroll to follow the power through each system, from the midday sun to after sunset.</p>
      <ol class="layers sys-list" id="layerList">
        <li data-i="0"><span class="k">01</span><div><b>On-grid</b><small>Solar powers your home by day and the extra goes to the grid through a net meter. After sunset you use grid power. No battery, so it costs the least, but it pauses during power cuts.<em>Best for lower bills</em></small></div></li>
        <li data-i="1"><span class="k">02</span><div><b>Off-grid</b><small>No grid connection at all. Panels charge a battery bank by day, and the battery keeps your home running after sunset.<em>Best for remote sites, farms and estates</em></small></div></li>
        <li data-i="2"><span class="k">03</span><div><b>Hybrid</b><small>Connected to the grid, with a battery. Solar is used first, the battery stores the extra and the rest goes to the grid. In a power cut, the battery takes over.<em>Best for savings with backup</em></small></div></li>
      </ol>
      <a class="text-link sys-cta" href="#contact">Not sure which fits? Ask an engineer {ARR}</a>
    </div>
    <div class="anat-stage">
      <canvas id="anatCanvas" aria-hidden="true"></canvas>
      <div class="sys-clock" id="sysClock" aria-hidden="true">
        <svg class="i-sun" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="10" cy="10" r="3.6"/><path d="M10 1.8v2M10 16.2v2M1.8 10h2M16.2 10h2M4.2 4.2l1.4 1.4M14.4 14.4l1.4 1.4M4.2 15.8l1.4-1.4M14.4 5.6l1.4-1.4"/></svg>
        <svg class="i-moon" viewBox="0 0 20 20" fill="currentColor"><path d="M15.6 12.9A6.6 6.6 0 0 1 7.1 4.4a6.6 6.6 0 1 0 8.5 8.5z"/></svg>
        <b id="sysTime">12:00</b><span id="sysSolar">Solar 4.2 kW</span>
      </div>
      <div class="anat-tag" id="anatTag" aria-hidden="true"><i></i><div><b>Net meter</b><span>Sending 1.6 kW to the grid</span></div></div>
      <div class="sys-key" aria-hidden="true"><span><i class="y"></i>Solar or battery power</span><span><i class="w"></i>Grid power</span></div>
    </div>
  </div>
  <div class="anat-progress" id="anatProg"></div>
</section>


''' + s[j:]

# ---------------- styles ----------------
rep('/* ---------- Solutions ---------- */', '''/* ---------- Solar systems: on-grid, off-grid, hybrid (reuses the pinned anatomy layout) ---------- */
.systems .nw{white-space:nowrap}
.sys-list li.on small{max-height:150px}
.sys-list small em{display:block;margin-top:8px;font:500 12px var(--f-mono);letter-spacing:.04em;font-style:normal;color:var(--sun)}
.sys-list.all li small{max-height:none;opacity:1}
.systems .sys-cta{color:#fff;margin-top:20px}
.sys-clock{position:absolute;left:0;top:6px;z-index:2;display:flex;align-items:center;gap:10px;padding:7px 14px 7px 10px;border-radius:999px;background:rgba(20,20,22,.82);border:1px solid var(--line-dark);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);font:500 13px var(--f-mono);color:var(--on-dark-muted)}
.sys-clock svg{width:18px;height:18px;color:var(--sun)}
.sys-clock .i-moon{display:none;color:#E4E4E7}
.sys-clock.night .i-sun{display:none}
.sys-clock.night .i-moon{display:block}
.sys-clock b{font-weight:500;color:#fff;font-variant-numeric:tabular-nums}
.sys-clock span{font-variant-numeric:tabular-nums}
.sys-key{position:absolute;left:0;bottom:8px;display:flex;gap:20px;font:500 12px var(--f-mono);color:var(--on-dark-muted)}
.sys-key i{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:8px;vertical-align:1px}
.sys-key i.y{background:var(--sun);box-shadow:0 0 0 4px rgba(249,194,46,.16)}
.sys-key i.w{background:#fff;box-shadow:0 0 0 4px rgba(255,255,255,.12)}
.systems .anat-tag>div{min-width:0}
@media (max-width:900px){
  .systems .sys-cta,.sys-key{display:none}
  .systems .anat-stage{margin-left:calc(-1 * var(--g, 20px));margin-right:calc(-1 * var(--gR, 20px))}   /* the model runs edge to edge on phones */
  .systems .sys-clock{left:var(--g, 20px)}
  .systems .anat-tag b{font-size:13px}.systems .anat-tag span{font-size:11.5px}
  .sys-list li.on small{font-size:13.5px}
  .sys-clock{top:2px;padding:6px 12px 6px 8px;font-size:12px}
  .sys-clock svg{width:16px;height:16px}
}

/* ---------- Solutions ---------- */''')

# ---------------- remove the panel model (no longer used) ----------------
a = s.index('function buildPanel(){'); b = s.index('function studioEnvironment(renderer){')
s = s[:a] + s[b:]

# ---------------- scene + scroll ----------------
a = s.index('/* ---------- Panel anatomy: the module comes apart layer by layer on scroll ---------- */')
b = s.index('} else { setActive(3); }', a) + len('} else { setActive(3); }')
s = s[:a] + r'''/* ---------- On-grid, off-grid or hybrid: follow the power round a home, by day and after sunset ---------- */
const list = [...document.querySelectorAll('#layerList li')];
let shownStep = -1;
function setActive(i){ if (i === shownStep) return; shownStep = i; list.forEach((li,k) => li.classList.toggle('on', k === i)); }
setActive(0);
const sys = { p: reduce ? (2 + .3) / 3 : 0 };
// flows from the inverter: solar in, home, battery (+ charging, - discharging), grid (+ export, - import)
const SYS_DAY   = [[1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]];
const SYS_NIGHT = [[0, 1, 0, -1], [0, 1, -1, 0], [0, 1, -1, 0]];
const SYS_HAS   = [[0, 1], [1, 0], [1, 1]];                       // [battery, grid] in each system
const SYS_TAGS  = [
  [['meter', 'Net meter', 'Sending 1.6 kW to the grid'], ['pole', 'Grid', 'Powering your home tonight']],
  [['batt', 'Battery bank', 'Charging · {b}%'], ['batt', 'Battery bank', 'Powering your home · {b}%']],
  [['inv', 'Hybrid inverter', 'Home first, then battery, then grid'], ['batt', 'Battery backup', 'Powering your home · {b}%']]
];
function sysState(p){
  const x = Math.min(2.9999, Math.max(0, p * 3)), step = Math.floor(x), u = x - step;
  const mix = step ? ss(0, .14, u) : 1, prev = step ? step - 1 : 0;
  const night = Math.max(step ? 1 - ss(0, .1, u) : 0, ss(.5, .7, u));
  const w = [0, 0, 0]; w[prev] += 1 - mix; w[step] += mix;
  const f = [0, 0, 0, 0]; let vb = 0, vg = 0;
  for (let m = 0; m < 3; m++){ if (!w[m]) continue;
    for (let k = 0; k < 4; k++) f[k] += w[m] * ((1 - night) * SYS_DAY[m][k] + night * SYS_NIGHT[m][k]);
    vb += w[m] * SYS_HAS[m][0]; vg += w[m] * SYS_HAS[m][1]; }
  const hour = (10.5 + 3.5 * ss(.1, .5, u)) * (1 - night) + (19.75 + 2 * ss(.6, 1, u)) * night;
  const solar = Math.max(0, 4.4 * (1 - Math.pow((hour - 12.8) / 6.2, 2))) * (1 - night);
  const charge = Math.round(40 + 50 * ss(.12, .5, u) - 34 * ss(.62, 1, u));
  return { step, u, night, f, vb, vg, w, hour, solar, charge };
}
if (hasThree){
  const canvas = document.getElementById('anatCanvas'), stage = canvas.parentElement;
  const S = makeScene(canvas), { scene, camera, key } = S;
  key.position.set(7, 13, 9); key.shadow.mapSize.set(2048, 2048);
  Object.assign(key.shadow.camera, { left:-9, right:9, top:9, bottom:-9, near:2, far:40 }); key.shadow.camera.updateProjectionMatrix();
  key.shadow.bias = -.0003; key.shadow.normalBias = .03;
  const rim = scene.children.find(o => o.isDirectionalLight && o !== key);
  const hemi = new THREE.HemisphereLight(0xe8ecff, 0x0c0c0e, .55); scene.add(hemi);
  const dayKey = new THREE.Color(0xfff1d8), nightKey = new THREE.Color(0x8ea6ff);
  const mats = [];
  const M = (color, o = {}) => { const m = new THREE.MeshStandardMaterial(Object.assign({ color, roughness:.85, metalness:0 }, o)); m.userData.env = 1; mats.push(m); return m; };
  const wallM = M(0xEDEBE6), wall2M = M(0xDDDAD3), roofM = M(0xCBC8C1), trimM = M(0x26262A, { roughness:.55 }), plinthM = M(0x141416, { roughness:.95 }),
        paveM = M(0x222226, { roughness:.95 }), metalM = M(0xC4C8CE, { roughness:.3, metalness:.85 }), poleM = M(0x4A4A50, { roughness:.75 }),
        whiteM = M(0xF5F5F3, { roughness:.45 }), darkM = M(0x101012, { roughness:.4 }), treeM = M(0xE2E0DA, { roughness:.9, flatShading:true }), meterM = M(0xD6D6D2, { roughness:.6 });
  const glassM = M(0x1a1e26, { roughness:.12, metalness:.3, emissive:0xF0A050, emissiveIntensity:0 }); glassM.toneMapped = false;   // warm lamp-light, not washed out
  const cellM = new THREE.MeshPhysicalMaterial({ map:cellTexture(), roughness:.32, metalness:.1, clearcoat:.4, clearcoatRoughness:.1 }); cellM.userData.env = .6; mats.push(cellM);
  const screenM = new THREE.MeshBasicMaterial({ color:0xF9C22E, toneMapped:false });
  const G = new THREE.Group(); scene.add(G);
  const add = (geo, m, x, y, z, parent = G, shadow = true) => { const o = new THREE.Mesh(geo, m); o.position.set(x, y, z); o.castShadow = shadow; o.receiveShadow = true; parent.add(o); return o; };
  const BX = (w, h, dd) => new THREE.BoxGeometry(w, h, dd);
  const V = (x, y, z) => new THREE.Vector3(x, y, z);

  // the plinth: a model on a rounded base, like an architect's maquette
  add(new THREE.ExtrudeGeometry(roundedRect(10.2, 7.4, .7), { depth:.4, bevelEnabled:true, bevelThickness:.05, bevelSize:.05, bevelSegments:3, curveSegments:10 }).rotateX(-Math.PI/2), plinthM, 1.0, -.45, -.1, G, false);
  add(BX(.9, .02, 2.2), paveM, 1.45, .01, 2.45, G, false);           // path to the door
  add(BX(4.3, .03, .9), paveM, -1.2, .015, 1.8, G, false);           // front terrace
  // the house: a two-storey main block and a single-storey annex
  add(BX(4.0, 2.7, 3.0), wallM, -1.2, 1.35, -.2);
  add(BX(4.1, .08, 3.1), roofM, -1.2, 2.74, -.2);
  add(BX(4.1, .2, .08), wallM, -1.2, 2.88, 1.31); add(BX(4.1, .2, .08), wallM, -1.2, 2.88, -1.71);
  add(BX(.08, .2, 3.1), wallM, -3.21, 2.88, -.2); add(BX(.08, .2, 3.1), wallM, .81, 2.88, -.2);
  add(BX(1.8, 1.9, 2.2), wall2M, 1.7, .95, .2);
  add(BX(2.15, .1, 2.6), trimM, 1.75, 1.95, .35);
  [-2.35, -.85].forEach(x => { add(BX(1.15, 1.25, .06), trimM, x, 1.45, 1.3); add(BX(1.0, 1.1, .07), glassM, x, 1.45, 1.31); });
  add(BX(1.15, .55, .06), trimM, -1.6, .55, 1.3, G, false); add(BX(1.0, .42, .07), glassM, -1.6, .55, 1.31, G, false);
  add(BX(.06, .5, 1.4), glassM, .82, 2.3, -.6);
  add(BX(.9, 1.6, .06), trimM, 1.45, .8, 1.3);                        // door
  add(BX(.25, 1.4, .07), glassM, 1.95, .8, 1.3);                      // glass beside the door
  // solar array on the roof: two rows of five, tilted towards the sun
  const cellMats = [metalM, metalM, cellM, metalM, metalM, metalM], pGeo = BX(.6, .035, 1.2);
  for (let r = 0; r < 2; r++) for (let c = 0; c < 5; c++){
    const g = new THREE.Group(); g.position.set(-2.85 + c * .68, 3.02, -1.0 + r * 1.35); g.rotation.x = .26; G.add(g);
    add(pGeo, cellMats, 0, 0, 0, g);
    add(BX(.03, .4, .03), metalM, -.25, -.2, -.5, g); add(BX(.03, .4, .03), metalM, .25, -.2, -.5, g);
    add(BX(.03, .14, .03), metalM, -.25, -.07, .5, g); add(BX(.03, .14, .03), metalM, .25, -.07, .5, g);
  }
  // inverter on the annex wall, with its small display
  add(BX(.16, .62, .46), whiteM, 2.68, 1.2, .45);
  add(BX(.012, .07, .2), screenM, 2.766, 1.34, .45, G, false);
  // net meter and the bracket the grid line comes in on
  const meter = new THREE.Group(); G.add(meter);
  add(BX(.14, .36, .26), meterM, 2.67, 1.15, -.38, meter); add(BX(.012, .1, .16), darkM, 2.745, 1.22, -.38, meter);
  add(BX(.1, .08, .3), trimM, 2.65, 1.85, -.44, meter);
  // battery bank, with a charge gauge
  const batt = new THREE.Group(); batt.position.set(3.5, 0, .55); G.add(batt);
  add(BX(.44, 1.1, .66), whiteM, 0, .55, 0, batt); add(BX(.47, .06, .69), trimM, 0, 1.12, 0, batt);
  const leds = [0, 1, 2, 3, 4].map(k => add(BX(.012, .12, .3), new THREE.MeshBasicMaterial({ color:0x2a2a2e, toneMapped:false }), .226, .3 + k * .16, 0, batt, false));
  // grid pole
  const pole = new THREE.Group(); pole.position.set(5.2, 0, -2.6); G.add(pole);
  add(new THREE.CylinderGeometry(.06, .09, 4.6, 12), poleM, 0, 2.3, 0, pole);
  const arm = add(BX(1.2, .08, .08), poleM, 0, 4.25, 0, pole); arm.rotation.y = Math.PI / 4;
  [-.5, .5].forEach(t => add(new THREE.CylinderGeometry(.035, .045, .14, 8), whiteM, t * .707, 4.36, -t * .707, pole));
  // cables, and the dots of power that run along them
  const poly = pts => { const c = new THREE.CurvePath(); for (let k = 1; k < pts.length; k++) c.add(new THREE.LineCurve3(pts[k-1], pts[k])); return c; };
  const pvC = poly([V(.2, 3.0, .45), V(.9, 3.0, .45), V(.9, 2.03, .45), V(2.86, 2.03, .45), V(2.86, 1.6, .45), V(2.7, 1.6, .45), V(2.7, 1.51, .45)]);
  const homeC = poly([V(2.7, .89, .58), V(2.64, .62, .58), V(2.64, .62, 1.34), V(2.08, .62, 1.34)]);
  const battC = poly([V(2.7, .89, .3), V(2.7, .05, .3), V(3.27, .05, .3)]);
  const ins = V(5.2 - .354, 4.43, -2.6 + .354), ins2 = V(5.2 + .354, 4.43, -2.6 - .354);
  const gridC = poly([V(2.7, 1.25, .22), V(2.7, 1.25, -.38), V(2.7, 1.85, -.38)]);
  gridC.add(new THREE.QuadraticBezierCurve3(V(2.7, 1.85, -.38), V(3.78, 2.55, -1.32), ins));
  const neutralC = new THREE.QuadraticBezierCurve3(V(2.7, 1.85, -.5), V(3.95, 2.45, -1.6), ins2);
  const dotTex = (() => { const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d');
    const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(.2, 'rgba(255,255,255,.95)'); gr.addColorStop(.42, 'rgba(255,255,255,.25)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = gr; g.fillRect(0, 0, 64, 64); return new THREE.CanvasTexture(c); })();
  const cableMat = () => M(0x1b1b1e, { roughness:.5, emissive:0xF9C22E, emissiveIntensity:0, transparent:true });
  const tube = (curve, m, r = .022) => add(new THREE.TubeGeometry(curve, Math.max(32, Math.round(curve.getLength() * 30)), r, 6, false), m, 0, 0, 0, G, false);
  const flows = [pvC, homeC, battC, gridC].map(curve => {
    const len = curve.getLength(), n = Math.max(3, Math.round(len / .26));
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(n * 3), 3));
    geo.setAttribute('color', new THREE.BufferAttribute(new Float32Array(n * 3), 3));
    const pts = new THREE.Points(geo, new THREE.PointsMaterial({ size:13, sizeAttenuation:false, map:dotTex, vertexColors:true, transparent:true, depthWrite:false, blending:THREE.AdditiveBlending, toneMapped:false }));
    pts.frustumCulled = false; pts.renderOrder = 5; G.add(pts);
    const cm = cableMat(); tube(curve, cm);
    return { curve, len, n, pts, cm, t: Math.random() };
  });
  const neutralM = cableMat(); tube(neutralC, neutralM, .016);
  const YEL = new THREE.Color(0xF9C22E), WHT = new THREE.Color(0xF4F4F5), col = new THREE.Color(), tmp = V(0, 0, 0), toCam = V(0, 0, 0);
  const anchors = { meter:V(2.76, 1.2, -.38), pole:ins, batt:V(3.73, .95, .55), inv:V(2.77, 1.25, .45) };

  const tag = document.getElementById('anatTag'), tagB = tag.querySelector('b'), tagS = tag.querySelector('span');
  const clock = document.getElementById('sysClock'), clockT = document.getElementById('sysTime'), clockS = document.getElementById('sysSolar');
  let tagKey = '', tagTpl = '', swapAt = 0, lastT = performance.now(), visible = false;
  const cam = { az:.32, el:.5, r:26, init:false };
  new IntersectionObserver(es => { visible = es[0].isIntersecting; if (visible) S.resize(); }, { rootMargin:'600px 0px' }).observe(canvas);   // start drawing (and compiling) a little before it scrolls in
  const pr = V(0, 0, 0);
  (function loop(now){
    requestAnimationFrame(loop); if (!visible) return;
    now = now || performance.now(); const dt = Math.min(.05, (now - lastT) / 1000); lastT = now;
    const st = sysState(sys.p), n = st.night, mob = isMobile();
    // light: warm midday sun, then a cool, dim evening
    key.intensity = 1.6 - 1.3 * n; key.color.copy(dayKey).lerp(nightKey, n);
    if (rim) rim.intensity = .7 * (1 - n);
    hemi.intensity = .55 - .3 * n;
    mats.forEach(m => m.envMapIntensity = m.userData.env * (1 - .7 * n));
    glassM.emissiveIntensity = .8 * ss(.25, 1, n);
    // battery rises out of the plinth when the system has one; the grid pole and line do the same
    const vb = ss(0, 1, st.vb), vg = ss(0, 1, st.vg);
    batt.visible = vb > .01; batt.scale.set(1, Math.max(.001, vb), 1);
    pole.visible = vg > .01; pole.scale.set(1, Math.max(.001, vg), 1);
    meter.visible = vg > .01; meter.scale.set(Math.max(.001, vg), 1, 1);
    neutralM.opacity = ss(.4, 1, vg); flows[3].cm.opacity = ss(.4, 1, vg);
    const lit = Math.round(st.charge / 20 + .3);
    leds.forEach((l, k) => l.material.color.set(k < lit ? 0xF9C22E : 0x2a2a2e));
    // power along the cables
    const gridHome = st.w[0] * n;                                  // on-grid at night: the home runs on grid power
    toCam.copy(camera.position);
    flows.forEach((fl, k) => {
      const v = st.f[k], a = Math.min(1, Math.abs(v));
      fl.cm.emissiveIntensity = .35 * a;
      if (a < .01){ fl.pts.visible = false; return; }
      fl.pts.visible = true;
      if (!reduce) fl.t = (fl.t + dt * .6 / fl.len) % 1;
      const dir = v >= 0 ? 1 : -1, pos = fl.pts.geometry.attributes.position, cl = fl.pts.geometry.attributes.color;
      if (k === 1) col.copy(YEL).lerp(WHT, gridHome); else if (k === 3 && dir < 0) col.copy(WHT); else col.copy(YEL);
      for (let i = 0; i < fl.n; i++){
        const sp = (fl.t + i / fl.n) % 1, fade = Math.min(1, sp / .1, (1 - sp) / .1);
        tmp.copy(fl.curve.getPoint(dir > 0 ? sp : 1 - sp));
        pr.copy(toCam).sub(tmp).normalize().multiplyScalar(.06); tmp.add(pr);   // sit just in front of the cable
        pos.setXYZ(i, tmp.x, tmp.y, tmp.z);
        cl.setXYZ(i, col.r * a * fade, col.g * a * fade, col.b * a * fade);
      }
      pos.needsUpdate = cl.needsUpdate = true;
    });
    // camera: a slow orbit across the whole scroll
    const r = stage.getBoundingClientRect(), asp = r.width / Math.max(1, r.height);
    const tAz = mob ? .26 + .22 * sys.p : .3 + .5 * sys.p, tEl = mob ? .64 : .5 - .07 * sys.p, tf = .2493;   // tan(14°), half the field of view
    const tR = Math.max((mob ? 5.2 : 6.6) / (tf * asp), (mob ? 3.6 : 4.4) / tf);   // fit the model to the stage, whatever its shape
    if (!cam.init){ Object.assign(cam, { az:tAz, el:tEl, r:tR, init:true }); }
    const e = 1 - Math.exp(-dt * 5);
    cam.az += (tAz - cam.az) * e; cam.el += (tEl - cam.el) * e; cam.r += (tR - cam.r) * e;
    const tx = mob ? 1.3 : .9, ty = mob ? .85 : 1.1, tz = -.1;
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
    if (tagTpl) { const txt = tagTpl.replace('{b}', st.charge); if (tagS.textContent !== txt) tagS.textContent = txt; }
    const hidden = (T[0] === 'batt' && vb < .9) || ((T[0] === 'meter' || T[0] === 'pole') && vg < .9) || st.u < .16 && st.step > 0;
    if (!swapAt) tag.style.opacity = hidden || sys.p < .003 && !reduce ? 0 : 1;
    tmp.copy(anchors[T[0]]); tmp.project(camera);
    let x = (tmp.x + 1) / 2 * r.width; const y = (1 - tmp.y) / 2 * r.height;
    const flip = x + tag.offsetWidth > r.width - 8; tag.classList.toggle('flip', flip);
    if (flip) x = Math.max(4, x - tag.offsetWidth);
    tag.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px)`;
  })();
}
if (hasGsap && !reduce){
  ScrollTrigger.create({ trigger:'#anatomy', start:'top top', end:'+=330%', pin:true, refreshPriority:2, scrub:true,
    onUpdate: self => { sys.p = self.progress; setActive(Math.min(2, Math.floor(self.progress * 3)));
      document.getElementById('anatProg').style.width = (self.progress * 100) + '%'; } });
} else { setActive(2); document.getElementById('layerList').classList.add('all'); }''' + s[b:]

s = s.replace('*{box-sizing:border-box}', '*{box-sizing:border-box}\nhtml,body{margin:0}', 1)
open(d + 'src_draft.html', 'w').write(s)
print('ok', len(s))
