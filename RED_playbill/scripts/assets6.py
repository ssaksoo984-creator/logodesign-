import cv2, numpy as np
B='/home/claude/build'; O=f'{B}/img6'
import os; os.makedirs(O,exist_ok=True)
rng=np.random.default_rng(7)
def grain(img,s,seed=1):
    r=np.random.default_rng(seed); n=r.normal(0,s,img.shape[:2]).astype(np.float32)
    n=cv2.GaussianBlur(n,(0,0),.7)*1.6
    return np.clip(img.astype(np.float32)+n[...,None],0,255).astype(np.uint8)
def crop(img,x0,y0,x1,y1,w,h):
    H,W=img.shape[:2]; c=img[int(y0*H):int(y1*H),int(x0*W):int(x1*W)]
    ch,cw=c.shape[:2]; s=max(w/cw,h/ch); c=cv2.resize(c,(round(cw*s)+1,round(ch*s)+1),interpolation=cv2.INTER_AREA if s<1 else cv2.INTER_CUBIC)
    y=(c.shape[0]-h)//2; x=(c.shape[1]-w)//2; return c[y:y+h,x:x+w]
def gray(img):
    g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY).astype(np.float32)/255; return g
def duo(g,dark,mid,light,knee=.62):
    d,m,l=[np.array(c[::-1],np.float32) for c in (dark,mid,light)]
    t=np.clip(g/knee,0,1)[...,None]; u=np.clip((g-knee)/(1-knee),0,1)[...,None]
    return ((d*(1-t)+m*t)*(1-u)+l*u).astype(np.uint8)
R=(200,25,30)
# studio strip (p3) 1.85 x 8.75in
st=cv2.imread(f'{B}/img4/studio_bw.jpg'); print('studio',st.shape)
s=crop(st,.36,.03,.66,.97,555,2625); g=gray(s); g=np.clip((g-.03)*1.25,0,1)**.85
cv2.imwrite(f'{O}/strip_studio.jpg',grain(duo(g,(14,3,4),(168,16,20),(238,72,48),knee=.55),9),[cv2.IMWRITE_JPEG_QUALITY,92])
# hands band (p2) 5.75 x 2.45in
ha=cv2.imread(f'{B}/img4/hands_bw.jpg'); print('hands',ha.shape)
h=crop(ha,0,.22,1,.86,1725,735); g=gray(h); g3=(np.clip((g-.02)*1.08,0,1)*255).astype(np.uint8)
cv2.imwrite(f'{O}/band_hands.jpg',grain(cv2.merge([g3,g3,g3]),8),[cv2.IMWRITE_JPEG_QUALITY,92])
# can (p10)
ca=cv2.imread(f'{B}/img4/can_red.jpg'); print('can',ca.shape)
cv2.imwrite(f'{O}/can.jpg',grain(crop(ca,.08,.1,.95,.98,660,840),6),[cv2.IMWRITE_JPEG_QUALITY,92])
# brush (back)
br=cv2.imread(f'{B}/img4/brush_red.jpg'); print('brush',br.shape, br[5:40,5:40].mean((0,1)), br[-40:-5,5:40].mean((0,1)))
def unpink(img,smin=.74):
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV).astype(np.float32); h,sa,v=hsv[...,0],hsv[...,1]/255,hsv[...,2]/255
    m=((h<14)|(h>166))&(sa<smin)&(sa>.18)&(v>.30)
    sa[m]=sa[m]+(smin-sa[m])*.92; v[m]=v[m]*(1-.10*(1-sa[m]))
    hsv[...,1]=np.clip(sa,0,1)*255; hsv[...,2]=np.clip(v,0,1)*255
    return cv2.cvtColor(hsv.astype(np.uint8),cv2.COLOR_HSV2BGR)
cv2.imwrite(f'{O}/brush.jpg',grain(unpink(crop(br,0,0,1,1,1725,2156)),5),[cv2.IMWRITE_JPEG_QUALITY,92])
cv2.imwrite(f'{O}/can.jpg',grain(crop(ca,.08,.1,.95,.98,660,840),6),[cv2.IMWRITE_JPEG_QUALITY,92])
# high-key grain: multiplies onto colour so it only darkens (no pink shift)
r=np.random.default_rng(23); gg=cv2.GaussianBlur(r.normal(0,1,(700,700)).astype(np.float32),(0,0),.7)
gg=np.clip(226+gg*34,186,255).astype(np.uint8)
cv2.imwrite(f'{O}/grain_soft.png',cv2.merge([gg,gg,gg]))
# paint fields with soft irregular edges
def field(name,w,h,col,feather=16,seed=3,rag=.035):
    r=np.random.default_rng(seed)
    lo=cv2.resize(r.normal(0,1,(h//90+2,w//90+2)).astype(np.float32),(w,h),interpolation=cv2.INTER_CUBIC)
    streak=cv2.GaussianBlur(r.normal(0,1,(h,w)).astype(np.float32),(0,0),sigmaX=60,sigmaY=1.2)
    fine=cv2.GaussianBlur(r.normal(0,1,(h,w)).astype(np.float32),(0,0),.8)
    v=1+lo*.035+streak*.16+fine*.012
    img=np.clip(np.array(col[::-1],np.float32)[None,None]*v[...,None],0,255).astype(np.uint8)
    m=np.zeros((h,w),np.float32); p=feather*2; m[p:h-p,p:w-p]=1
    e=cv2.resize(r.normal(0,1,(h//40+2,w//40+2)).astype(np.float32),(w,h),interpolation=cv2.INTER_CUBIC)
    m=cv2.GaussianBlur(m,(0,0),feather); a=np.clip((m+e*rag-.5)*3.2+.5,0,1); a=cv2.GaussianBlur(a,(0,0),2.5)
    cv2.imwrite(f'{O}/{name}.png',np.dstack([img,(a*255).astype(np.uint8)]))
field('field_red',1425,1065,R,seed=3); field('field_dark',1425,1065,(22,25,27),seed=5)
field('blk_red',1365,1035,R,feather=3,seed=8,rag=.012); field('blk_dark',1365,1035,(22,25,27),feather=3,seed=9,rag=.012)
# paper
h,w=2625,1725; r=np.random.default_rng(11)
lo=cv2.resize(r.normal(0,1,(30,20)).astype(np.float32),(w,h),interpolation=cv2.INTER_CUBIC)
fib=cv2.GaussianBlur(r.normal(0,1,(h,w)).astype(np.float32),(0,0),sigmaX=5,sigmaY=.9)+cv2.GaussianBlur(r.normal(0,1,(h,w)).astype(np.float32),(0,0),sigmaX=.9,sigmaY=5)
v=1+lo*.008+fib*.03
cv2.imwrite(f'{O}/paper.jpg',np.clip(np.array([231,235,236],np.float32)*v[...,None],0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,90])
# --- v9: red duotone band for p2 (matches p3 strip) + full-bleed paint bands without ragged edges
hb=crop(ha,0,.22,1,.86,1725,690); g=gray(hb); g=np.clip((g-.03)*1.2,0,1)**.85
cv2.imwrite(f'{O}/band_hands_red.jpg',grain(duo(g,(14,3,4),(168,16,20),(238,72,48),knee=.55),9),[cv2.IMWRITE_JPEG_QUALITY,92])
def paintband(name,w,h,col,seed,amt=.10):
    r=np.random.default_rng(seed)
    lo=cv2.resize(r.normal(0,1,(h//110+2,w//110+2)).astype(np.float32),(w,h),interpolation=cv2.INTER_CUBIC)
    st=cv2.GaussianBlur(r.normal(0,1,(h,w)).astype(np.float32),(0,0),sigmaX=70,sigmaY=1.3)
    v=np.minimum(1+lo*.03+st*amt,1.03)
    cv2.imwrite(f'{O}/{name}.jpg',np.clip(np.array(col[::-1],np.float32)[None,None]*v[...,None],0,255).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,92])
paintband('paint_red',1725,1290,R,31); paintband('paint_dark',1725,1290,(22,25,27),32,.05)
# --- v10: rehearsal placeholders (red duotone)
def red_duo(img,x0,y0,x1,y1,w,h,seed):
    g=gray(crop(img,x0,y0,x1,y1,w,h)); g=np.clip((g-.03)*1.2,0,1)**.85
    return grain(duo(g,(14,3,4),(168,16,20),(238,72,48),knee=.55),9,seed)
cv2.imwrite(f'{O}/reh_a.jpg',red_duo(st,0,.18,1,.78,1725,1380,1),[cv2.IMWRITE_JPEG_QUALITY,92])
cv2.imwrite(f'{O}/reh_b.jpg',red_duo(ha,.35,.05,.85,.95,690,760,2),[cv2.IMWRITE_JPEG_QUALITY,92])
cv2.imwrite(f'{O}/reh_c.jpg',red_duo(st,.02,.5,.4,.95,690,760,3),[cv2.IMWRITE_JPEG_QUALITY,92])
