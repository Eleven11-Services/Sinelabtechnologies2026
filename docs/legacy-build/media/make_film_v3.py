# Sharper milestone clips (user: "upscale the milestone images a bit"): Full HD, Lanczos resampling, light sharpening,
# higher quality encode, and a 2400x1350 poster so the still is crisp on high-density screens.
import subprocess, sys
from PIL import Image, ImageFilter
key, src, fx, fy, zend = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
W, H, FPS, SEC = 1920, 1080, 24, float(sys.argv[6]) if len(sys.argv) > 6 else 10
im = Image.open(src).convert('RGB'); IW, IH = im.size
SH = ImageFilter.UnsharpMask(radius=1.1, percent=55, threshold=2)
im.resize((2400, round(2400 * IH / IW)), Image.LANCZOS, box=(0, 0, IW, IH)).filter(SH).crop((0, 0, 2400, 1350)).save(f'{key}_poster.jpg', quality=84, optimize=True, progressive=True)
im.resize((400, 225), Image.LANCZOS).save(f'{key}_t.jpg', quality=84)
N = int(FPS * SEC)
def ease(t): return t * t * (3 - 2 * t)
p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-crf', '21', '-preset', 'slow', '-tune', 'film', '-movflags', '+faststart', '-an', f'{key}.mp4'], stdin=subprocess.PIPE)
for i in range(N):
    t = ease(i / (N - 1)); z = 1 + (zend - 1) * t
    cw, ch = IW / z, IH / z
    cx = IW / 2 + (fx * IW - IW / 2) * t; cy = IH / 2 + (fy * IH - IH / 2) * t
    cx = min(max(cx, cw / 2), IW - cw / 2); cy = min(max(cy, ch / 2), IH - ch / 2)
    fr = im.resize((W, H), Image.LANCZOS, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)).filter(SH)
    p.stdin.write(fr.tobytes())
p.stdin.close(); p.wait()
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{key}.mp4', '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '33', '-row-mt', '1', '-deadline', 'good', '-cpu-used', '3', '-an', f'{key}.webm'])
print(key, 'done', flush=True)
