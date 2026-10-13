import zipfile,uuid,html,os,sys
from model import *
L=load()
e=html.escape
UID="urn:uuid:"+str(uuid.uuid5(uuid.NAMESPACE_URL,"novpub:NOVPUB-PILOT-001:the-blue-silence:trial"))
CSS="""@namespace epub "http://www.idpf.org/2007/ops";
html{font-size:100%}
body{font-family:serif;line-height:1.45;margin:0;padding:0}
p{margin:0;text-indent:1.3em;text-align:justify;hyphens:auto;-webkit-hyphens:auto;orphans:2;widows:2}
p.first,p.noindent{text-indent:0}
h1,h2{font-weight:normal;margin:0;page-break-after:avoid;break-after:avoid}
.chap{page-break-before:always;break-before:page;text-align:center;margin:18% 0 2.2em 0}
h1.num{font-size:.85em;letter-spacing:.25em;text-transform:uppercase;margin-bottom:.6em}
h2.ttl{font-size:1.6em;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.7em;line-height:1.2}
p.loc{text-align:center;text-indent:0;font-style:italic;margin-bottom:0}
p.scene{text-align:center;text-indent:0;margin:1.2em 0;letter-spacing:.4em}
p.insert{text-align:center;text-indent:0;font-weight:bold;font-size:.88em;letter-spacing:.06em;margin:.5em 0}
p.insert.gap{margin-top:1.4em}
p.end{text-align:center;text-indent:0;margin-top:3em;letter-spacing:.2em;font-size:.85em}
.half{text-align:center;margin-top:30%}
.half h1{font-size:2em;letter-spacing:.1em;text-transform:uppercase}
.title{text-align:center;margin-top:22%}
.title h1{font-size:2.3em;letter-spacing:.12em;text-transform:uppercase;margin-bottom:1.4em}
.title p.sub{font-style:italic;text-transform:none;letter-spacing:.05em;margin-bottom:3em}
.title p{text-align:center;text-indent:0;letter-spacing:.2em;text-transform:uppercase;font-size:.95em}
.copy p{text-indent:0;text-align:left;font-size:.8em;margin:0 0 .8em 0;line-height:1.35}
.copy p.trial{text-align:center;font-weight:bold;margin-top:2em}
.toc h1{text-align:center;font-size:1.2em;letter-spacing:.2em;text-transform:uppercase;margin:12% 0 1.5em}
nav ol{list-style:none;padding:0;margin:0}
nav li{margin:.35em 0;text-indent:0}
nav a{text-decoration:none;color:inherit}
"""
def xhtml(title,body,cls=""):
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">
<head><meta charset="utf-8"/><title>{e(title)}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body{(' class="'+cls+'"') if cls else ''}>
{body}
</body></html>'''
def label(c):
    return c['num'].title()
files=[]  # (id,href,title,xhtml)
files.append(("half","half.xhtml",TITLE,xhtml(TITLE,f'<section epub:type="halftitlepage" class="half"><h1>{e(TITLE)}</h1></section>')))
files.append(("title","title.xhtml",TITLE,xhtml(TITLE,f'<section epub:type="titlepage" class="title"><h1>{e(TITLE)}</h1><p class="sub">A Novel</p><p>{e(AUTHOR)}</p></section>')))
cp="".join(f"<p>{e(x)}</p>" for x in COPY_LINES)+f'<p class="trial">{e(TRIAL)}</p>'
files.append(("copy","copyright.xhtml","Copyright",xhtml("Copyright",f'<section epub:type="copyright-page" class="copy">{cp}</section>')))
for i,c in enumerate(L):
    nm=f"ch{i:02d}"
    isp=c['num']=='PROLOGUE'
    h=f'<section epub:type="{"prologue" if isp else "chapter"}" id="{nm}"><div class="chap"><h1 class="num">{e(c["num"].title() if not isp else "Prologue")}</h1><h2 class="ttl">{e(c["title"])}</h2><p class="loc">{e(c["loc"])}</p></div>'
    first=True; prev=None
    for k,t in c['blocks']:
        if k=='p':
            h+=f'<p class="{"first" if first else ""}">{e(t)}</p>'.replace(' class=""',''); first=False
        elif k=='scene': h+='<p class="scene">* * *</p>'; first=True
        elif k=='insert':
            h+=f'<p class="insert{" gap" if prev!="insert" else ""}">{e(t)}</p>'; first=True
        elif k=='end': h+=f'<p class="end">{e(t)}</p>'
        prev=k
    h+='</section>'
    files.append((nm,f"{nm}.xhtml",(c['title'].title() if isp else f"{label(c)}: {c['title'].title()}"),xhtml(c['title'].title(),h)))
# nav
nav_items="".join(f'<li><a href="{f[1]}">{e(f[2])}</a></li>' for f in files[3:])
nav=xhtml("Contents",f'<nav epub:type="toc" id="toc" class="toc"><h1>Contents</h1><ol>{nav_items}</ol></nav>'
 f'<nav epub:type="landmarks" hidden="hidden"><ol><li><a epub:type="titlepage" href="title.xhtml">Title Page</a></li><li><a epub:type="bodymatter" href="ch00.xhtml">Start of Content</a></li></ol></nav>')
ids=[f[0] for f in files]
manifest="".join(f'<item id="{f[0]}" href="{f[1]}" media-type="application/xhtml+xml"/>' for f in files)
spine="".join(f'<itemref idref="{i}"/>' for i in ids[:3])+'<itemref idref="navdoc"/>'+"".join(f'<itemref idref="{i}"/>' for i in ids[3:])
opf=f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="en">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">{UID}</dc:identifier>
<dc:title>{e(TITLE)}</dc:title>
<dc:creator id="creator">{e(AUTHOR)}</dc:creator>
<dc:language>en</dc:language>
<dc:publisher>{e(AUTHOR)}</dc:publisher>
<dc:rights>Copyright © 2026 Darya Malak. All rights reserved.</dc:rights>
<dc:description>TRIAL BUILD (NOVPUB-PILOT-001). A Malaysian crime thriller about police corruption and an internal affairs investigation.</dc:description>
<dc:subject>Fiction / Thrillers / Crime</dc:subject>
<meta property="dcterms:modified">2026-10-13T00:00:00Z</meta>
<meta property="schema:accessMode">textual</meta>
<meta property="schema:accessibilityFeature">structuralNavigation</meta>
<meta property="schema:accessibilityHazard">none</meta>
<meta property="schema:accessibilitySummary">Reflowable text with a navigable table of contents. No images.</meta>
</metadata>
<manifest>
<item id="navdoc" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
<item id="css" href="style.css" media-type="text/css"/>
<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
{manifest}
</manifest>
<spine toc="ncx">{spine}</spine>
</package>'''
ncx_pts="".join(f'<navPoint id="n{i}" playOrder="{i+1}"><navLabel><text>{e(f[2])}</text></navLabel><content src="{f[1]}"/></navPoint>' for i,f in enumerate(files[3:]))
ncx=f'''<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head><meta name="dtb:uid" content="{UID}"/><meta name="dtb:depth" content="1"/><meta name="dtb:totalPageCount" content="0"/><meta name="dtb:maxPageNumber" content="0"/></head>
<docTitle><text>{e(TITLE)}</text></docTitle><navMap>{ncx_pts}</navMap></ncx>'''
out=sys.argv[1]
if os.path.exists(out): os.remove(out)
z=zipfile.ZipFile(out,'w')
z.writestr(zipfile.ZipInfo('mimetype',(2026,10,13,0,0,0)),'application/epub+zip',zipfile.ZIP_STORED)
def w(n,s):
    zi=zipfile.ZipInfo(n,(2026,10,13,0,0,0)); zi.compress_type=zipfile.ZIP_DEFLATED; z.writestr(zi,s)
w('META-INF/container.xml','<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
w('OEBPS/content.opf',opf); w('OEBPS/nav.xhtml',nav); w('OEBPS/toc.ncx',ncx); w('OEBPS/style.css',CSS)
for f in files: w('OEBPS/'+f[1],f[3])
z.close(); print(out,os.path.getsize(out))
