import json
from pathlib import Path
from datetime import date, timedelta
from decimal import Decimal
from validators.isbn import validate_isbn13, normalize_isbn13
from validators.phase4 import calculate_ingram_compensation


def _load(value):
    if isinstance(value,(str,Path)):
        return json.loads(Path(value).read_text(encoding='utf-8'))
    return value

def _day(v):
    if isinstance(v,date): return v
    return date.fromisoformat(str(v)[:10])

def D(v): return Decimal(str(v))


def validate_ingram_rule_snapshot(snapshot, as_of=None, max_age_days=30):
    d=_load(snapshot); errors=[]
    try: verified=_day(d.get('verified_at'))
    except Exception: return ['ING-RULE-001 verified_at missing or invalid']
    current=_day(as_of) if as_of else date.today()
    if verified>current: errors.append('ING-RULE-002 rule snapshot dated in the future')
    if (current-verified).days>max_age_days: errors.append('ING-RULE-003 rule snapshot stale')
    if not d.get('sources'): errors.append('ING-RULE-002 official sources missing')
    if not d.get('rules'): errors.append('ING-RULE-003 rules missing')
    return errors


def validate_ingram_account(readiness):
    d=_load(readiness); errors=[]
    if not d.get('account',{}).get('exists') or not d.get('account',{}).get('accessible'): errors.append('ING-ACC-001 account unavailable')
    if str(d.get('publisher_profile',{}).get('status','')).lower() not in ('complete','verified','ready'): errors.append('ING-ACC-002 publisher profile incomplete')
    if str(d.get('payments',{}).get('status','')).lower() not in ('complete','configured','ready'): errors.append('ING-ACC-003 payment setup incomplete')
    if d.get('restrictions'): errors.append('ING-ACC-004 account restriction detected')
    if d.get('ready_for_submission') is not True: errors.append('ING-ACC-005 account not marked ready')
    return errors


def validate_ingram_metadata(metadata, canonical=None):
    d=_load(metadata); errors=[]
    for field in ('edition_id','format','title','author','imprint','isbn','language','description'):
        if not d.get(field): errors.append(f'ING-META-001 required field missing: {field}')
    if not validate_isbn13(d.get('isbn','')): errors.append('ING-META-005 invalid ISBN')
    if not d.get('subjects'): errors.append('ING-META-006 subject mapping missing')
    if not d.get('markets'): errors.append('ING-META-010 markets missing')
    if d.get('approved') is not True: errors.append('ING-META-010 metadata not approved')
    if canonical:
        c=_load(canonical); work=c.get('work',{}); con=c.get('contributors',{}); pub=c.get('publisher',{})
        if work.get('title') and d.get('title')!=work.get('title'): errors.append('ING-META-001 title mismatch')
        if con.get('primary_author') and d.get('author')!=con.get('primary_author'): errors.append('ING-META-003 author mismatch')
        if pub.get('imprint') and d.get('imprint')!=pub.get('imprint'): errors.append('ING-META-004 imprint mismatch')
    return errors


def validate_ingram_manufacturing(config, expected_page_count=None, approved_hashes=None):
    d=_load(config); errors=[]
    if d.get('format') not in ('paperback','hardcover'): errors.append('ING-PRD-002 unsupported binding/format')
    trim=d.get('trim',{})
    if float(trim.get('width_in',0))<=0 or float(trim.get('height_in',0))<=0: errors.append('ING-PRD-001 invalid trim')
    if int(d.get('page_count',0))<=0: errors.append('ING-PRD-003 invalid page count')
    if expected_page_count is not None and int(d.get('page_count',0))!=int(expected_page_count): errors.append('ING-PRD-003 page count differs from production lock')
    if int(d.get('template_page_count',0))!=int(d.get('page_count',0)): errors.append('ING-PRD-009 cover template stale for current page count')
    if not d.get('cover_template_id'): errors.append('ING-PRD-009 cover template missing')
    if approved_hashes:
        if approved_hashes.get('interior') and d.get('interior_hash')!=approved_hashes.get('interior'): errors.append('ING-PRD-010 interior asset hash mismatch')
        if approved_hashes.get('cover') and d.get('cover_hash')!=approved_hashes.get('cover'): errors.append('ING-PRD-010 cover asset hash mismatch')
    if d.get('approved') is not True: errors.append('ING-PRD-012 manufacturing configuration not approved')
    return errors


def validate_ingram_isbn_reconciliation(record, expected_isbn=None):
    d=_load(record); errors=[]
    isbn=normalize_isbn13(d.get('isbn',''))
    if not validate_isbn13(isbn): errors.append('ING-ISBN-001 invalid ISBN')
    if expected_isbn and isbn!=normalize_isbn13(expected_isbn): errors.append('ING-ISBN-003 ISBN differs from edition registry')
    if d.get('publisher_owned') is not True: errors.append('ING-ISBN-005 shared KDP/Ingram architecture requires publisher-owned ISBN')
    vals=[normalize_isbn13(d.get(k,'')) for k in ('kdp_isbn','ingram_isbn','copyright_page_isbn','cover_isbn') if d.get(k)]
    if any(v!=isbn for v in vals): errors.append('ING-ISBN-003 ISBN parity failure')
    if d.get('consistent') is not True: errors.append('ING-ISBN-010 record not marked consistent')
    return errors


def validate_print_isbn_pair(paperback, hardcover):
    p=_load(paperback); h=_load(hardcover); errors=[]
    if normalize_isbn13(p.get('isbn','')) and normalize_isbn13(p.get('isbn',''))==normalize_isbn13(h.get('isbn','')): errors.append('ING-ISBN-006 paperback ISBN reused for hardcover')
    return errors


def validate_kdp_ingram_coexistence(record):
    d=_load(record); errors=[]
    if d.get('ingram_distribution') and d.get('kdp_direct'):
        if d.get('same_publisher_owned_isbn') is not True: errors.append('ING-ISBN-003 same edition must reconcile to publisher-owned ISBN')
        if d.get('kdp_expanded_distribution') is True: errors.append('ING-ISBN-008 KDP Expanded Distribution conflict')
    if d.get('historical_kdp_expanded_distribution') is True: errors.append('ING-ISBN-009 historical Expanded Distribution requires title-transfer/distribution reconciliation')
    compatible=not any(code in ' '.join(errors) for code in ['ING-ISBN-003','ING-ISBN-008','ING-ISBN-009'])
    if d.get('compatible')!=compatible: errors.append('ING-ISBN-011 compatibility flag incorrect')
    return errors


def _discount_bounds(market):
    m=str(market).upper()
    if m in ('US','USA','UNITED STATES','CA','CANADA'): return Decimal('0.40'),Decimal('0.55')
    return Decimal('0.35'),Decimal('0.55')


def validate_ingram_market_pricing(model):
    d=_load(model); errors=[]
    for row in d.get('markets',[]):
        market=row.get('market','?'); discount=D(row.get('wholesale_discount',0)); lo,hi=_discount_bounds(market)
        if discount<lo or discount>hi: errors.append(f'ING-WHL-004 discount outside current allowed range: {market}')
        expected=calculate_ingram_compensation(row.get('list_price',0),discount,row.get('print_cost',0),row.get('other_charges',0))
        reported=D(row.get('estimated_publisher_compensation',0))
        if reported<0: errors.append(f'ING-WHL-005 compensation negative: {market}')
        if abs(expected-reported)>Decimal('0.01'): errors.append(f'ING-WHL-009 publisher compensation mismatch: {market}')
    if not d.get('rule_snapshot'): errors.append('ING-WHL-003 wholesale rule snapshot missing')
    if d.get('approved') is not True or not d.get('approved_by'): errors.append('ING-WHL-008 human wholesale approval absent')
    return errors


def validate_ingram_return_policy(policy):
    d=_load(policy); errors=[]; status=d.get('returnability')
    if status not in ('NON_RETURNABLE','YES_DELIVER','YES_DESTROY'): errors.append('ING-RET-001 returns decision missing/invalid')
    if d.get('risk_model_current') is not True: errors.append('ING-RET-002 return stress test/risk model missing or stale')
    if D(d.get('estimated_worst_case_exposure',0))>D(d.get('maximum_return_exposure',0)) and D(d.get('maximum_return_exposure',0))>0: errors.append('ING-RET-004 return exposure exceeds approval')
    if status=='YES_DELIVER' and d.get('deliver_logistics_resolved') is not True: errors.append('ING-RET-005 Deliver logistics unresolved')
    if status in ('YES_DELIVER','YES_DESTROY') and (d.get('approved') is not True or not d.get('approved_by')): errors.append('ING-RET-006 returnable status lacks explicit approval')
    prev=d.get('previous_returnability')
    if prev in ('YES_DELIVER','YES_DESTROY') and status=='NON_RETURNABLE':
        if not d.get('change_date') or not d.get('tail_end_date') or d.get('tail_exposure_modelled') is not True: errors.append('ING-RET-008 180-day residual return liability not modelled')
        else:
            try:
                expected=_day(d['change_date'])+timedelta(days=180)
                if _day(d['tail_end_date'])<expected: errors.append('ING-RET-008 return tail ends before 180 days')
            except Exception: errors.append('ING-RET-008 invalid return-tail dates')
    return errors


def validate_ingram_eproof(record):
    d=_load(record); errors=[]
    if d.get('processing_complete') is not True: errors.append('ING-PROOF-001 file processing incomplete')
    if d.get('eproof_available') is not True: errors.append('ING-PROOF-002 eProof unavailable')
    if d.get('reviewed') is not True: errors.append('ING-PROOF-003 eProof not reviewed')
    if d.get('blocking_findings'): errors.append('ING-PROOF-004 blocking eProof findings unresolved')
    if d.get('approval')!='APPROVED_FOR_PRINT_PROOF': errors.append('ING-PROOF-005 eProof not approved for print proof')
    if not d.get('approved_by'): errors.append('ING-PROOF-006 human eProof approval missing')
    return errors


def validate_ingram_physical_proof(record):
    d=_load(record); errors=[]
    if d.get('ordered') is not True: errors.append('ING-PHYS-001 physical copy not ordered')
    if d.get('received') is not True: errors.append('ING-PHYS-002 physical copy not received')
    if d.get('inspected') is not True: errors.append('ING-PHYS-003 physical copy not inspected')
    if d.get('blocking_findings'): errors.append('ING-PHYS-004 blocking physical-proof findings unresolved')
    if d.get('approval')!='PASS': errors.append('ING-PHYS-005 physical proof approval missing')
    if not d.get('approved_by'): errors.append('ING-PHYS-006 human physical-proof approval missing')
    return errors


def validate_gate08_components(components, human_approval=False):
    errors=[]
    for comp,status in components.items():
        if status not in ('PASS','NOT_APPLICABLE'): errors.append(f'G08 component not passed: {comp}')
    if not human_approval: errors.append('G08 human physical-proof approval missing')
    return errors


def validate_ingram_distribution_authorization(auth):
    d=_load(auth); errors=[]
    if d.get('gate08_status')!='PASS': errors.append('ING-DIST-001 GATE-08 has not passed')
    if not d.get('markets'): errors.append('ING-DIST-002 distribution markets missing')
    if d.get('authorized') is not True or not d.get('authorized_by'): errors.append('ING-DIST-003 distribution activation not human-authorized')
    return errors


def validate_retailer_listing(snapshot, expected):
    s=_load(snapshot); e=_load(expected); errors=[]
    for f,code in [('title','ING-LIVE-001'),('author','ING-LIVE-002'),('isbn','ING-LIVE-003'),('publisher','ING-LIVE-004')]:
        if e.get(f) is not None and s.get(f)!=e.get(f): errors.append(f'{code} {f} mismatch')
    if e.get('price') is not None and round(float(s.get('price',-1)),2)!=round(float(e.get('price')),2): errors.append('ING-LIVE-005 price mismatch')
    if e.get('cover_hash') and s.get('cover_hash')!=e.get('cover_hash'): errors.append('ING-LIVE-006 cover mismatch')
    return errors


def validate_gate_ingram01(rule_snapshot, account, metadata_records, manufacturing_records, isbn_records, coexistence_records, pricing_records, return_records, eproof_records, physical_proofs, distribution_authorizations, human_gate_approval=False):
    errors=[]
    errors += validate_ingram_rule_snapshot(rule_snapshot,as_of=date(2026,10,10),max_age_days=30)
    errors += validate_ingram_account(account)
    for x in metadata_records: errors += validate_ingram_metadata(x)
    for x in manufacturing_records: errors += validate_ingram_manufacturing(x)
    for x in isbn_records: errors += validate_ingram_isbn_reconciliation(x)
    for x in coexistence_records: errors += validate_kdp_ingram_coexistence(x)
    for x in pricing_records: errors += validate_ingram_market_pricing(x)
    for x in return_records: errors += validate_ingram_return_policy(x)
    for x in eproof_records: errors += validate_ingram_eproof(x)
    for x in physical_proofs: errors += validate_ingram_physical_proof(x)
    for x in distribution_authorizations: errors += validate_ingram_distribution_authorization(x)
    if not human_gate_approval: errors.append('ING01 human Ingram gate approval missing')
    return errors
