import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
SRC='/mnt/user-data/uploads/01_The_Blue_Silence/Publish/CoverFront_v3.jpg'
TITLE=['THE BLUE','SILENCE']; AUTHOR='DARYA MALAK'
TAG1='Everyone knows the police protect the law.'; TAG2='Nobody asks who protects the police from themselves.'
BLURB=["For thirty-five years, Dato’ Rahman Aziz has believed that criminals are the enemy and that an honest man is enough to make the truth win.",
"Then Task Force ORION starts to fail. Raids find empty warehouses with the food still warm. Evidence thins. Witnesses disappear. Someone always knows what the police are about to do.",
"Inspector Nur Aisyah Othman of Internal Integrity has been sent to find the leak. Her orders point at the task force’s own commander.",
"The Circle has no leader and no membership list. It runs on favours, information and fear, and the harder Rahman looks, the more of it he finds inside the institution he gave his life to."]
SANS='/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'
SANSR='/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf'
SERIF='/usr/share/fonts/truetype/crosextra/Caladea-Regular.ttf'; SERIFI='/usr/share/fonts/truetype/crosextra/Caladea-Italic.ttf'
ICE=(232,241,248)
src=Image.open(SRC).convert('RGB')
def cover_art(w,h):
    """crop src to w:h ratio (centered) then upscale"""
    sw,sh=src.size; r=w/h
    if sw/sh>r: cw=int(round(sh*r)); x=(sw-cw)//2; box=(x,0,x+cw,sh)
    else: ch=int(round(sw/r)); y=(sh-ch)//2; box=(0,y,sw,y+ch)
    im=src.crop(box).resize((w,h),Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2,percent=60,threshold=2))
    a=np.asarray(im).astype(np.float32); rng=np.random.default_rng(7)
    a+=rng.normal(0,3.2,a.shape[:2])[...,None]   # fine grain, masks upscale softness
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def grad(w,h,top=None,bottom=None):
    """RGBA overlay with dark vertical gradients: top=(alpha,fraction) bottom=(alpha,fraction)"""
    y=np.arange(h,dtype=np.float32)[:,None]*np.ones((1,w),np.float32); al=np.zeros((h,w),np.float32)
    if top: a0,f=top; al=np.maximum(al,a0*np.clip(1-y/(h*f),0,1)**1.4)
    if bottom: a0,f=bottom; al=np.maximum(al,a0*np.clip(1-(h-1-y)/(h*f),0,1)**1.4)
    o=np.zeros((h,w,4),np.uint8); o[...,:3]=(3,10,20); o[...,3]=(al*255).astype(np.uint8); return Image.fromarray(o,'RGBA')
def spaced(draw,text,font,x_center,y,fill,track=0,anchor_w=None):
    ws=[draw.textlength(c,font=font) for c in text]; tw=sum(ws)+track*(len(text)-1); x=x_center-tw/2
    for c,w in zip(text,ws): draw.text((x,y),c,font=font,fill=fill); x+=w+track
    return tw
def fit_font(path,text,maxw,track_ratio=0.06,start=600):
    s=start
    while s>10:
        f=ImageFont.truetype(path,s); d=ImageDraw.Draw(Image.new('L',(1,1)))
        tw=sum(d.textlength(c,font=f) for c in text)+s*track_ratio*(len(text)-1)
        if tw<=maxw: return f,s
        s-=4
    return ImageFont.truetype(path,10),10
def front_text(im,panel_x0,panel_w,H,top_pad):
    """draw title+author in a front panel region; coordinates relative to image"""
    cx=panel_x0+panel_w/2; d=ImageDraw.Draw(im)
    maxw=panel_w*0.78
    f,s=fit_font(SANS,'THE BLUE',maxw)
    f2,s2=fit_font(SANS,'SILENCE',maxw)
    s=min(s,s2); f=ImageFont.truetype(SANS,s)
    glow=Image.new('RGBA',im.size,(0,0,0,0)); gd=ImageDraw.Draw(glow)
    y=top_pad; lines=[]
    for t in TITLE:
        for dr in (gd,d):
            pass
        lines.append((t,y)); y+=int(s*1.12)
    for t,yy in lines: spaced(gd,t,f,cx,yy,(120,190,235,255),track=s*0.06)
    glow=glow.filter(ImageFilter.GaussianBlur(s*0.10)); im.paste(glow,(0,0),glow)
    for t,yy in lines: spaced(d,t,f,cx,yy,ICE+(255,) if im.mode=='RGBA' else ICE,track=s*0.06)
    fa=ImageFont.truetype(SANS,int(s*0.25)); ay=y+int(s*0.16)
    sh=Image.new('RGBA',im.size,(0,0,0,0)); sdd=ImageDraw.Draw(sh)
    spaced(sdd,AUTHOR,fa,cx,ay,(0,6,14,255),track=int(s*0.25)*0.40)
    sh=sh.filter(ImageFilter.GaussianBlur(s*0.05)); 
    for _ in range(3): im.alpha_composite(sh) if im.mode=='RGBA' else im.paste(sh,(0,0),sh)
    spaced(d,AUTHOR,fa,cx,ay,ICE,track=int(s*0.25)*0.40)
    return ay+int(s*0.25)
def wrap(draw,text,font,maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if draw.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
# ---------- EBOOK 1600x2560 ----------
EW,EH=1600,2560
eb=cover_art(EW,EH).convert('RGBA'); eb=Image.alpha_composite(eb,grad(EW,EH,top=(0.72,0.42),bottom=(0.35,0.2)))
front_text(eb,0,EW,EH,int(EH*0.075))
eb.convert('RGB').save('THE_BLUE_SILENCE_ebook_cover_1600x2560_TRIAL.jpg',quality=95,dpi=(300,300),subsampling=0)
# ---------- PRINT WRAP 12.785 x 8.75 in @300dpi ----------
D=300; BL=int(0.125*D); TW=int(5.5*D); TH=int(8.5*D); SP=int(round(1.535*D))
W=BL+TW+SP+TW+BL; H=BL+TH+BL
fx0=BL+TW+SP         # front panel starts at spine's right edge (incl. right bleed to end)
fw=W-fx0             # 5.625in
bx1=BL+TW            # back panel ends at spine left edge
wrap_img=Image.new('RGB',(W,H),(6,18,34))
front=cover_art(fw,H).convert('RGBA'); front=Image.alpha_composite(front,grad(fw,H,top=(0.72,0.42),bottom=(0.35,0.2)))
# back: mirrored art, darkened and blurred
bk=cover_art(bx1,H).transpose(Image.FLIP_LEFT_RIGHT).filter(ImageFilter.GaussianBlur(5)).convert('RGBA')
bk=Image.alpha_composite(bk,Image.new('RGBA',bk.size,(3,10,20,150)))
# spine: sample colours from edges of back/front for blend
sp=Image.new('RGBA',(SP,H),(5,15,30,255))
wrap_img.paste(bk.convert('RGB'),(0,0)); wrap_img.paste(sp.convert('RGB'),(bx1,0)); wrap_img.paste(front.convert('RGB'),(fx0,0))
# soften seams: gradient from spine into panels
seam=Image.new('RGBA',(W,H),(0,0,0,0)); sd=ImageDraw.Draw(seam)
wi=wrap_img.convert('RGBA'); d=ImageDraw.Draw(wi)
# front text (front panel trim area: from fx0 to W-BL ; centre on trim area)
trim_front_w=TW
front_text(wi,fx0,trim_front_w,H,BL+int(TH*0.075))
# spine text rotated 90deg clockwise (reads top-to-bottom)
st=Image.new('RGBA',(H,SP),(0,0,0,0)); sdr=ImageDraw.Draw(st)
fsp=ImageFont.truetype(SANS,int(SP*0.27)); fau=ImageFont.truetype(SANS,int(SP*0.15))
def _len(t,f,tr): return sum(sdr.textlength(c,font=f) for c in t)+tr*(len(t)-1)
trT=fsp.size*0.08; trA=fau.size*0.30
lt=_len('THE BLUE SILENCE',fsp,trT); la=_len(AUTHOR,fau,trA); mg=BL+int(0.5*D)
assert mg+lt+int(0.4*D)+la+mg<=H,(mg,lt,la,H)
spaced(sdr,'THE BLUE SILENCE',fsp,mg+lt/2,int(SP*0.36),ICE+(255,),track=trT)
spaced(sdr,AUTHOR,fau,H-mg-la/2,int(SP*0.42),ICE+(255,),track=trA)
st=st.rotate(-90,expand=True); wi.alpha_composite(st,(bx1,0))
d=ImageDraw.Draw(wi)
# back text
m=int(0.55*D); bw=bx1-BL-m-BL      # usable width inside trim with margin
bx=BL+m; by=BL+int(0.7*D)
ft=ImageFont.truetype(SERIFI,int(0.19*D)); 
y=by
for t in (TAG1,TAG2):
    for ln in wrap(d,t,ft,bw): d.text((bx,y),ln,font=ft,fill=ICE,); y+=int(ft.size*1.35)
y+=int(0.28*D); d.line((bx,y,bx+int(0.9*D),y),fill=(120,190,235),width=3); y+=int(0.32*D)
fb=ImageFont.truetype(SERIF,int(0.152*D))
for p in BLURB:
    for ln in wrap(d,p,fb,bw): d.text((bx,y),ln,font=fb,fill=(222,232,240)); y+=int(fb.size*1.42)
    y+=int(fb.size*0.7)
text_bottom=y
# barcode area 2 x 1.2 in white box, bottom-right of back, 0.25in+ from trim
bcw,bch=int(2.0*D),int(1.2*D); bcx=BL+TW-int(0.5*D)-bcw; bcy=BL+TH-int(0.55*D)-bch
d.rectangle((bcx,bcy,bcx+bcw,bcy+bch),fill=(255,255,255))
wi=wi.convert('RGB'); wi.save('THE_BLUE_SILENCE_print_wrap_12.785x8.75in_TRIAL.jpg',quality=95,dpi=(300,300),subsampling=0)
print('wrap',wi.size,'text_bottom_in',round((text_bottom-BL)/D,2),'barcode_top_in',round((bcy-BL)/D,2))
# guides version
g=wi.copy().convert('RGBA'); gd=ImageDraw.Draw(g)
def rect(x0,y0,x1,y1,c): gd.rectangle((x0,y0,x1,y1),outline=c,width=4)
rect(BL,BL,W-BL,H-BL,(255,60,60,255))                       # trim
rect(BL+int(.25*D),BL+int(.25*D),W-BL-int(.25*D),H-BL-int(.25*D),(60,255,120,255))   # safe
gd.line((bx1,0,bx1,H),fill=(255,220,0,255),width=4); gd.line((bx1+SP,0,bx1+SP,H),fill=(255,220,0,255),width=4)
g.convert('RGB').resize((W//3,H//3)).save('guides_preview.jpg',quality=85)
# PDF at exact size
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
c=canvas.Canvas('THE_BLUE_SILENCE_print_cover_wrap_TRIAL.pdf',pagesize=(12.785*72,8.75*72)); c.setTitle('The Blue Silence print cover wrap (TRIAL)')
c.drawImage('THE_BLUE_SILENCE_print_wrap_12.785x8.75in_TRIAL.jpg',0,0,12.785*72,8.75*72); c.save()
# front-only preview + thumbnail test
ebt=Image.open('THE_BLUE_SILENCE_ebook_cover_1600x2560_TRIAL.jpg'); t=ebt.copy(); t.thumbnail((900,1440)); t.save('eb_preview.png'); th=ebt.copy(); th.thumbnail((160,256)); th.save('eb_thumb.png')
wp=wi.copy(); wp.thumbnail((1700,1200)); wp.save('wrap_preview.png')
