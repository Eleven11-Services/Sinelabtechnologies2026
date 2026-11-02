import json, math
rings = json.load(open('/tmp/claude-0/geo/india_rings.json'))
LON0, LON1, LAT0, LAT1 = 75.55, 77.35, 9.75, 10.95
C = math.cos(math.radians((LAT0 + LAT1) / 2))
W = 1000; K = W / ((LON1 - LON0) * C); H = (LAT1 - LAT0) * K
def P(lon, lat): return ((lon - LON0) * C * K, (LAT1 - lat) * K)
ring = rings[0]
# keep the part of the ring inside a padded box, as one path (outside points are clamped to the frame so the land fills correctly)
pad = 0.3
def clip(poly, edge):   # Sutherland-Hodgman against one side of the box
    out = []
    inside = lambda p: edge(p)[0]
    for i in range(len(poly)):
        cur, prev = poly[i], poly[i - 1]
        ci, pi = inside(cur), inside(prev)
        if ci:
            if not pi: out.append(edge((prev, cur))[1])
            out.append(cur)
        elif pi: out.append(edge((prev, cur))[1])
    return out
def mk(axis, val, keep_greater):
    def f(arg):
        if isinstance(arg[0], tuple) or isinstance(arg[0], list):
            (x1, y1), (x2, y2) = arg
            a1, a2 = (x1, x2) if axis == 0 else (y1, y2)
            t = (val - a1) / (a2 - a1)
            return (None, (x1 + (x2 - x1) * t, y1 + (y2 - y1) * t))
        v = arg[axis]
        return ((v >= val) if keep_greater else (v <= val), None)
    return f
pts = [tuple(p) for p in ring]
for e in [mk(0, LON0 - pad, True), mk(0, LON1 + pad, False), mk(1, LAT0 - pad, True), mk(1, LAT1 + pad, False)]:
    pts = clip(pts, e)
d = 'M' + ' L'.join(f'{P(x,y)[0]:.1f},{P(x,y)[1]:.1f}' for x, y in pts) + 'Z'
print(len(pts), W, round(H))
json.dump({'d': d, 'W': W, 'H': H}, open('/tmp/claude-0/geo/land.json', 'w'))
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H:.0f}"><rect width="{W}" height="{H:.0f}" fill="#dfe4ea"/><path d="{d}" fill="#f3f3f5" stroke="#fff" stroke-width="2"/>'
for name, lat, lon in [('Kochi', 9.9771, 76.3144), ('Palakkad', 10.766, 76.6761), ('Thrissur', 10.5276, 76.2144)]:
    x, y = P(lon, lat); svg += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="8" fill="#09090B"/><text x="{x+12:.0f}" y="{y+5:.0f}" font-size="22">{name}</text>'
svg += '</svg>'
open('/tmp/claude-0/geo/test.svg', 'w').write(svg)
