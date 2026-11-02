#!/usr/bin/env python3
"""Turn a photo into a WebP for the site, sized and cropped the way the site uses images.

    pip install pillow

Examples
    # card for the Projects page and gallery highlights (5:4)
    python3 tools/to_webp.py assets-source/photos/projects/sinicon.jpg --crop 5:4 --focus 0.62,0.4 --max 1200 -o site/assets/img/real_sinicon_card.webp
    # homepage project slider (16:10)
    python3 tools/to_webp.py photo.jpg --crop 16:10 --max 1600 -o site/assets/img/real_x_slide.webp
    # gallery photo (keep the whole frame)
    python3 tools/to_webp.py photo.jpg --max 1600 -o site/assets/img/real_x.webp
    # team portraits: square for About, 3:4 for the homepage cards
    python3 tools/to_webp.py face.jpg --crop 1:1 --focus 0.5,0.35 --max 800 -o site/assets/img/team_name_sq.webp
    python3 tools/to_webp.py face.jpg --crop 3:4 --focus 0.5,0.3 --max 960 -o site/assets/img/team_name_tall.webp

Defaults match the rest of the site: quality 72 for photos, transparency kept (near-lossless) for logos/PNG cut-outs.
"""
import argparse, os
from PIL import Image, ImageOps

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('src')
ap.add_argument('-o', '--out', help='output .webp path (default: next to the source)')
ap.add_argument('--max', type=int, default=1920, help='longest side in px after cropping (default 1920)')
ap.add_argument('--q', type=int, default=72, help='WebP quality for photos (default 72)')
ap.add_argument('--crop', help='aspect ratio to crop to, e.g. 5:4, 16:10, 1:1, 3:4')
ap.add_argument('--focus', default='0.5,0.5', help='crop centre as fractions x,y (default 0.5,0.5)')
a = ap.parse_args()

im = ImageOps.exif_transpose(Image.open(a.src))
alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
im = im.convert('RGBA' if alpha else 'RGB')
if a.crop:
    rw, rh = (float(v) for v in a.crop.split(':')); ar = rw / rh
    fx, fy = (float(v) for v in a.focus.split(','))
    W, H = im.size
    if W / H > ar: h = H; w = h * ar
    else: w = W; h = w / ar
    cx = min(max(fx * W, w / 2), W - w / 2); cy = min(max(fy * H, h / 2), H - h / 2)
    im = im.crop((round(cx - w / 2), round(cy - h / 2), round(cx + w / 2), round(cy + h / 2)))
if max(im.size) > a.max:
    s = a.max / max(im.size); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
out = a.out or os.path.splitext(a.src)[0] + '.webp'
if alpha: im.save(out, 'WEBP', quality=92, alpha_quality=100, method=6)
else: im.save(out, 'WEBP', quality=a.q, method=6)
print(f'{out}  {im.width}x{im.height}  {os.path.getsize(out) // 1024} KB')
