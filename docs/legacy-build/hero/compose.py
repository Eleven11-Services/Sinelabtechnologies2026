# Clean wide hero (2410x1196) from the original 1536x1024 photo, without mirrored or blurred trees.
# Layers per side band: smooth sky -> distant treeline -> tree crown that ends with a real leafy edge -> hedge -> bed + lawn.
import numpy as np
from PIL import Image
from scipy import ndimage
rng = np.random.default_rng(11)
W, H, DX, DY = 2410, 1196, 437, 172
O = np.asarray(Image.open('/tmp/claude-0/hero/day.jpg').convert('RGB')).astype(np.float32) / 255
def o(x0, x1, y0, y1): return O[y0:y1, x0:x1].copy()
# ---- 1. sky: row profile measured from the photo (top is deeper blue, horizon paler), plus fine grain ----
rows = np.array([-172, 0, 25, 50, 75, 100, 125, 150, 175, 200, 260, 330, 1024])
cols = np.array([[.40, .53, .74], [.529, .643, .808], [.573, .675, .839], [.608, .706, .863], [.647, .737, .882], [.686, .776, .902],
                 [.729, .804, .925], [.776, .831, .941], [.80, .859, .953], [.827, .875, .953], [.84, .88, .955], [.865, .9, .962], [.87, .9, .962]])
yy = np.arange(H) - DY
SKY = np.stack([np.interp(yy, rows, cols[:, c]) for c in range(3)], 1)[:, None, :] * np.ones((1, W, 1))
SKY += rng.normal(0, .006, SKY.shape)
C = SKY.copy()
def skyness(p, cloud_rows=None):
    r, g, b = p[..., 0], p[..., 1], p[..., 2]
    s = np.clip(((b - r) - 0.04) / 0.06, 0, 1) * np.clip((b - 0.48) / 0.08, 0, 1)
    cl = np.clip((p.mean(2) - 0.72) / 0.08, 0, 1) * np.clip((0.14 - (p.max(2) - p.min(2))) / 0.06, 0, 1)   # pale clouds count as sky too
    if cloud_rows is not None: cl[cloud_rows:] = 0
    return ndimage.gaussian_filter(np.maximum(s, cl), 0.7)
def put(p, x, y, alpha=None, fl=0, fr=0, ft=0, fb=0):
    """composite patch p (orig-space colours) at scene (x,y); alpha defaults to 1; feathers in px on each side"""
    h, w = p.shape[:2]
    a = np.ones((h, w)) if alpha is None else alpha.copy()
    if fl: a[:, :fl] *= np.linspace(0, 1, fl)[None]
    if fr: a[:, w - fr:] *= np.linspace(1, 0, fr)[None]
    if ft: a[:ft] *= np.linspace(0, 1, ft)[:, None]
    if fb: a[h - fb:] *= np.linspace(1, 0, fb)[:, None]
    X0, Y0 = max(0, x), max(0, y); X1, Y1 = min(W, x + w), min(H, y + h)
    if X1 <= X0 or Y1 <= Y0: return
    pa = p[Y0 - y:Y1 - y, X0 - x:X1 - x]; aa = a[Y0 - y:Y1 - y, X0 - x:X1 - x, None]
    C[Y0:Y1, X0:X1] = C[Y0:Y1, X0:X1] * (1 - aa) + pa * aa
def fol(p): return 1 - skyness(p)          # foliage alpha: real sky pixels in a patch are replaced by our sky
S = lambda x: x + DX                        # orig x -> scene x
T = lambda y: y + DY                        # orig y -> scene y
