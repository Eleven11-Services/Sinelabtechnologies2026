#!/usr/bin/env python3
"""Make a homepage "Projects in motion" clip from a still drone photo: a slow, eased push-in towards a point.
Used until Sinelab sends real drone videos. Needs: pip install pillow ; ffmpeg on PATH.

    python3 tools/make_film.py assets-source/photos/projects/sinicon.jpg sinicon --focus 0.62,0.38 --zoom 1.13 --seconds 3

Writes into site/:
    media/<key>.mp4 and media/<key>.webm      (1920x1080, silent; the page picks MP4 or WebM automatically)
    assets/img/film_<key>.webp                 poster shown before the clip plays (1280 wide)
    assets/img/film_<key>_t.webp               tab thumbnail (400x225)
Then add/replace the <article class="film"> slide and its tab button in site/index.html (section#films).
For a real drone video instead: ffmpeg -i in.mov -t 8 -vf "scale=1920:-2" -c:v libx264 -crf 22 -maxrate 3200k -bufsize 6400k \
    -pix_fmt yuv420p -movflags +faststart -an site/media/<key>.mp4   (and a WebM: -c:v libvpx-vp9 -b:v 0 -crf 33)
"""
import argparse, os, subprocess
from PIL import Image, ImageFilter, ImageOps

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('key')
ap.add_argument('--focus', default='0.5,0.5', help='where the zoom ends, as fractions x,y')
ap.add_argument('--zoom', type=float, default=1.12, help='final zoom factor (1.10–1.15 suits a 3 s clip)')
ap.add_argument('--seconds', type=float, default=3)
a = ap.parse_args()
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
W, H, FPS = 1920, 1080, 24
im = ImageOps.exif_transpose(Image.open(a.src)).convert('RGB'); IW, IH = im.size
if IW / IH > W / H:   # crop the source to 16:9 first
    nw = IH * W / H; im = im.crop((round((IW - nw) / 2), 0, round((IW + nw) / 2), IH))
else:
    nh = IW * H / W; im = im.crop((0, round((IH - nh) / 2), IW, round((IH + nh) / 2)))
IW, IH = im.size; fx, fy = (float(v) for v in a.focus.split(','))
SH = ImageFilter.UnsharpMask(radius=1.1, percent=55, threshold=2)
os.makedirs(os.path.join(ROOT, 'media'), exist_ok=True)
im.resize((1280, 720), Image.LANCZOS).filter(SH).save(os.path.join(ROOT, 'assets/img', f'film_{a.key}.webp'), 'WEBP', quality=78, method=6)
im.resize((400, 225), Image.LANCZOS).save(os.path.join(ROOT, 'assets/img', f'film_{a.key}_t.webp'), 'WEBP', quality=80, method=6)
mp4 = os.path.join(ROOT, 'media', f'{a.key}.mp4'); webm = os.path.join(ROOT, 'media', f'{a.key}.webm')
p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', '22', '-maxrate', '3200k', '-bufsize', '6400k',
                      '-preset', 'slow', '-movflags', '+faststart', '-an', mp4], stdin=subprocess.PIPE)
N = int(FPS * a.seconds)
for i in range(N):
    t = i / (N - 1); t = t * t * (3 - 2 * t); z = 1 + (a.zoom - 1) * t
    cw, ch = IW / z, IH / z
    cx = IW / 2 + (fx * IW - IW / 2) * t; cy = IH / 2 + (fy * IH - IH / 2) * t
    cx = min(max(cx, cw / 2), IW - cw / 2); cy = min(max(cy, ch / 2), IH - ch / 2)
    p.stdin.write(im.resize((W, H), Image.LANCZOS, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)).filter(SH).tobytes())
p.stdin.close(); p.wait()
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp4, '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '33', '-row-mt', '1', '-an', webm], check=True)
for f in (mp4, webm): print(f, os.path.getsize(f) // 1024, 'KB')
