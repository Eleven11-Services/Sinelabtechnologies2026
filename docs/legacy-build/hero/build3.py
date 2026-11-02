exec(open('/tmp/claude-0/hero2/compose.py').read())
L_SEAM, R_SEAM = S(0), S(1536)            # 437, 1973
def jag(h, w, scale=7, seed=0):
    r = np.random.default_rng(abs(int(seed))).random((h // scale + 2, w // scale + 2))
    return ndimage.gaussian_filter(ndimage.zoom(r, scale, order=1)[:h, :w], 1.2)
def join(h, w, n, side, seed):
    """alpha 1 everywhere except a patchy n-px transition at one edge ('L' rises 0->1 from the left, 'R' falls to the right, 'T' rises from the top)"""
    a = np.ones((h, w))
    if side in 'LR':
        t = np.linspace(0, 1, n)[None].repeat(h, 0); t = np.clip((t + (jag(h, n, seed=seed) - .5) * .8 - .5) * 5 + .5, 0, 1)
        if side == 'L': a[:, :n] = t
        else: a[:, w - n:] = t[:, ::-1]
    else:
        t = np.linspace(0, 1, n)[:, None].repeat(w, 1); t = np.clip((t + (jag(n, w, seed=seed) - .5) * .8 - .5) * 5 + .5, 0, 1)
        a[:n] = t
    return a
def flipx(p): return p[:, ::-1].copy()
def match(p, ref, mask_p=None, mask_r=None):
    """per-channel mean/std transfer so a borrowed patch takes on the colours of the area it continues"""
    out = p.copy()
    for c in range(3):
        a = p[..., c][mask_p] if mask_p is not None else p[..., c].ravel(); b = ref[..., c][mask_r] if mask_r is not None else ref[..., c].ravel()
        out[..., c] = (p[..., c] - a.mean()) / (a.std() + 1e-6) * b.std() + b.mean()
    return np.clip(out, 0, 1)
# ---------- photo: its sky fades into the new sky near the edges; everything else stays crisp ----------
P = O.copy(); sk = skyness(P, cloud_rows=430); fade = np.ones(P.shape[:2])
for i in range(90):
    f = i / 90; fade[:, i] = np.minimum(fade[:, i], f); fade[:, -1 - i] = np.minimum(fade[:, -1 - i], f); fade[i, :] = np.minimum(fade[i, :], f)
put(P, L_SEAM, T(0), 1 - sk * (1 - fade))
OV = 70
CROWN = o(1300, 1536, 0, 380)              # big tree, leafy left edge against the sky
CROWN2 = o(1300, 1536, 130, 380)
# ---------- RIGHT ----------
HD = o(1445, 1536, 648, 740)
def hedge(x0, x1, top, height, seed, start):
    src = HD if height == HD.shape[0] else np.asarray(Image.fromarray((HD * 255).astype(np.uint8)).resize((HD.shape[1], height), Image.LANCZOS)).astype(np.float32) / 255
    r = np.random.default_rng(seed); step = src.shape[1] - 30
    xs = list(range(x0, x1, step)) if start == 'L' else list(range(x1 - src.shape[1], x0 - src.shape[1], -step))
    for k, x in enumerate(xs):
        h = flipx(src) if k % 2 else src
        a = join(*h.shape[:2], 30, start, seed + k) * join(*h.shape[:2], 16, 'T', seed + 90 + k)
        put(h, x, top + int(r.integers(-3, 4)), a)
Eb = flipx(CROWN2); Ea = flipx(CROWN)
put(Eb, R_SEAM - OV, T(410), fol(Eb) * join(*Eb.shape[:2], OV, 'L', 22) * join(*Eb.shape[:2], 50, 'T', 23))
put(Eb, R_SEAM - OV, T(300), fol(Eb) * join(*Eb.shape[:2], OV, 'L', 24) * join(*Eb.shape[:2], 50, 'T', 25))
put(Ea, R_SEAM - OV, T(0), fol(Ea) * join(*Ea.shape[:2], OV, 'L', 21), fb=0)
hedge(R_SEAM - 40, W + 60, T(646), HD.shape[0], 3, 'L')
GR = o(1060, 1536, 750, 1024)
ref = o(1440, 1536, 760, 1024)
GR = match(GR, ref)
wall = np.clip((GR.mean(2) - .62) / .1, 0, 1) * np.clip((.13 - (GR.max(2) - GR.min(2))) / .06, 0, 1)
for k, x in enumerate([R_SEAM - 80, R_SEAM - 80 + GR.shape[1] - 90]):
    g = GR if k == 0 else flipx(GR)
    a = (1 - ndimage.gaussian_filter(wall if k == 0 else wall[:, ::-1], 2)) * join(*g.shape[:2], 80 if k == 0 else 90, 'L', 31 + k) * join(*g.shape[:2], 28, 'T', 35 + k)
    put(g, x, T(750) - 40, a)
    put(g[-40:], x, H - 40, join(40, g.shape[1], 80, 'L', 33 + k))
# ---------- LEFT ----------
lt_mask = fol(o(0, 140, 300, 760)) > .9
CL = match(CROWN, o(0, 140, 300, 760), fol(CROWN) > .9, lt_mask)        # same leafy edge, recoloured to the lighter left tree
CL2 = match(CROWN2, o(0, 140, 300, 760), fol(CROWN2) > .9, lt_mask)
put(CL2, L_SEAM + OV - CL2.shape[1], T(520), fol(CROWN2) * join(*CL2.shape[:2], OV, 'R', 42) * join(*CL2.shape[:2], 50, 'T', 43))
put(CL, L_SEAM + OV - CL.shape[1], T(290), fol(CROWN) * join(*CL.shape[:2], OV, 'R', 41))
hedge(-80, L_SEAM + 40, T(652), 175, 4, 'R')
SH = o(200, 400, 820, 1024); BU = match(o(1110, 1430, 752, 860), SH)
x = L_SEAM + OV - BU.shape[1]; k = 0                                    # a row of bushes behind the grasses
while x > -BU.shape[1]:
    b = flipx(BU) if k % 2 else BU
    put(b, x, H - SH.shape[0] - 60, join(*b.shape[:2], 50, 'R', 81 + k) * join(*b.shape[:2], 30, 'T', 85 + k))
    x -= BU.shape[1] - 50; k += 1
x = L_SEAM + OV - SH.shape[1]; k = 0
while x > -SH.shape[1]:
    sh = flipx(SH) if k % 2 else SH
    put(sh, x, H - SH.shape[0] + (8 if k % 2 else 0), join(*sh.shape[:2], OV if k == 0 else 50, 'R', 61 + k) * join(*sh.shape[:2], 36, 'T', 71 + k))
    x -= SH.shape[1] - 50; k += 1
Image.fromarray((np.clip(C, 0, 1) * 255).astype(np.uint8)).save('/tmp/claude-0/hero2/wide_clean.png')
