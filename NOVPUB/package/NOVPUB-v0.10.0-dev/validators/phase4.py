import json, re
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
from datetime import date, datetime


def _load(value):
    if isinstance(value,(str,Path)):
        return json.loads(Path(value).read_text(encoding='utf-8'))
    return value


def D(value): return Decimal(str(value))
def money(value): return D(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def validate_metadata_master(master, identity=None, product=None):
    d=_load(master); errors=[]
    work=d.get('work',{}); contrib=d.get('contributors',{}); pub=d.get('publisher',{})
    if not work.get('title'): errors.append('META-001 title missing')
    if not work.get('language'): errors.append('META-001 language missing')
    if not contrib.get('primary_author'): errors.append('META-001 primary author missing')
    if not pub.get('publisher_name'): errors.append('META-001 publisher missing')
    if not d.get('editions'): errors.append('META-001 editions missing')
    if not d.get('provenance',{}).get('sources'): errors.append('META-006 provenance sources missing')
    if identity:
        i=_load(identity)
        if i.get('title') and work.get('title')!=i.get('title'): errors.append('META-002 title differs from Phase 2')
        if i.get('author') and contrib.get('primary_author')!=i.get('author'): errors.append('META-002 author differs from Phase 2')
        if i.get('publisher') and pub.get('publisher_name')!=i.get('publisher'): errors.append('META-002 publisher differs from Phase 2')
    if product:
        p=_load(product); byid={x.get('edition_id'):x for x in d.get('editions',[])}
        for e in p.get('editions',[]):
            m=byid.get(e.get('edition_id'))
            if not m: errors.append(f'META-003 production edition missing from metadata: {e.get("edition_id")}'); continue
            for field in ('format','page_count'):
                if field in e and field in m and e.get(field)!=m.get(field): errors.append(f'META-003 {field} differs from Phase 3 for {e.get("edition_id")}')
    return errors


def validate_metadata_manifest(manifest):
    d=_load(manifest); errors=[]; fields=d.get('fields',[])
    if not fields: return ['META-001 metadata manifest empty']
    seen=set()
    for f in fields:
        key=f.get('field')
        if not key: errors.append('META-001 unnamed metadata field'); continue
        if key in seen: errors.append(f'META-010 duplicate metadata manifest field: {key}')
        seen.add(key)
        if not f.get('source') or not f.get('authority'): errors.append(f'META-006 provenance missing: {key}')
        if f.get('approved') is not True: errors.append(f'META-009 field not approved: {key}')
    return errors


def validate_positioning(positioning):
    d=_load(positioning); errors=[]
    for k in ('genre','target_reader','core_promise'):
        if not d.get(k): errors.append(f'POS-001 {k} missing')
    if not d.get('manuscript_basis'): errors.append('POS-002 manuscript basis missing')
    if d.get('approved') is not True: errors.append('POS-003 positioning not human-approved')
    return errors


def validate_classification(strategy, kdp_category_limit=3, current_bisac=None, current_thema=None):
    d=_load(strategy); errors=[]
    bisac=d.get('bisac',[]); thema=d.get('thema',[]); cats=d.get('amazon_categories',[])
    if not bisac: errors.append('CLASS-001 primary BISAC missing')
    if len(cats)>kdp_category_limit: errors.append(f'CLASS-005 KDP categories exceed current limit {kdp_category_limit}')
    for x in bisac:
        if not x.get('basis'): errors.append(f'CLASS-002 BISAC unsupported by manuscript: {x.get("code")}')
        if x.get('approved') is not True: errors.append(f'CLASS-011 BISAC not approved: {x.get("code")}')
        if current_bisac is not None and x.get('code') not in current_bisac: errors.append(f'CLASS-010 stale/unknown BISAC: {x.get("code")}')
    for x in thema:
        if current_thema is not None and x.get('code') and x.get('code') not in current_thema: errors.append(f'CLASS-010 stale/unknown Thema: {x.get("code")}')
    for c in cats:
        if not c.get('basis'): errors.append(f'CLASS-002 Amazon category unsupported: {c.get("category")}')
        if c.get('approved') is not True: errors.append(f'CLASS-011 Amazon category not approved: {c.get("category")}')
    if d.get('approved') is not True: errors.append('CLASS-012 classification strategy not approved')
    return errors


PROHIBITED_KEYWORD_PATTERNS=[r'\bbestseller\b',r'\bbest seller\b',r'\bfree\b',r'\bkindle unlimited\b',r'\b5[- ]?star\b']
def validate_keywords(strategy, kdp_limit=7, competitor_names=None):
    d=_load(strategy); errors=[]; candidates=d.get('candidates',[]); cmap=d.get('channel_map',{})
    phrases=[str(x.get('phrase','')).strip() for x in candidates]
    normalized=[re.sub(r'\s+',' ',x.casefold()) for x in phrases if x]
    if len(normalized)!=len(set(normalized)): errors.append('KW-001 duplicate keyword phrase')
    competitors=[x.casefold() for x in (competitor_names or [])]
    for x in candidates:
        phrase=str(x.get('phrase',''))
        if not phrase: errors.append('KW-002 empty keyword'); continue
        if not x.get('manuscript_basis'): errors.append(f'KW-003 keyword lacks manuscript basis: {phrase}')
        if x.get('approved') is not True: errors.append(f'KW-004 keyword not approved: {phrase}')
        low=phrase.casefold()
        if any(re.search(p,low) for p in PROHIBITED_KEYWORD_PATTERNS): errors.append(f'KW-005 prohibited promotional keyword: {phrase}')
        if any(n in low for n in competitors): errors.append(f'KW-006 competitor name in keyword: {phrase}')
    kdp=cmap.get('kdp',[])
    if len(kdp)>kdp_limit: errors.append(f'KW-007 KDP keyword slots exceed current limit {kdp_limit}')
    if d.get('approved') is not True: errors.append('KW-008 keyword strategy not approved')
    return errors


def validate_descriptions(data, verified_claim_ids=None, allow_major_spoiler=False):
    d=_load(data); errors=[]; valid=set(verified_claim_ids or [])
    if not d.get('descriptions'): errors.append('DESC-001 no descriptions')
    for desc in d.get('descriptions',[]):
        did=desc.get('description_id','?')
        if not desc.get('text'): errors.append(f'DESC-001 empty description: {did}')
        if desc.get('approved') is not True: errors.append(f'DESC-008 unapproved copy: {did}')
        if desc.get('spoiler_level')=='major' and not allow_major_spoiler: errors.append(f'DESC-002 major spoiler: {did}')
        for claim in desc.get('claims',[]):
            if claim.get('requires_verification',True) and claim.get('claim_id') not in valid: errors.append(f'DESC-003 unverified claim: {claim.get("claim_id")}')
    if d.get('approved') is not True: errors.append('DESC-008 description set not approved')
    return errors


def validate_author_bios(data, legal_name=None):
    d=_load(data); errors=[]
    if not d.get('display_name'): errors.append('BIO-001 display name missing')
    if not d.get('bios'): errors.append('BIO-002 bio variants missing')
    if d.get('protected_legal_identity') and legal_name:
        for b in d.get('bios',[]):
            if legal_name.casefold() in str(b.get('text','')).casefold(): errors.append(f'BIO-003 protected legal identity exposed in {b.get("type")} bio')
    for b in d.get('bios',[]):
        if b.get('approved') is not True: errors.append(f'BIO-004 unapproved bio: {b.get("type")}')
    if d.get('approved') is not True: errors.append('BIO-005 author bios not approved')
    return errors


def kdp_print_royalty_rate(list_price, threshold_60):
    return Decimal('0.60') if D(list_price) >= D(threshold_60) else Decimal('0.50')

def calculate_kdp_print_royalty(list_price, print_cost, royalty_rate):
    return money(D(list_price)*D(royalty_rate)-D(print_cost))

def calculate_kdp_ebook_royalty(list_price, royalty_rate, delivery_cost=0):
    # KDP 70% option may deduct applicable delivery charge; 35% generally does not use this parameter.
    return money(D(list_price)*D(royalty_rate)-D(delivery_cost))

def calculate_ingram_compensation(list_price, wholesale_discount, print_cost, other_charges=0):
    return money(D(list_price)*(Decimal('1')-D(wholesale_discount))-D(print_cost)-D(other_charges))

def calculate_return_exposure(units_returned, list_price, wholesale_discount, handling_per_unit=0, shipping_total=0):
    wholesale=D(list_price)*(Decimal('1')-D(wholesale_discount))
    return money(D(units_returned)*(wholesale+D(handling_per_unit))+D(shipping_total))


def validate_pricing_model(model):
    d=_load(model); errors=[]
    for e in d.get('editions',[]):
        ident=e.get('edition_id','?'); price=D(e.get('list_price',0))
        if price<=0: errors.append(f'PRICE-003 non-positive list price: {ident}')
        if not e.get('currency'): errors.append(f'PRICE-008 currency missing: {ident}')
        if 'estimated_compensation' in e and D(e['estimated_compensation'])<0: errors.append(f'PRICE-005 negative estimated compensation: {ident}')
    if not d.get('rule_snapshot'): errors.append('PRICE-009 pricing rule snapshot missing')
    if d.get('approved') is not True: errors.append('PRICE-010 human pricing approval absent')
    return errors


def validate_wholesale(strategy, minimum_discount=None, maximum_discount=None):
    d=_load(strategy); errors=[]
    for e in d.get('editions',[]):
        disc=D(e.get('wholesale_discount',0)); ident=e.get('edition_id','?')
        if minimum_discount is not None and disc<D(minimum_discount): errors.append(f'WHL-002 discount below current allowed minimum: {ident}')
        if maximum_discount is not None and disc>D(maximum_discount): errors.append(f'WHL-002 discount above current allowed maximum: {ident}')
        if D(e.get('publisher_compensation',0))<0: errors.append(f'WHL-003 compensation negative: {ident}')
        if e.get('approved') is not True: errors.append(f'WHL-008 wholesale decision not approved: {ident}')
    if d.get('approved') is not True: errors.append('WHL-008 wholesale strategy not human-approved')
    return errors


def validate_returns(model):
    d=_load(model); errors=[]; status=d.get('returnability')
    if status=='UNRESOLVED' or not status: errors.append('WHL-004 returns policy undefined')
    rates={round(float(s.get('return_rate',-1)),2) for s in d.get('scenarios',[])}
    required={0.0,0.05,0.10,0.20,0.40}
    if not required.issubset(rates): errors.append('WHL-005 return stress test incomplete')
    maxexp=D(d.get('maximum_return_exposure',0))
    if status!='NON_RETURNABLE':
        worst=max([D(s.get('estimated_loss',0)) for s in d.get('scenarios',[])],default=Decimal('0'))
        if maxexp>0 and worst>maxexp: errors.append('WHL-006 return liability exceeds policy')
        if d.get('approved') is not True: errors.append('WHL-008 returnability requires human approval')
    return errors


def validate_territories(strategy, rights_matrix=None):
    d=_load(strategy); errors=[]; rights={}
    if rights_matrix:
        r=_load(rights_matrix)
        for x in r.get('rights',[]): rights[(x.get('territory'),x.get('format'))]=bool(x.get('allowed'))
    for m in d.get('markets',[]):
        key=(m.get('territory'),m.get('format'))
        if m.get('distribution_enabled'):
            if not m.get('rights_available'): errors.append(f'TERR-001 distribution exceeds rights: {key}')
            if rights and not rights.get(key,False): errors.append(f'TERR-001 rights matrix blocks distribution: {key}')
            if not m.get('currency'): errors.append(f'TERR-004 currency missing: {key}')
    if d.get('approved') is not True: errors.append('TERR-008 territory strategy unapproved')
    return errors


def _date(v):
    if not v: return None
    return date.fromisoformat(str(v)[:10])

def validate_publication_strategy(strategy, gate08_status='PENDING'):
    d=_load(strategy); errors=[]
    try:
        pub=_date(d.get('official_publication_date')); pre=_date(d.get('preorder_start_date')); sub=_date(d.get('submission_target_date')); launch=_date(d.get('marketing_launch_date'))
    except ValueError:
        return ['REL-001 invalid date']
    if not pub: errors.append('REL-001 publication date undefined')
    if pre and pub and pre>=pub: errors.append('REL-002 preorder must begin before publication')
    if sub and pub and sub>=pub: errors.append('REL-003 submission target is not before publication')
    if launch and pub and d.get('release_type')=='coordinated_launch' and launch<pub: errors.append('REL-008 coordinated marketing launch precedes publication')
    if d.get('proof_required') and gate08_status not in ('PASS','PENDING'):
        errors.append('REL-005 proof state blocks release')
    if d.get('approved') is not True: errors.append('REL-010 release approval absent')
    return errors


def validate_channel_map(channel_map, canonical=None, channel_values=None):
    d=_load(channel_map); errors=[]
    if not d.get('mappings'): return ['META-008 channel mapping incomplete']
    if canonical is not None and channel_values is not None:
        c=_load(canonical); v=_load(channel_values)
        for m in d.get('mappings',[]):
            if m.get('parity_class')!='MUST_MATCH': continue
            cf=m.get('canonical_field'); ch=m.get('channel_field')
            if cf in c and ch in v and c.get(cf)!=v.get(ch): errors.append(f'META-004 channel mismatch {cf}->{ch}')
    return errors


def validate_gate07(master, positioning, classification, keywords, descriptions, bios, pricing, wholesale, returns_model, territories, release, human_approval=False):
    errors=[]
    errors += validate_metadata_master(master)
    errors += validate_positioning(positioning)
    errors += validate_classification(classification)
    errors += validate_keywords(keywords)
    errors += validate_descriptions(descriptions, verified_claim_ids=[])
    errors += validate_author_bios(bios)
    errors += validate_pricing_model(pricing)
    errors += validate_wholesale(wholesale)
    errors += validate_returns(returns_model)
    errors += validate_territories(territories)
    errors += validate_publication_strategy(release)
    if not human_approval: errors.append('G07 human commercial approval missing')
    return errors
