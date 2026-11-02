# Isometric line-and-tone drawings for the Solutions page: one small "maquette on a plinth" per service.
# Everything is built in 3D units and projected (2:1 isometric); each scene is auto-fitted into the same viewBox.
# Pieces are wrapped in <g class="pc" style="--i:n"> so the page can build a scene piece by piece when it becomes active.
import math
C = math.cos(math.radians(30))
VB_W, VB_H, PAD = 560, 440, 34

def P(x, y, z=0):
    return ((x - y) * C, (x + y) * 0.5 - z)

class Scene:
    def __init__(self):
        self.items = []      # (order, svg) ; order is the build index
        self.pts = []
        self.defs = []
        self.k = 0
        self.has_sun = False
    def _pts(self, pts):
        self.pts += pts
        return ' '.join(f'{a:.1f},{b:.1f}' for a, b in pts)
    def piece(self, svg_parts, step=True):
        self.items.append((self.k, ''.join(svg_parts)))
        if step: self.k += 1
    # ---- primitives returning svg strings ----
    def poly(self, pts3, cls):
        return f'<polygon class="{cls}" points="{self._pts([P(*p) for p in pts3])}"/>'
    def line(self, pts3, cls):
        return f'<polyline class="{cls}" points="{self._pts([P(*p) for p in pts3])}"/>'
    def box(self, x, y, z, w, d, h, t='t', l='l', r='r'):
        top = [(x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)]
        rgt = [(x + w, y, z), (x + w, y + d, z), (x + w, y + d, z + h), (x + w, y, z + h)]
        lft = [(x, y + d, z), (x + w, y + d, z), (x + w, y + d, z + h), (x, y + d, z + h)]
        return self.poly(lft, l) + self.poly(rgt, r) + self.poly(top, t)
    def face_y(self, x, y, z, w, h, cls):          # rectangle on a plane facing +y (left face)
        return self.poly([(x, y, z), (x + w, y, z), (x + w, y, z + h), (x, y, z + h)], cls)
    def face_x(self, x, y, z, d, h, cls):          # rectangle on a plane facing +x (right face)
        return self.poly([(x, y, z), (x, y + d, z), (x, y + d, z + h), (x, y, z + h)], cls)
    def tilt_row(self, x0, x1, y, z, depth, rise, cols=6, rows=2, cls='pv'):
        """A south-facing (+y) tilted panel row: front edge at y (low), back edge at y-depth (high)."""
        q = lambda u, v: (x0 + (x1 - x0) * u, y - depth * v, z + rise * v)
        out = [self.poly([q(0, 0), q(1, 0), q(1, 1), q(0, 1)], cls)]
        g = []
        for i in range(1, cols): g.append(f'M{P(*q(i / cols, 0))[0]:.1f},{P(*q(i / cols, 0))[1]:.1f}L{P(*q(i / cols, 1))[0]:.1f},{P(*q(i / cols, 1))[1]:.1f}')
        for j in range(1, rows): g.append(f'M{P(*q(0, j / rows))[0]:.1f},{P(*q(0, j / rows))[1]:.1f}L{P(*q(1, j / rows))[0]:.1f},{P(*q(1, j / rows))[1]:.1f}')
        out.append(f'<path class="pg" d="{"".join(g)}"/>')
        # the right-hand edge thickness and a glint along the top
        out.append(self.poly([q(1, 0), (x1, y, z - 2), (x1, y - depth, z + rise - 2), q(1, 1)], 'r'))
        return ''.join(out)
    def legs(self, pts3, h):
        return ''.join(self.line([(x, y, z), (x, y, z - h)], 'lg') for x, y, z in pts3)
    def cyl(self, x, y, z, r, h, body='l', top='t'):
        cx, by = P(x, y, z); _, ty = P(x, y, z + h)
        rx, ry = r * 1.2247, r * 0.7071
        self.pts += [(cx - rx, ty - ry), (cx + rx, by + ry)]
        return (f'<path class="{body}" d="M{cx - rx:.1f},{ty:.1f}L{cx - rx:.1f},{by:.1f}A{rx:.1f},{ry:.1f} 0 0 0 {cx + rx:.1f},{by:.1f}L{cx + rx:.1f},{ty:.1f}Z"/>'
                f'<ellipse class="{top}" cx="{cx:.1f}" cy="{ty:.1f}" rx="{rx:.1f}" ry="{ry:.1f}"/>')
    def ell(self, x, y, z, r, cls):
        cx, cy = P(x, y, z); rx, ry = r * 1.2247, r * 0.7071
        self.pts += [(cx - rx, cy - ry), (cx + rx, cy + ry)]
        return f'<ellipse class="{cls}" cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}"/>'
    def sun(self, x, y, z, r=16):
        cx, cy = P(x, y, z)
        self.pts += [(cx - r - 14, cy - r - 14), (cx + r + 14, cy + r + 14)]
        rays = ''.join(f'M{cx + math.cos(a) * (r + 6):.1f},{cy + math.sin(a) * (r + 6):.1f}L{cx + math.cos(a) * (r + 13):.1f},{cy + math.sin(a) * (r + 13):.1f}'
                       for a in [k * math.pi / 4 for k in range(8)])
        return f'<g class="sun"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}"/><path d="{rays}"/></g>'
    def flow(self, pts3, cls='fl'):
        return f'<polyline class="{cls}" points="{self._pts([P(*p) for p in pts3])}"/>'
    def plinth(self, x, y, w, d, h=8):
        return self.box(x, y, -h, w, d, h, 'pt', 'pl', 'pr')
    # ---- output ----
    def svg(self, label, extra_defs=''):
        xs = [p[0] for p in self.pts]; ys = [p[1] for p in self.pts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        s = min((VB_W - 2 * PAD) / (x1 - x0), (VB_H - 2 * PAD) / (y1 - y0))
        tx = (VB_W - (x1 - x0) * s) / 2 - x0 * s; ty = (VB_H - (y1 - y0) * s) / 2 - y0 * s
        body = ''.join(f'<g class="pc" style="--i:{k}">{svg}</g>' for k, svg in self.items)
        sun = ''
        if self.has_sun:
            cx, cy, r = VB_W - 58, 58, 15
            rays = ''.join(f'M{cx + math.cos(a) * (r + 6):.1f},{cy + math.sin(a) * (r + 6):.1f}L{cx + math.cos(a) * (r + 13):.1f},{cy + math.sin(a) * (r + 13):.1f}' for a in [k * math.pi / 4 for k in range(8)])
            sun = f'<g class="pc" style="--i:{self.k}"><g class="sun"><circle cx="{cx}" cy="{cy}" r="{r}"/><path d="{rays}"/></g></g>'
        return (f'<svg class="iso" viewBox="0 0 {VB_W} {VB_H}" role="img" aria-label="{label}">'
                f'{("<defs>" + "".join(self.defs) + extra_defs + "</defs>") if (self.defs or extra_defs) else ""}'
                f'<g transform="translate({tx:.1f} {ty:.1f}) scale({s:.4f})">{body}</g>{sun}</svg>')


def gable_house(S, x, y, W, D, H, R, o=8, panels=(2, 5), win_warm=False):
    """House with the ridge along x; the front (+y) roof slope carries the panels."""
    parts = [S.box(x, y, 0, W, D, H)]
    # windows + door on the +y wall
    fy = y + D
    for wx in (x + 16, x + 52, x + W - 46):
        parts.append(S.face_y(wx, fy, 18 if wx != x + 52 else 0, 26 if wx != x + 52 else 22, 30 if wx != x + 52 else 46, 'ww' if (win_warm and wx != x + 52) else ('dr' if wx == x + 52 else 'wn')))
    parts.append(S.face_x(x + W, y + 30, 22, 44, 26, 'wn'))
    rz = H + R; ry = y + D / 2
    front = [(x - o, fy + o, H - 4), (x + W + o, fy + o, H - 4), (x + W + o, ry, rz), (x - o, ry, rz)]
    gable = [(x + W, y, H), (x + W, y + D, H), (x + W, ry, rz)]
    parts.append(S.poly(gable, 'r'))
    parts.append(S.poly(front, 'rf'))
    S.piece(parts)
    # panels on the front slope
    rows, cols = panels
    u0, u1, v0, v1 = 0.12, 0.9, 0.16, 0.86
    def q(u, v):
        a = (x - o + (W + 2 * o) * u)
        return (a, fy + o + (ry - fy - o) * v, H - 4 + (rz - H + 4) * v + 1.2)
    pv = [S.poly([q(u0, v0), q(u1, v0), q(u1, v1), q(u0, v1)], 'pv')]
    g = []
    for i in range(1, cols):
        u = u0 + (u1 - u0) * i / cols; a, b = P(*q(u, v0)), P(*q(u, v1)); g.append(f'M{a[0]:.1f},{a[1]:.1f}L{b[0]:.1f},{b[1]:.1f}')
    for j in range(1, rows):
        v = v0 + (v1 - v0) * j / rows; a, b = P(*q(u0, v)), P(*q(u1, v)); g.append(f'M{a[0]:.1f},{a[1]:.1f}L{b[0]:.1f},{b[1]:.1f}')
    pv.append(f'<path class="pg" d="{"".join(g)}"/>')
    S.piece(pv)
    return q


def scenes():
    out = {}

    # 1. Residential solar ---------------------------------------------------
    S = Scene()
    S.piece([S.plinth(0, -6, 230, 160)])
    q = gable_house(S, 30, 20, 150, 100, 70, 46)
    S.piece([S.box(180, 70, 30, 4, 18, 24)])                                    # inverter on the gable wall
    S.piece([S.flow([q(0.86, 0.5), (185, 62, 98), (184, 79, 56)])])
    S.has_sun = True
    out['residential'] = S.svg('Illustration: a home with solar panels on its roof')

    # 2. Commercial & industrial ----------------------------------------------
    S = Scene()
    S.piece([S.plinth(-10, -10, 300, 290)])
    S.piece([S.box(10, 10, 0, 250, 130, 62), S.face_y(40, 140, 0, 46, 44, 'dr'), S.face_y(100, 140, 0, 46, 44, 'dr'),
             S.poly([(10, 140, 54), (260, 140, 54), (260, 140, 58), (10, 140, 58)], 'wn')])
    rows = []
    for k in range(5): rows.append(S.tilt_row(22, 248, 38 + k * 22, 63, 14, 7, cols=10, rows=1))
    S.piece(rows)
    grd = []
    for k in range(3):
        yk = 200 + k * 28
        grd.append(S.legs([(30, yk, 10), (240, yk, 10), (30, yk - 16, 18), (240, yk - 16, 18)], 10))
        grd.append(S.tilt_row(30, 240, yk, 10, 18, 9, cols=9, rows=2))
    S.piece(grd)
    S.piece([S.box(270, 150, 0, 14, 24, 26)])
    S.has_sun = True
    out['commercial'] = S.svg('Illustration: a factory with rooftop solar and a ground-mounted solar array')

    # 3. Lithium battery & inverter -------------------------------------------
    S = Scene()
    S.piece([S.plinth(-10, -10, 240, 150)])
    S.piece([S.box(0, 0, 0, 220, 10, 150, 't', 'wl', 'r')])                     # wall
    racks = []
    for rx in (14, 78):
        racks.append(S.box(rx, 34, 0, 56, 48, 118))
        for m in range(6):
            zz = 10 + m * 18
            racks.append(S.poly([(rx + 6, 82, zz), (rx + 50, 82, zz), (rx + 50, 82, zz + 14), (rx + 6, 82, zz + 14)], 'md'))
            racks.append(S.poly([(rx + 40, 82.2, zz + 5), (rx + 46, 82.2, zz + 5), (rx + 46, 82.2, zz + 9), (rx + 40, 82.2, zz + 9)], 'led'))
    S.piece(racks[:len(racks) // 2]); S.piece(racks[len(racks) // 2:])
    S.piece([S.box(152, 10, 62, 54, 16, 64), S.face_y(162, 26, 96, 34, 18, 'scr'),
             S.poly([(166, 26.2, 101), (172, 26.2, 101), (172, 26.2, 107), (166, 26.2, 107)], 'ac'),
             S.poly([(175, 26.2, 101), (181, 26.2, 101), (181, 26.2, 107), (175, 26.2, 107)], 'ac'),
             S.poly([(184, 26.2, 101), (190, 26.2, 101), (190, 26.2, 107), (184, 26.2, 107)], 'ac')])
    S.piece([S.flow([(178, 18, 62), (178, 18, 128), (110, 18, 128), (110, 34, 118)]), S.flow([(110, 18, 128), (46, 18, 128), (46, 34, 118)])])
    out['storage'] = S.svg('Illustration: lithium battery racks connected to a wall-mounted inverter')

    # 4. Hybrid solar & storage ------------------------------------------------
    S = Scene()
    S.piece([S.plinth(-10, -20, 290, 190)])
    S.piece([S.box(30, 20, 0, 130, 100, 64), S.face_y(48, 120, 16, 34, 30, 'ww'), S.face_y(96, 120, 0, 24, 46, 'dr'), S.face_x(160, 44, 20, 40, 26, 'wn')])
    S.piece([S.tilt_row(40, 150, 40 + k * 24, 65, 14, 8, cols=6, rows=1) for k in range(3)])
    S.piece([S.box(176, 74, 0, 24, 34, 56), S.poly([(178, 108.2, 12), (198, 108.2, 12), (198, 108.2, 40), (178, 108.2, 40)], 'md'),
             S.poly([(181, 108.4, 16), (195, 108.4, 16), (195, 108.4, 34), (181, 108.4, 34)], 'gauge')])
    S.piece([S.cyl(250, 20, 0, 4, 170), S.box(232, 16, 152, 36, 8, 4), S.line([(236, 20, 156), (196, -16, 150)], 'wire'), S.line([(264, 20, 156), (224, -16, 150)], 'wire')])
    S.piece([S.flow([(140, 66, 72), (166, 66, 72), (188, 74, 56)]), S.flow([(250, 20, 120), (162, 56, 54)], 'fg')])
    S.has_sun = True
    out['hybrid'] = S.svg('Illustration: a home with rooftop solar, a battery unit and a grid connection')

    # 5. Manufacturing -------------------------------------------------------
    S = Scene()
    S.piece([S.plinth(-10, -10, 300, 250)])
    fac = [S.box(10, 10, 0, 240, 120, 60)]
    for k in range(4):                                                          # saw-tooth roof
        x0 = 14 + k * 59
        fac.append(S.poly([(x0, 130, 60), (x0 + 59, 130, 60), (x0 + 59, 130, 60), (x0, 130, 60)], 't'))
        fac.append(S.poly([(x0, 14, 60), (x0, 126, 60), (x0, 126, 82), (x0, 14, 82)], 'gl'))
        fac.append(S.poly([(x0, 14, 82), (x0, 126, 82), (x0 + 59, 126, 60), (x0 + 59, 14, 60)], 'rf'))
    fac += [S.face_y(30, 130, 0, 56, 46, 'dr'), S.face_y(100, 130, 0, 56, 46, 'dr'), S.face_y(180, 130, 24, 50, 16, 'wn')]
    S.piece(fac)
    conv = [S.box(20, 170, 16, 230, 26, 5, 'cv', 'l', 'r'), S.legs([(30, 196, 16), (240, 196, 16), (135, 196, 16)], 16)]
    S.piece(conv)
    mods = []
    for k in range(5):
        mx = 34 + k * 44
        mods.append(S.box(mx, 175, 21, 26, 16, 14))
        mods.append(S.box(mx + 4, 179, 35, 4, 4, 3, 'ac', 'acl', 'acr'))
        mods.append(S.box(mx + 18, 179, 35, 4, 4, 3, 't', 'l', 'r'))
    S.piece(mods)
    S.piece([S.box(262, 150, 0, 24, 24, 12), S.box(262, 150, 12, 24, 24, 12), S.box(262, 176, 0, 24, 24, 12)])
    out['manufacturing'] = S.svg('Illustration: a factory with battery modules moving along a production line')

    # 6. Indoor & outdoor lighting -------------------------------------------
    S = Scene()
    gid = 'lgCone'
    S.defs.append(f'<radialGradient id="{gid}" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#F9C22E" stop-opacity=".55"/><stop offset="1" stop-color="#F9C22E" stop-opacity="0"/></radialGradient>'
                  '<linearGradient id="lgBeam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F9C22E" stop-opacity=".42"/><stop offset="1" stop-color="#F9C22E" stop-opacity=".02"/></linearGradient>')
    S.piece([S.plinth(-10, -10, 300, 260)])
    S.piece([S.poly([(-10, 170, 0.5), (290, 170, 0.5), (290, 220, 0.5), (-10, 220, 0.5)], 'road'),
             S.line([(0, 195, 0.8), (280, 195, 0.8)], 'lane')])
    S.piece([f'<ellipse cx="{P(120, 80, 0)[0]:.1f}" cy="{P(120, 80, 0)[1]:.1f}" rx="{130 * 1.2247:.1f}" ry="{130 * .7071:.1f}" fill="url(#{gid})" class="glow"/>'])
    hx, hy = P(120, 80, 214)
    bx0, by0 = P(120 - 95, 80 + 95, 0); bx1, by1 = P(120 + 95, 80 - 95, 0)
    S.piece([f'<path class="beam" d="M{hx - 14:.1f},{hy + 6:.1f}L{bx0:.1f},{by0:.1f}L{bx1:.1f},{by1:.1f}L{hx + 14:.1f},{hy + 6:.1f}Z" fill="url(#lgBeam)"/>',
             S.cyl(120, 80, 0, 7, 200), S.box(110, 70, 0, 20, 20, 6)])
    head = [S.ell(120, 80, 210, 24, 'ring')]
    for a in range(6):
        ang = a * math.pi / 3
        lx, ly = 120 + math.cos(ang) * 24, 80 + math.sin(ang) * 24
        head.append(S.box(lx - 4, ly - 4, 204, 8, 8, 8, 'lamp', 'lampl', 'lampr'))
    S.piece(head)
    for k, sx in enumerate((10, 150)):
        cx_, cy_ = P(sx + 26, 160, 74)
        gx0, gy0 = P(sx + 26 - 26, 160 + 26, 0); gx1, gy1 = P(sx + 26 + 26, 160 - 6, 0)
        S.piece([f'<path class="beam" d="M{cx_ - 5:.1f},{cy_ + 2:.1f}L{gx0:.1f},{gy0:.1f}L{gx1:.1f},{gy1:.1f}L{cx_ + 5:.1f},{cy_ + 2:.1f}Z" fill="url(#lgBeam)"/>',
                 S.cyl(sx, 160, 0, 2.6, 80), S.line([(sx, 160, 78), (sx + 26, 160, 76)], 'arm'), S.box(sx + 20, 156, 70, 14, 8, 4, 'lamp', 'lampl', 'lampr')])
    out['lighting'] = S.svg('Illustration: a high-mast light and streetlights lighting a road at night')

    # 7. Energy consultancy ----------------------------------------------------
    S = Scene()
    S.piece([S.plinth(-10, -10, 300, 200)])
    bld = [S.box(10, 10, 0, 100, 80, 96)]
    for r_ in range(4):
        for c_ in range(3):
            bld.append(S.face_y(20 + c_ * 30, 90, 14 + r_ * 20, 20, 12, 'wn'))
        bld.append(S.face_x(110, 18, 14 + r_ * 20, 60, 12, 'wn'))
    S.piece(bld)
    heights = [34, 52, 44, 70, 96]
    bars = []
    for k, h in enumerate(heights):
        cls = ('ac', 'acl', 'acr') if k == 4 else ('t', 'l', 'r')
        bars.append(S.box(140 + k * 26, 120, 0, 16, 16, h, *cls))
    S.piece(bars[:3]); S.piece(bars[3:])
    tops = [(148 + k * 26, 128, h + 22) for k, h in enumerate(heights)]
    S.piece([S.flow(tops, 'trend')] + [f'<circle class="dot" cx="{P(*t)[0]:.1f}" cy="{P(*t)[1]:.1f}" r="3.4"/>' for t in tops])
    out['consultancy'] = S.svg('Illustration: a building beside an energy chart with rising bars')

    # 8. Operations & maintenance ----------------------------------------------
    S = Scene()
    S.piece([S.plinth(-10, -10, 300, 210)])
    rows_ = []; clip = []
    for k in range(3):
        yk = 50 + k * 50
        rows_.append(S.legs([(14, yk, 14), (250, yk, 14), (14, yk - 22, 26), (250, yk - 22, 26)], 14))
        rows_.append(S.tilt_row(14, 250, yk, 14, 26, 12, cols=10, rows=2))
        a = [P(14, yk, 14), P(250, yk, 14), P(250, yk - 26, 26), P(14, yk - 26, 26)]
        clip.append('<polygon points="' + ' '.join(f'{u:.1f},{v:.1f}' for u, v in a) + '"/>')
    S.defs.append('<clipPath id="omClip">' + ''.join(clip) + '</clipPath>')
    S.piece(rows_[:2]); S.piece(rows_[2:4]); S.piece(rows_[4:])
    # scanning band (moves along +x in the page's CSS)
    p0, p1, p2 = P(14, 200, 0), P(14, -40, 60), P(26, -40, 60)
    p3 = P(26, 200, 0)
    S.piece([f'<g clip-path="url(#omClip)"><polygon class="scan" points="{p0[0]:.1f},{p0[1]:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} {p3[0]:.1f},{p3[1]:.1f}"/></g>'], step=False)
    S.piece([S.box(262, 150, 0, 22, 30, 38), S.face_y(266, 180, 20, 14, 10, 'scr')])
    bx, by = P(273, 165, 74)
    S.pts += [(bx - 16, by - 16), (bx + 16, by + 16)]
    S.piece([f'<g class="badge"><circle cx="{bx:.1f}" cy="{by:.1f}" r="14"/><path d="M{bx - 6:.1f},{by:.1f}l4,4l8,-8"/></g>', S.line([(273, 165, 38), (273, 165, 58)], 'arm')])
    out['maintenance'] = S.svg('Illustration: rows of solar panels being inspected, with a check mark above the inverter')
    return out

ISO_CSS = '''
.iso{display:block;width:100%;height:100%}
.iso polygon,.iso path,.iso ellipse,.iso polyline{stroke:rgba(255,255,255,.3);stroke-width:1;stroke-linejoin:round;vector-effect:non-scaling-stroke}
.iso .t{fill:#2A2A31}.iso .l{fill:#1D1D22}.iso .r{fill:#141418}
.iso .pt{fill:#1F1F24;stroke:rgba(255,255,255,.18)}.iso .pl{fill:#16161A;stroke:rgba(255,255,255,.14)}.iso .pr{fill:#0F0F12;stroke:rgba(255,255,255,.12)}
.iso .rf{fill:#33333B}.iso .wl{fill:#1A1A1F}.iso .gl{fill:#2C3446;stroke:rgba(190,205,255,.35)}
.iso .pv{fill:#1C2740;stroke:rgba(170,190,240,.55)}.iso .pg{fill:none;stroke:rgba(190,205,255,.3)}
.iso .wn{fill:#0B0B0D;stroke:rgba(255,255,255,.32)}.iso .ww{fill:rgba(249,194,46,.55);stroke:rgba(249,194,46,.8)}.iso .dr{fill:#3A2E22;stroke:rgba(255,255,255,.3)}
.iso .md{fill:#232329;stroke:rgba(255,255,255,.22)}.iso .led{fill:#F9C22E;stroke:none}.iso .scr{fill:#0B0B0D;stroke:rgba(255,255,255,.4)}
.iso .ac{fill:#F9C22E;stroke:rgba(9,9,11,.5)}.iso .acl{fill:#C99412;stroke:rgba(9,9,11,.5)}.iso .acr{fill:#9C7208;stroke:rgba(9,9,11,.5)}
.iso .gauge{fill:#F9C22E;stroke:none;opacity:.9}
.iso .cv{fill:#3A3A42}
.iso .lg,.iso .arm,.iso .wire{fill:none;stroke:rgba(255,255,255,.4)}
.iso .wire{stroke:rgba(255,255,255,.35)}
.iso .road{fill:#121215;stroke:none}.iso .lane{fill:none;stroke:rgba(255,255,255,.4);stroke-dasharray:8 8}
.iso .ring{fill:none;stroke:rgba(255,255,255,.55);stroke-width:1.5}
.iso .lamp{fill:#FFE7A3;stroke:#F9C22E}.iso .lampl{fill:#F9C22E;stroke:#F9C22E}.iso .lampr{fill:#D9A21C;stroke:#F9C22E}
.iso .beam,.iso .glow{stroke:none}
.iso .sun circle{fill:none;stroke:#F9C22E;stroke-width:1.6}.iso .sun path{fill:none;stroke:#F9C22E;stroke-width:1.6;stroke-linecap:round}
.iso .fl,.iso .fg,.iso .trend{fill:none;stroke:#F9C22E;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:2 7}
.iso .fg{stroke:#fff;opacity:.75}
.iso .trend{stroke-dasharray:none;stroke-width:1.6}
.iso .dot{fill:#09090B;stroke:#F9C22E;stroke-width:1.6}
.iso .scan{fill:rgba(249,194,46,.45);stroke:none}
.iso .badge circle{fill:#F9C22E;stroke:none}.iso .badge path{fill:none;stroke:#09090B;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
'''

if __name__ == '__main__':
    sc = scenes()
    html = '<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;background:#0E0E11;display:grid;grid-template-columns:repeat(4,1fr);gap:8px;padding:8px}div{background:#0E0E11;border:1px solid #333;aspect-ratio:560/440}' + ISO_CSS + '</style></head><body>' + ''.join(f'<div>{v}</div>' for v in sc.values()) + '</body></html>'
    open('/tmp/claude-0/site/iso_test.html', 'w').write(html)
    print({k: len(v) for k, v in sc.items()})
