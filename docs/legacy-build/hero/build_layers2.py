from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage
rng=np.random.default_rng(3)
im=Image.open('/tmp/claude-0/hero2/wide_clean.png').convert('RGB'); W,H=im.size
A=np.asarray(im).astype(float)/255
dx,dy=437,172
r,g,b=A[...,0],A[...,1],A[...,2]
cand=((b>r+0.06)&(b>0.5))|(A.mean(2)>0.8)
cand[dy+448:, 437:1973]=False; cand[dy+662:]=False   # bands: open sky reaches down to the hedges
lab,n=ndimage.label(cand); top=set(np.unique(lab[0:3,:]))-{0}
sky=np.isin(lab,list(top))
ex=np.load('/tmp/claude-0/hero/edge.npy')   # detected gable edge for x 150..1225 (orig coords)
det=dict(zip(ex[0].astype(int),ex[1]))
def topY(x):
    if x<300: return det.get(x,400)
    if x<=1017: return 178+0.105*(x-300)
    if x<=1215: return 254+(345-254)*(x-1017)/(1215-1017)
    return 345
pts=[(x,topY(x)) for x in range(150,1216)]+[(1222,345),(1222,351),(1203,367),(1142,371),(1142,452),(150,452)]
house=Image.new('L',(W,H),0); d=ImageDraw.Draw(house)
d.polygon([(x+dx,y+dy) for x,y in pts],fill=255)
d.polygon([(x+dx,y+dy) for x,y in [(700,548),(860,438),(1300,436),(1510,548)]],fill=255)
hm=np.asarray(house)>0
# light, sky-coloured pixels just inside the roof outline still count as sky (no pale seam)
light=(A.mean(2)>0.78)&(b>r)
band=ndimage.binary_dilation(~hm,iterations=6)&hm
sky=(sky&~hm)|(band&light)
holes=cand&~ndimage.binary_dilation(hm,iterations=14); holes[dy+560:]=False   # sky seen through gaps inside the tree crowns
sky=sky|holes
sky=ndimage.binary_opening(sky,iterations=1)
sky=ndimage.gaussian_filter(sky.astype(float),1.1)[...,None]
yy=np.arange(H)[:,None]*np.ones((1,W)); horizon=dy+470
def grad(stops):
    out=np.zeros((H,W,3)); ys=[s[0] for s in stops]
    for c in range(3): out[...,c]=np.interp(yy/horizon, ys, [s[1][c]/255 for s in stops])
    return out
wins=[(428,336,612,478),(612,336,680,412),(798,356,852,402),(905,362,1062,442),(283,330,322,406),
      (430,577,678,782),(935,594,1152,738),(1248,592,1376,666),(283,586,336,692)]
wins=[(a+dx,b2+dy,c+dx,e+dy) for a,b2,c,e in wins]
wmask=Image.new('L',(W,H),0); dd=ImageDraw.Draw(wmask)
for rr in wins: dd.rectangle(rr,fill=255)
wm=np.asarray(wmask).astype(float)/255
wm_soft=ndimage.gaussian_filter(wm,1.5)[...,None]
halo=ndimage.gaussian_filter(wm,30)[...,None]
spill=np.zeros((H,W))
for x0,y0,x1,y1 in wins:
    if y1>dy+560: spill[y1:min(H,y1+120),x0-20:x1+20]=np.linspace(1,0,min(H,y1+120)-y1)[:,None]
spill=ndimage.gaussian_filter(spill,25)[...,None]
lm=np.zeros((H,W))
for x,y in [(775,612),(1210,622)]: lm[y+dy-4:y+dy+4,x+dx-4:x+dx+4]=1
lamph=ndimage.gaussian_filter(lm,20)[...,None]*50
lampc=ndimage.gaussian_filter(lm,2.5)[...,None]*5
warm=np.array([1.0,0.72,0.36])

import json, os
OUT='/tmp/claude-0/site/layers/'
skym=sky[...,0]
alpha=np.clip(1-skym,0,1)
np.save('/tmp/claude-0/hero2/skym.npy',skym)
def base(kind):
    if kind=='dusk': return np.clip(A*np.array([0.98,0.74,0.56])*0.74,0,1)
    return np.clip(A*np.array([0.22,0.27,0.40]),0,1)
def save_rgba(arr,al,path,q=82):
    im=Image.fromarray((np.dstack([arr,al[...,None]])*255).astype(np.uint8),'RGBA')
    im.save(path,'WEBP',quality=q,method=6)
# edge clean-up: pixels on the soft edge between foliage and sky still carry daylight sky colour, which showed as a
# pale outline at dusk and night. Give every edge pixel the colour of the nearest solid foliage pixel instead.
solid = alpha > 0.97
_, (iy, ix) = ndimage.distance_transform_edt(~solid, return_indices=True)
A_fg = np.where(solid[..., None], A, A[iy, ix])
alpha = np.clip((alpha - 0.08) / 0.92, 0, 1)          # and pull the soft edge in by a hair
A_day = A; A = A_fg
save_rgba(A,alpha,OUT+'fg_day.webp')
dusk_b=base('dusk'); night_b=base('night')
save_rgba(dusk_b,alpha,OUT+'fg_dusk.webp')
save_rgba(night_b,alpha,OUT+'fg_night.webp')
Image.fromarray((A_day*255).astype(np.uint8)).save(OUT+'day.jpg',quality=84)
# stars (transparent)
st=np.zeros((H,W)); n=700
xs=rng.integers(0,W,n); ys=rng.integers(0,int(H*0.5),n); st[ys,xs]=rng.uniform(.35,1,n)
st=np.clip(ndimage.gaussian_filter(st,0.8)*3.2,0,1)*skym
Image.fromarray((np.dstack([np.ones((H,W,3)),st[...,None]])*255).astype(np.uint8),'RGBA').save(OUT+'stars.webp','WEBP',quality=80)
# light layers as screen-blend images
lit_col=lambda: np.clip(A*warm*1.25+warm*0.28,0,1)
LIT=lit_col()
def screen_layer(target,basei):
    return np.clip(1-(1-target)/np.maximum(1-basei,1e-3),0,1)
layers=[]
order=[5,6,0,3,8,1,2,7,4]   # living room first, then upstairs, then the small ones
for rank,i in enumerate(order):
    x0,y0,x1,y1=wins[i]
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).rectangle((x0,y0,x1,y1),fill=255)
    m=np.asarray(m).astype(float)/255
    ms=ndimage.gaussian_filter(m,1.5)[...,None]
    hal=ndimage.gaussian_filter(m,30)[...,None]
    sp=np.zeros((H,W))
    if y1>dy+560: sp[y1:min(H,y1+120),x0-20:x1+20]=np.linspace(1,0,min(H,y1+120)-y1)[:,None]
    sp=ndimage.gaussian_filter(sp,25)[...,None]
    tgt=night_b*(1-ms)+LIT*ms
    tgt=1-(1-tgt)*(1-np.clip(hal*0.22+sp*0.35,0,1)*warm)
    L=screen_layer(tgt,night_b)
    ys_,xs_=np.where(L.max(2)>0.012)
    bx0,bx1,by0,by1=xs_.min(),xs_.max()+1,ys_.min(),ys_.max()+1
    crop=(L[by0:by1,bx0:bx1]*255).astype(np.uint8)
    fn=f'win{rank}.jpg'; Image.fromarray(crop).save(OUT+fn,quality=82)
    layers.append(dict(f=fn,x=bx0/W*100,y=by0/H*100,w=(bx1-bx0)/W*100,h=(by1-by0)/H*100,kind='win'))
for j,(x,y) in enumerate([(775,612),(1210,622)]):
    l=np.zeros((H,W)); l[y+dy-4:y+dy+4,x+dx-4:x+dx+4]=1
    gl=np.clip((ndimage.gaussian_filter(l,20)*50+ndimage.gaussian_filter(l,2.5)*5)[...,None]*warm,0,1)
    tgt=1-(1-night_b)*(1-gl)
    L=screen_layer(tgt,night_b)
    ys_,xs_=np.where(L.max(2)>0.012)
    bx0,bx1,by0,by1=xs_.min(),xs_.max()+1,ys_.min(),ys_.max()+1
    fn=f'lamp{j}.jpg'; Image.fromarray((L[by0:by1,bx0:bx1]*255).astype(np.uint8)).save(OUT+fn,quality=85)
    layers.append(dict(f=fn,x=bx0/W*100,y=by0/H*100,w=(bx1-bx0)/W*100,h=(by1-by0)/H*100,kind='lamp'))
# panel mask
pm=hm&(b>r+0.12)&(A.mean(2)<0.72)&(b>0.3)&(skym<0.5)
pm=ndimage.binary_closing(ndimage.binary_opening(pm,iterations=1),iterations=2)
lab2,n2=ndimage.label(pm); sizes=ndimage.sum(pm,lab2,range(1,n2+1))
keep=np.isin(lab2,[i+1 for i,sz in enumerate(sizes) if sz>800])
Image.fromarray((ndimage.gaussian_filter(keep.astype(float),0.8)*255).astype(np.uint8),'L').save(OUT+'panels.png',optimize=True)
json.dump(dict(W=W,H=H,horizon=(dy+470)/H*100,layers=layers),open(OUT+'layers.json','w'),indent=1)
for f in sorted(os.listdir(OUT)): print(f, os.path.getsize(OUT+f)//1024,'KB')
