import sys
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER,TA_LEFT
from reportlab.platypus import NextPageTemplate,BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,PageBreak,Flowable,KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from xml.sax.saxutils import escape as e
from model import *
D='/usr/share/fonts/truetype/crosextra/Caladea-'
for n,f in [('Cal','Regular'),('Cal-I','Italic'),('Cal-B','Bold'),('Cal-BI','BoldItalic')]:
    pdfmetrics.registerFont(TTFont(n,D+f+'.ttf'))
addMapping('Cal',0,0,'Cal');addMapping('Cal',1,0,'Cal-B');addMapping('Cal',0,1,'Cal-I');addMapping('Cal',1,1,'Cal-BI')
from reportlab import rl_config
rl_config.canvas_basefontname='Cal'
W,H=5.5*inch,8.5*inch
IN,OUT,TOP,BOT=0.8*inch,0.55*inch,0.65*inch,0.75*inch
L=load()
FS,LD=10,13.5
def st(name,**k):
    base=dict(fontName='Cal',fontSize=FS,leading=LD,alignment=TA_JUSTIFY,hyphenationLang='en_GB',embeddedHyphenation=1,allowWidows=0,allowOrphans=0,splitLongWords=1)
    base.update(k); return ParagraphStyle(name,**base)
S_P=st('p',firstLineIndent=14)
S_F=st('f',firstLineIndent=0)
S_SC=st('sc',alignment=TA_CENTER,spaceBefore=11,spaceAfter=11,hyphenationLang=None,leading=LD)
S_INS=st('ins',alignment=TA_CENTER,fontName='Cal-B',fontSize=9,leading=12.5,hyphenationLang=None,spaceBefore=3,spaceAfter=3)
S_END=st('end',alignment=TA_CENTER,fontSize=9,spaceBefore=30,hyphenationLang=None)
S_NUM=st('num',alignment=TA_CENTER,fontSize=9.5,leading=13,hyphenationLang=None)
S_TTL=st('ttl',alignment=TA_CENTER,fontName='Cal-B',fontSize=17,leading=21,spaceBefore=8,hyphenationLang=None)
S_LOC=st('loc',alignment=TA_CENTER,fontName='Cal-I',fontSize=10,spaceBefore=10,spaceAfter=22,hyphenationLang=None)
class Spaced(Paragraph):
    pass
def sp(t,n): return ''.join(c+('<font size="1"> </font>' if False else '') for c in t)
class OddFill(Flowable):
    """If next page would be even (verso), emit a blank page. Placed after PageBreak."""
    def wrap(self,aW,aH):
        self.aH=aH
        pg=self.canv.getPageNumber()
        if pg%2==0:
            self.canv._doctemplate._blank.add(pg); return (aW,aH-2)
        return (0,0)
    def draw(self): pass
class ChapHead(Flowable):
    def __init__(self,key,num,title,loc):
        super().__init__(); self.key=key; self.p=[Paragraph(num,S_NUM),Paragraph(title,S_TTL),Paragraph(loc,S_LOC)]
    def wrap(self,aW,aH):
        d=self.canv._doctemplate; d._chap.add(self.canv.getPageNumber()); d._pos[self.key]=self.canv.getPageNumber()
        self.hs=[]; tot=0.9*inch
        for p in self.p:
            w,h=p.wrap(aW,aH); self.hs.append(h); tot+=h+p.getSpaceBefore()+p.getSpaceAfter()
        self.w=aW; self.h=tot; return (aW,tot)
    def draw(self):
        y=self.h-0.9*inch
        for p,h in zip(self.p,self.hs):
            y-=p.getSpaceBefore(); y-=h; p.drawOn(self.canv,0,y); y-=p.getSpaceAfter()
class TocLine(Flowable):
    def __init__(self,lab,t2,key,pos,off): super().__init__(); self.lab=lab;self.t2=t2;self.key=key;self.pos=pos;self.off=off
    def wrap(self,aW,aH): self.w=aW; return (aW,15.5)
    def draw(self):
        c=self.canv; c.setFont('Cal',9.8)
        pg=self.pos.get(self.key); pg=str(pg-self.off) if pg else '0'
        tw=1.5*inch+c.stringWidth(self.t2,'Cal',9.8); pw=c.stringWidth(pg,'Cal',9.8)
        c.drawString(0,3,self.lab); c.drawString(1.5*inch,3,self.t2); c.drawRightString(self.w,3,pg)
        dot=c.stringWidth(' .','Cal',9.8); x=tw+6; end=self.w-pw-6
        n=int((end-x)//dot)
        if n>0: c.drawString(end-n*dot,3,' .'*n)
class Doc(BaseDocTemplate):
    def __init__(self,fn,off,pos_prev):
        super().__init__(fn,pagesize=(W,H),title=TITLE+" (TRIAL BUILD)",author=AUTHOR,subject="NOVPUB-PILOT-001 trial interior",creator="NOVPUB trial build")
        self._blank=set(); self._chap=set(); self._pos={}; self.off=off; self.prev=pos_prev
        self.fm=set()
        fr_r=Frame(IN,BOT,W-IN-OUT,H-TOP-BOT,id='r',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        fr_l=Frame(OUT,BOT,W-IN-OUT,H-TOP-BOT,id='l',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        self.addPageTemplates([PageTemplate(id='R',frames=[fr_r],onPageEnd=self.deco),PageTemplate(id='L',frames=[fr_l],onPageEnd=self.deco)])
        self._fr_r,self._fr_l=fr_r,fr_l
    def deco(self,canv,doc):
        pg=canv.getPageNumber()
        if pg in self._blank: return
        if self.off and pg>self.off:
            n=pg-self.off
            canv.setFont('Cal',9)
            if pg in self._chap:
                canv.drawCentredString(((IN-OUT)/2+ (W/2) ) if pg%2==1 else (W/2-(IN-OUT)/2), BOT-26, str(n))
            else:
                cx=(W+(IN-OUT))/2 if pg%2==1 else (W-(IN-OUT))/2
                canv.drawCentredString(cx,BOT-26,str(n))
                canv.setFont('Cal-I',8.5)
                canv.drawCentredString(cx,H-TOP+14,(TITLE if pg%2==1 else AUTHOR).upper() if False else (TITLE if pg%2==1 else AUTHOR))
def story(pos,off):
    s=[NextPageTemplate(['L','R'])]
    # half title (recto p1)
    s+= [Spacer(1,1.9*inch),Paragraph(TITLE.upper(),st('ht',alignment=TA_CENTER,fontSize=15,leading=20,hyphenationLang=None)),PageBreak(),
         Spacer(1,0.1*inch),PageBreak()]   # p2 blank verso
    s+= [Spacer(1,1.6*inch),Paragraph(TITLE.upper(),st('tt',alignment=TA_CENTER,fontName='Cal-B',fontSize=26,leading=32,hyphenationLang=None)),
         Spacer(1,0.2*inch),Paragraph('A Novel',st('sub',alignment=TA_CENTER,fontName='Cal-I',fontSize=12,leading=16,hyphenationLang=None)),Spacer(1,0.6*inch),
         Paragraph(AUTHOR.upper(),st('au',alignment=TA_CENTER,fontSize=12,leading=16,hyphenationLang=None)),PageBreak()]
    cs=st('cp',alignment=TA_LEFT,fontSize=8.6,leading=11.8,spaceAfter=7,hyphenationLang=None)
    s+= [Spacer(1,3.3*inch)]+[Paragraph(e(x),cs) for x in COPY_LINES]+[Spacer(1,10),Paragraph('<b>'+e(TRIAL)+'</b>',st('tr',alignment=TA_CENTER,fontSize=8,leading=11,hyphenationLang=None)),PageBreak(),OddFill()]
    s+= [Paragraph('CONTENTS',st('ch',alignment=TA_CENTER,fontSize=11,leading=15,spaceAfter=16,hyphenationLang=None))]
    for i,c in enumerate(L):
        lab='Prologue' if c['num']=='PROLOGUE' else c['num'].title()
        t=(c['title'].title().replace('’S','’s') )
        s.append(TocLine(lab,t,i,pos,off))
    s+= [PageBreak(),OddFill()]
    for i,c in enumerate(L):
        isp=c['num']=='PROLOGUE'
        s.append(ChapHead(i,'PROLOGUE' if isp else c['num'],e(c['title']),e(c['loc'])))
        first=True; prev=None
        for k,t in c['blocks']:
            if k=='p': s.append(Paragraph(e(t),S_F if first else S_P)); first=False
            elif k=='scene': s.append(Paragraph('*&nbsp;&nbsp;*&nbsp;&nbsp;*',S_SC)); first=True
            elif k=='insert':
                if prev!='insert': s.append(Spacer(1,6))
                s.append(Paragraph(e(t),S_INS)); first=True
            elif k=='end': s.append(Paragraph(e(t),S_END))
            prev=k
        if i<len(L)-1: s+=[PageBreak(),OddFill()]
    return s
out=sys.argv[1]
d1=Doc('/dev/null',0,{}); d1.build(story({},0))
pos=dict(d1._pos); off=pos[0]-1
d2=Doc(out,off,pos); d2.build(story(pos,off))
assert d2._pos==pos or True
print('pages',d2.page,'body offset',off,'prologue page',pos[0],'ch1',pos[1]-off)
if d2._pos!=pos: print('POS CHANGED',{k:(pos[k],d2._pos[k]) for k in pos if pos[k]!=d2._pos[k]})

from pypdf import PdfReader,PdfWriter
r=PdfReader(out); w=PdfWriter(); [w.add_page(p) for p in r.pages]
if len(r.pages)%2: w.add_blank_page(width=W,height=H)
w.add_metadata({'/Title':TITLE+' (TRIAL BUILD)','/Author':AUTHOR,'/Subject':'NOVPUB-PILOT-001 trial interior, 5.5x8.5in'})
w.write(out); print('final pages',len(w.pages))
