# WebP versions of every site image (user, 29 Oct: "convert all images to webp and optimise performance").
# webp(path) returns a cached .webp next to nothing in layers/: /tmp/claude-0/site/webp/<name>.webp
# Photos: longest side capped at 1920 px, quality 76. Images with transparency (logos, panel texture): near-lossless.
import os
from PIL import Image
CACHE = '/tmp/claude-0/site/webp/'
os.makedirs(CACHE, exist_ok=True)
MAXW = 1920
def maxw(name):   # cards, thumbnails and portraits never show wider than ~600 css px, so 1200 px covers 2x screens
    if name.startswith('film_') and not name.endswith('_t'): return 1280   # video posters: shown for a moment before the clip plays
    return 1200 if any(k in name for k in ('_card', '_sq', '_tall', '_t', 'thumb', 'g_')) else MAXW
def webp(path):
    if path.lower().endswith('.webp'): return path
    name = os.path.splitext(os.path.basename(path))[0]
    out = CACHE + name + '.webp'
    if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(path): return out
    im = Image.open(path)
    alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
    im = im.convert('RGBA' if alpha else 'RGB')
    W = maxw(name)
    if im.width > W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    if alpha: im.save(out, 'WEBP', quality=92, alpha_quality=100, method=6)
    else: im.save(out, 'WEBP', quality=72, method=6)
    return out
