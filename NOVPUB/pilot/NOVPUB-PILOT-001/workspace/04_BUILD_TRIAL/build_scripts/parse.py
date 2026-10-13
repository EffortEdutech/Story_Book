import sys,glob,json,re,docx,os
from docx.enum.text import WD_ALIGN_PARAGRAPH as A
src=sys.argv[1]
files=sorted(glob.glob(src+'/*.docx'))
out=[]
for f in files:
    d=docx.Document(f); items=[]
    for p in d.paragraphs:
        t=p.text.strip()
        if not t: continue
        st=p.style.name
        center=p.alignment==A.CENTER
        bold=all(r.bold for r in p.runs if r.text.strip()) and any(r.text.strip() for r in p.runs)
        ital=all(r.italic for r in p.runs if r.text.strip())
        items.append(dict(style=st,text=t,center=center,bold=bold,ital=ital))
    out.append(dict(file=os.path.basename(f),items=items))
json.dump(out,open('chapters.json','w'),ensure_ascii=False,indent=1)
for c in out[:3]+out[-2:]:
    print(c['file'],len(c['items']));
    for i in c['items'][:5]+c['items'][-3:]: print('  ',i['style'],i['center'],i['bold'],i['ital'],i['text'][:60])
