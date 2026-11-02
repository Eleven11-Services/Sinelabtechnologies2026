import cv2, numpy as np, os
from PIL import Image, ImageOps
casc = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml'))
P = {'sunil':'img1.jpg','sajeev':'img2.jpg','ravinder':'img3.jpg','athul':'img4.jpg','sravan':'img5.jpg','leenu':'leenu-000.jpg','saran':'saran-000.jpg'}
L = '/tmp/claude-0/site/layers/'
def box(W,H,cx,top,w,h):
    s = min(1, W / w, H / h); w, h = w * s, h * s
    x0 = min(max(cx - w/2, 0), W - w); y0 = min(max(top, 0), H - h)
    return (round(x0), round(y0), round(x0 + w), round(y0 + h))
sheet = []
for k, f in P.items():
    im = ImageOps.exif_transpose(Image.open(f)).convert('RGB'); W, H = im.size
    g = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
    fs = casc.detectMultiScale(g, 1.1, 6, minSize=(int(W*.12), int(W*.12)))
    fx, fy, fw, fh = max(fs, key=lambda r: r[2]*r[3])
    print(k, (W,H), 'face', fx, fy, fw, fh, flush=True)
    cx = fx + fw/2
    sq = im.crop(box(W,H,cx, fy - .62*fh, 2.5*fw, 2.5*fw)).resize((800,800), Image.LANCZOS)
    tw = 2.3*fw; tall = im.crop(box(W,H,cx, fy - .55*fh, tw, tw*4/3)).resize((720,960), Image.LANCZOS)
    sq.save(L + f'team_{k}_sq.jpg', quality=84, optimize=True, progressive=True)
    tall.save(L + f'team_{k}_tall.jpg', quality=84, optimize=True, progressive=True)
    sheet.append((sq, tall))
S = Image.new('RGB', (7*310, 330+410), 'white')
for i,(sq,tall) in enumerate(sheet):
    S.paste(sq.resize((300,300)), (i*310, 0)); S.paste(tall.resize((300,400)), (i*310, 330))
S.save('crops.jpg', quality=80)
