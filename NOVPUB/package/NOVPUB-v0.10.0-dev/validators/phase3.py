import hashlib, json, re, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    from pypdf import PdfReader
except Exception:  # optional runtime dependency
    PdfReader = None


def _load(value):
    if isinstance(value, (str, Path)):
        return json.loads(Path(value).read_text(encoding='utf-8'))
    return value


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def validate_book_model(model):
    d=_load(model); errors=[]
    if not d.get('book_id') or not d.get('title'): errors.append('PROD-001 canonical book identity incomplete')
    sections=d.get('sections',[])
    if not sections: errors.append('PROD-002 canonical book has no sections')
    ids=[x.get('section_id') for x in sections]; seq=[x.get('sequence') for x in sections]
    if len(ids)!=len(set(ids)): errors.append('PROD-003 duplicate section_id')
    if seq and seq != sorted(seq): errors.append('PROD-004 section sequence not ordered')
    if not re.fullmatch(r'[a-fA-F0-9]{64}', d.get('source_hash','')): errors.append('PROD-005 source hash missing/invalid')
    return errors


def validate_production_source_manifest(manifest):
    d=_load(manifest); errors=[]
    for key in ('editorial_source_hash','canonical_text_hash'):
        if not re.fullmatch(r'[a-fA-F0-9]{64}', d.get(key,'')): errors.append(f'PROD-006 invalid {key}')
    if not d.get('source_freeze_id'): errors.append('PROD-007 source freeze ID missing')
    return errors


def validate_format_strategy(strategy, edition_manifest=None):
    d=_load(strategy); errors=[]
    if not d.get('editions'): errors.append('FMT-001 no production editions selected')
    if not d.get('approved'): errors.append('FMT-002 format strategy not human-approved')
    if edition_manifest is not None:
        e=_load(edition_manifest); allowed={x.get('edition_id') for x in e.get('editions',[])}
        for item in d.get('editions',[]):
            if item.get('edition_id') not in allowed: errors.append(f'FMT-003 production edition absent from Phase 2: {item.get("edition_id")}')
    return errors


def validate_trim_profile(profile, required_channels=None):
    d=_load(profile); errors=[]
    if d.get('width_in',0)<=0 or d.get('height_in',0)<=0: errors.append('TRIM-001 invalid trim dimensions')
    if d.get('estimated_pages',0)<1: errors.append('TRIM-002 invalid page estimate')
    if not d.get('approved'): errors.append('TRIM-003 trim not approved')
    supported=set(d.get('channels_supported',[]))
    for ch in required_channels or []:
        if ch not in supported: errors.append(f'TRIM-004 required channel unsupported: {ch}')
    return errors


def validate_font_register(register, required_usage=('print','ebook')):
    d=_load(register); errors=[]
    fonts=d.get('fonts',[])
    if not fonts: return ['FONT-001 no fonts registered']
    ids=[f.get('font_id') for f in fonts]
    if len(ids)!=len(set(ids)): errors.append('FONT-002 duplicate font_id')
    for f in fonts:
        fid=f.get('font_id','UNKNOWN')
        if f.get('license_status')!='verified': errors.append(f'FONT-003 font licence not verified: {fid}')
        if not f.get('embedding_allowed'): errors.append(f'FONT-004 embedding not allowed: {fid}')
        if 'print' in required_usage and not f.get('print_allowed'): errors.append(f'FONT-005 print use not allowed: {fid}')
        if 'ebook' in required_usage and not f.get('ebook_allowed'): errors.append(f'FONT-006 ebook use not allowed: {fid}')
    return errors


def validate_typography(spec, font_register):
    s=_load(spec); f=_load(font_register); errors=[]
    font_ids={x.get('font_id') for x in f.get('fonts',[])}
    if s.get('body_font_id') not in font_ids: errors.append('TYPE-001 body font not registered')
    if s.get('chapter_title_font_id') and s.get('chapter_title_font_id') not in font_ids: errors.append('TYPE-002 chapter-title font not registered')
    if s.get('body_size_pt',0)<7: errors.append('TYPE-003 body font below production minimum')
    if s.get('leading_pt',0)<=s.get('body_size_pt',0): errors.append('TYPE-004 leading must exceed body size')
    if not s.get('approved'): errors.append('TYPE-005 typography not approved')
    return errors


def validate_page_architecture(arch):
    d=_load(arch); errors=[]
    if not d.get('chapter_start'): errors.append('PAGE-001 chapter start rule missing')
    if not d.get('folios'): errors.append('PAGE-002 folio rules missing')
    if not isinstance(d.get('front_matter'),list) or not isinstance(d.get('back_matter'),list): errors.append('PAGE-003 matter map invalid')
    if not d.get('approved'): errors.append('PAGE-004 page architecture not approved')
    for i,b in enumerate(d.get('blank_page_rules',[])):
        if not b.get('reason'): errors.append(f'PAGE-005 blank-page rule without reason: {i}')
    return errors


def normalize_literary_text(text):
    text=text.replace('\u00ad','').replace('\u00a0',' ')
    return re.sub(r'\s+',' ',text).strip()


def validate_text_integrity(approved_text, canonical_text):
    a=Path(approved_text).read_text(encoding='utf-8') if isinstance(approved_text,(str,Path)) and Path(approved_text).exists() else str(approved_text)
    c=Path(canonical_text).read_text(encoding='utf-8') if isinstance(canonical_text,(str,Path)) and Path(canonical_text).exists() else str(canonical_text)
    return [] if normalize_literary_text(a)==normalize_literary_text(c) else ['TEXT-001 canonical literary text differs from approved source']


def _obj(x):
    try: return x.get_object()
    except Exception: return x


def _font_embedded(font_obj):
    f=_obj(font_obj)
    desc=_obj(f.get('/FontDescriptor')) if hasattr(f,'get') else None
    if desc and any(k in desc for k in ['/FontFile','/FontFile2','/FontFile3']): return True
    # Type0 fonts point to descendant fonts
    descendants=f.get('/DescendantFonts') if hasattr(f,'get') else None
    if descendants:
        for item in descendants:
            df=_obj(item); ddesc=_obj(df.get('/FontDescriptor')) if hasattr(df,'get') else None
            if ddesc and any(k in ddesc for k in ['/FontFile','/FontFile2','/FontFile3']): return True
    # Standard base14 fonts need not embed, but NOVPUB flags them as warning rather than hard false here.
    base=str(f.get('/BaseFont','')) if hasattr(f,'get') else ''
    return base.lstrip('/') in {'Courier','Courier-Bold','Courier-Oblique','Courier-BoldOblique','Helvetica','Helvetica-Bold','Helvetica-Oblique','Helvetica-BoldOblique','Times-Roman','Times-Bold','Times-Italic','Times-BoldItalic','Symbol','ZapfDingbats'}


def preflight_pdf(path, expected_width_in=None, expected_height_in=None, expected_page_count=None, require_embedded_fonts=True, tolerance_pt=1.0):
    p=Path(path); errors=[]; warnings=[]
    result={'profile':'NOVPUB_PRINT_MASTER','file_hash':sha256_file(p),'page_count':0,'errors':errors,'warnings':warnings,'passed':False}
    if PdfReader is None:
        errors.append('PDF-001 pypdf unavailable'); return result
    try: reader=PdfReader(str(p))
    except Exception as exc:
        errors.append(f'PDF-001 cannot parse PDF: {exc}'); return result
    if reader.is_encrypted: errors.append('PDF-011 encrypted PDF')
    pages=reader.pages; result['page_count']=len(pages)
    if expected_page_count is not None and len(pages)!=expected_page_count: errors.append(f'PDF-013 page count mismatch: {len(pages)} != {expected_page_count}')
    expected_w=expected_width_in*72 if expected_width_in else None; expected_h=expected_height_in*72 if expected_height_in else None
    dims=[]; nonembedded=set()
    for idx,page in enumerate(pages,1):
        box=page.mediabox; w=float(box.width); h=float(box.height); dims.append((round(w,3),round(h,3)))
        if expected_w and abs(w-expected_w)>tolerance_pt: errors.append(f'PDF-002 page {idx} width mismatch')
        if expected_h and abs(h-expected_h)>tolerance_pt: errors.append(f'PDF-002 page {idx} height mismatch')
        if page.get('/Annots'): errors.append(f'PDF-010 annotation detected on page {idx}')
        if require_embedded_fonts:
            res=_obj(page.get('/Resources')) if page.get('/Resources') else None
            fonts=_obj(res.get('/Font')) if res and hasattr(res,'get') and res.get('/Font') else None
            if fonts:
                for name,fo in fonts.items():
                    if not _font_embedded(fo): nonembedded.add(str(name))
    if len(set(dims))>1: errors.append('PDF-003 inconsistent page dimensions')
    if nonembedded: errors.append('PDF-004 non-embedded fonts detected: '+','.join(sorted(nonembedded)))
    result['passed']=not errors
    return result


def validate_pdf_preflight_report(report):
    d=_load(report); errors=[]
    if d.get('errors'): errors.extend(d['errors'])
    if not d.get('passed'): errors.append('PDF-000 preflight report not passed')
    return errors


def validate_epub_file(path):
    p=Path(path); errors=[]; warnings=[]
    result={'file_hash':sha256_file(p),'validator':'NOVPUB basic EPUB3 structural validator','errors':errors,'warnings':warnings,'reading_qa':'PENDING','passed':False}
    try:
        with zipfile.ZipFile(p) as z:
            names=z.namelist()
            if not names or names[0] != 'mimetype': warnings.append('EPUB-013 mimetype is not first ZIP entry')
            if 'mimetype' not in names or z.read('mimetype') != b'application/epub+zip': errors.append('EPUB-001 invalid/missing mimetype')
            if 'META-INF/container.xml' not in names: errors.append('EPUB-001 missing container.xml'); result['passed']=False; return result
            cont=ET.fromstring(z.read('META-INF/container.xml'))
            rootfile=None
            for el in cont.iter():
                if el.tag.endswith('rootfile'): rootfile=el.attrib.get('full-path'); break
            if not rootfile or rootfile not in names: errors.append('EPUB-001 package document missing'); result['passed']=False; return result
            opf=ET.fromstring(z.read(rootfile)); base=str(Path(rootfile).parent)
            if base=='.': base=''
            def full(href): return str(Path(base)/href).replace('\\','/') if base else href
            manifest={}; nav_found=False
            for el in opf.iter():
                if el.tag.endswith('item'):
                    iid=el.attrib.get('id'); href=el.attrib.get('href'); props=el.attrib.get('properties','')
                    if iid in manifest: errors.append(f'EPUB-009 duplicate manifest id: {iid}')
                    manifest[iid]=href
                    if 'nav' in props: nav_found=True
                    if href and full(href) not in names: errors.append(f'EPUB-005 missing manifest asset: {href}')
            spine=[]
            for el in opf.iter():
                if el.tag.endswith('itemref'):
                    rid=el.attrib.get('idref'); spine.append(rid)
                    if rid not in manifest: errors.append(f'EPUB-003 spine item missing from manifest: {rid}')
            if not spine: errors.append('EPUB-003 empty spine')
            if not nav_found: errors.append('EPUB-002 navigation document not declared')
            text=' '.join((el.text or '').strip() for el in opf.iter() if el.text)
            if not text.strip(): warnings.append('EPUB-007 package metadata may be incomplete')
    except zipfile.BadZipFile: errors.append('EPUB-001 invalid ZIP container')
    except ET.ParseError as exc: errors.append(f'EPUB-001 invalid XML: {exc}')
    result['passed']=not errors
    return result


def validate_cover_spec(spec, pagination, edition=None):
    s=_load(spec); p=_load(pagination); errors=[]
    if s.get('pagination_lock_id') != p.get('lock_id'): errors.append('COV-006 cover based on wrong pagination lock')
    if s.get('page_count') != p.get('page_count'): errors.append('COV-006 page-count/template mismatch')
    if abs(float(s.get('trim_width_in',0))-float(p.get('trim_width_in',0)))>1e-6 or abs(float(s.get('trim_height_in',0))-float(p.get('trim_height_in',0)))>1e-6: errors.append('COV-005 trim/template mismatch')
    if not s.get('template_source') or not s.get('template_generated_at'): errors.append('COV-015 template provenance missing')
    if edition is not None:
        e=_load(edition)
        if s.get('edition_id') != e.get('edition_id'): errors.append('COV-005 edition/template mismatch')
        if e.get('isbn') and s.get('isbn') and re.sub(r'\D','',str(e.get('isbn'))) != re.sub(r'\D','',str(s.get('isbn'))): errors.append('COV-003 ISBN mismatch')
    return errors


def validate_cover_parity(cover_qa, expected):
    q=_load(cover_qa); e=_load(expected); errors=[]
    checks=q.get('identity_checks',{})
    for field,code in [('title','COV-001'),('author','COV-002'),('isbn','COV-003'),('publisher','COV-004')]:
        if field in e and checks.get(field) != e.get(field): errors.append(f'{code} {field} mismatch')
    if q.get('visual_qa')!='PASS': errors.append('COV-016 visual QA not passed')
    if q.get('errors'): errors.extend(q['errors'])
    return errors


def validate_proof_plan(plan):
    d=_load(plan); errors=[]
    if not d.get('proofs'): errors.append('PROOF-001 no proof plan registered')
    for p in d.get('proofs',[]):
        if p.get('proof_required') and p.get('proof_status')=='approved' and not p.get('human_approved'):
            errors.append(f'PROOF-002 approved without human approval: {p.get("edition_id")}')
    return errors


def validate_physical_proof(proof):
    d=_load(proof); errors=[]
    if d.get('proof_status')!='approved': errors.append('PROOF-003 physical proof not approved')
    if not d.get('received_at'): errors.append('PROOF-004 proof not recorded as received')
    if not d.get('inspected'): errors.append('PROOF-005 physical inspection missing')
    if not d.get('human_approved'): errors.append('PROOF-006 human physical-proof approval missing')
    for f in d.get('findings',[]):
        if f.get('severity')=='BLOCKING' and f.get('status')=='open': errors.append('PROOF-007 blocking proof finding unresolved')
    return errors


def validate_gate05(book_model, source_manifest, trim, typography, fonts, architecture, pdf_report, epub_report, human_approval=False):
    errors=[]
    errors += validate_book_model(book_model)
    errors += validate_production_source_manifest(source_manifest)
    errors += validate_trim_profile(trim)
    errors += validate_font_register(fonts)
    errors += validate_typography(typography,fonts)
    errors += validate_page_architecture(architecture)
    errors += validate_pdf_preflight_report(pdf_report)
    e=_load(epub_report)
    if e.get('errors') or not e.get('passed'): errors.append('G05 EPUB technical validation not passed')
    if e.get('reading_qa')!='PASS': errors.append('G05 EPUB reading QA not passed')
    if not human_approval: errors.append('G05 human interior approval missing')
    return errors


def validate_gate06(cover_spec, pagination, cover_qa, expected_identity, human_approval=False):
    errors=validate_cover_spec(cover_spec,pagination)+validate_cover_parity(cover_qa,expected_identity)
    if not human_approval: errors.append('G06 human cover approval missing')
    return errors
