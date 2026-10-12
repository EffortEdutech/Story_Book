import json, hashlib
from pathlib import Path
from datetime import date, datetime, timedelta
from validators.isbn import validate_isbn13, normalize_isbn13


def _load(value):
    if isinstance(value,(str,Path)):
        return json.loads(Path(value).read_text(encoding='utf-8'))
    return value


def _day(v):
    if isinstance(v,date): return v
    return date.fromisoformat(str(v)[:10])


def file_sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()


def validate_kdp_rule_snapshot(snapshot, as_of=None, max_age_days=30):
    d=_load(snapshot); errors=[]
    try: verified=_day(d.get('verified_at'))
    except Exception: return ['KDP-RULE-001 verified_at missing or invalid']
    current=_day(as_of) if as_of else date.today()
    if verified > current: errors.append('KDP-RULE-002 rule snapshot is dated in the future')
    if (current-verified).days > max_age_days: errors.append('KDP-RULE-003 cached rule stale')
    if not d.get('sources'): errors.append('KDP-RULE-002 official sources missing')
    if not d.get('rules'): errors.append('KDP-RULE-003 rules missing')
    return errors


def validate_kdp_account(readiness):
    d=_load(readiness); errors=[]
    if not d.get('account',{}).get('exists'): errors.append('KDP-ACC-001 KDP account unavailable')
    if not d.get('account',{}).get('accessible'): errors.append('KDP-ACC-001 KDP account inaccessible')
    if str(d.get('identity',{}).get('status','')).lower() not in ('complete','verified','ready'): errors.append('KDP-ACC-002 identity verification incomplete')
    if str(d.get('tax',{}).get('status','')).lower() not in ('complete','ready'): errors.append('KDP-ACC-003 tax profile incomplete')
    if str(d.get('payments',{}).get('status','')).lower() not in ('complete','configured','ready'): errors.append('KDP-ACC-004 payment profile incomplete')
    if d.get('restrictions'): errors.append('KDP-ACC-005 account restriction detected')
    if d.get('ready_for_submission') is not True: errors.append('KDP-ACC-007 account not marked ready')
    return errors


def validate_kdp_metadata(metadata, canonical=None, max_keywords=7, max_categories=3):
    d=_load(metadata); errors=[]
    for field in ('edition_id','format','language','title','author','description'):
        if not d.get(field): errors.append(f'KDP-META-001 required field missing: {field}')
    if len(d.get('keywords',[])) > max_keywords: errors.append('KDP-META-002 keyword slot limit exceeded')
    if len(d.get('categories',[])) > max_categories: errors.append('KDP-META-003 category selection limit exceeded')
    if len({x.strip().lower() for x in d.get('keywords',[])}) != len(d.get('keywords',[])): errors.append('KDP-META-004 duplicate keyword')
    if not d.get('territories'): errors.append('KDP-META-005 territories missing')
    if d.get('approved') is not True: errors.append('KDP-META-006 channel metadata not approved')
    if canonical:
        c=_load(canonical); work=c.get('work',{}); con=c.get('contributors',{}); pub=c.get('publisher',{})
        if work.get('title') and d.get('title') != work.get('title'): errors.append('KDP-META-007 title differs from metadata master')
        if con.get('primary_author') and d.get('author') != con.get('primary_author'): errors.append('KDP-META-008 author differs from metadata master')
        if d.get('imprint') and pub.get('imprint') and d.get('imprint') != pub.get('imprint'): errors.append('KDP-META-009 imprint differs from metadata master')
    return errors


def validate_kdp_print_isbn(metadata, ingram_planned=False, expected_isbn=None, expected_imprint=None, kdp_free_isbn=False):
    d=_load(metadata); errors=[]
    if d.get('format') not in ('paperback','hardcover'): return ['KDP-ISBN-001 validator requires print format']
    isbn=normalize_isbn13(d.get('isbn',''))
    if not validate_isbn13(isbn): errors.append('KDP-ISBN-002 invalid print ISBN')
    if expected_isbn and normalize_isbn13(expected_isbn) != isbn: errors.append('KDP-ISBN-003 ISBN differs from edition registry')
    if expected_imprint is not None and d.get('imprint') != expected_imprint: errors.append('KDP-ISBN-004 ISBN/imprint mismatch')
    if kdp_free_isbn and ingram_planned: errors.append('KDP-ISBN-ARCHITECTURE-CONFLICT KDP free ISBN cannot support planned external distribution')
    return errors


def validate_print_format_pair(paperback, hardcover):
    p=_load(paperback); h=_load(hardcover); errors=[]
    if normalize_isbn13(p.get('isbn','')) and normalize_isbn13(p.get('isbn','')) == normalize_isbn13(h.get('isbn','')):
        errors.append('KDP-ISBN-005 paperback and hardcover must have different ISBNs')
    return errors


def validate_content_origin(record):
    d=_load(record); errors=[]
    for area in ('manuscript','cover'):
        cls=d.get(area,{}).get('classification')
        if cls in (None,'unknown'): errors.append(f'KDP-AI-001 {area} content origin unresolved')
    expected=any(d.get(area,{}).get('classification') in ('ai_generated','mixed') for area in ('manuscript','cover')) or any(x.get('classification') in ('ai_generated','mixed') for x in d.get('illustrations',[]))
    if d.get('kdp_disclosure_required') != expected: errors.append('KDP-AI-002 disclosure flag inconsistent with recorded origin')
    if not d.get('confirmed_by'): errors.append('KDP-AI-003 human content-origin confirmation missing')
    return errors


def validate_kdp_select(decision):
    d=_load(decision); errors=[]
    choice=d.get('decision')
    if choice not in ('SELECT','WIDE','DEFER'): errors.append('KDP-SELECT-002 decision missing')
    if choice=='SELECT' and d.get('wide_ebook_distribution') is True: errors.append('KDP-SELECT-001 KDP Select conflicts with wide eBook distribution')
    if choice=='SELECT' and d.get('auto_renew') is None: errors.append('KDP-SELECT-003 auto-renew state unknown')
    if not d.get('approved_by'): errors.append('KDP-SELECT-004 human approval missing')
    return errors


def validate_expanded_distribution(check):
    d=_load(check); errors=[]
    if d.get('format')=='hardcover' and d.get('kdp_expanded_distribution_requested'):
        errors.append('KDP-ED-002 hardcover is not eligible for Expanded Distribution')
    conflict=d.get('ingram_distribution_planned') and d.get('same_isbn_on_ingram') and d.get('kdp_expanded_distribution_requested')
    if conflict: errors.append('KDP-ED-001 same ISBN already planned through another distribution service')
    expected_compatible=not conflict and not (d.get('format')=='hardcover' and d.get('kdp_expanded_distribution_requested'))
    if d.get('compatible') != expected_compatible: errors.append('KDP-ED-003 compatibility flag incorrect')
    return errors


def validate_kindle_preorder(release_date, created_date, submission_deadline=None):
    errors=[]
    try: rel=_day(release_date); created=_day(created_date)
    except Exception: return ['KDP-PRE-001 invalid date']
    if rel <= created: errors.append('KDP-PRE-002 release must be after creation date')
    # 18 months represented conservatively as 548 days for deterministic guard; live account timer remains authority.
    if created >= date(2026,9,2) and (rel-created).days > 548: errors.append('KDP-PRE-003 pre-order exceeds current 18-month window')
    if created < date(2026,9,2) and (rel-created).days > 366: errors.append('KDP-PRE-003 pre-order exceeds legacy one-year window')
    if submission_deadline:
        dl=datetime.fromisoformat(str(submission_deadline).replace('Z','+00:00'))
        rd=datetime.combine(rel,datetime.min.time(),tzinfo=dl.tzinfo)
        if rd-dl < timedelta(hours=72): errors.append('KDP-PRE-004 final submission deadline is less than 72 hours before release')
    return errors


def validate_scheduled_print_release(release_date, setup_date):
    try: rel=_day(release_date); setup=_day(setup_date)
    except Exception: return ['KDP-REL-001 invalid date']
    delta=(rel-setup).days; errors=[]
    if delta < 5: errors.append('KDP-REL-002 scheduled print release must be at least 5 days ahead')
    if delta > 90: errors.append('KDP-REL-003 scheduled print release exceeds 90 days')
    return errors


def validate_asset_hashes(candidate, approved):
    c=_load(candidate); a=_load(approved); errors=[]
    for key,value in a.items():
        if value and c.get(key) != value: errors.append(f'KDP-ASSET-001 hash mismatch: {key}')
    return errors


def validate_kindle_preview(report):
    d=_load(report); errors=[]
    if d.get('reviewed') is not True: errors.append('KDP-PREV-001 Kindle preview not reviewed')
    if d.get('findings'): errors.append('KDP-PREV-002 unresolved Kindle preview findings')
    if d.get('approved') is not True: errors.append('KDP-PREV-003 Kindle preview not approved')
    if not d.get('approved_by'): errors.append('KDP-PREV-004 human preview approval missing')
    return errors


def validate_print_previewer(report):
    d=_load(report); errors=[]
    if d.get('previewed') is not True: errors.append('KDP-PREV-005 Print Previewer not run')
    if d.get('blocking_errors'): errors.append('KDP-PREV-006 Print Previewer has blocking errors')
    if d.get('approved') is not True: errors.append('KDP-PREV-007 print preview not approved')
    if not d.get('approved_by'): errors.append('KDP-PREV-008 human print-preview approval missing')
    return errors


def validate_kdp_proof(record, require_physical=True):
    d=_load(record); errors=[]
    if require_physical:
        if d.get('requested') is not True: errors.append('KDP-PROOF-001 physical proof not requested')
        if d.get('received') is not True: errors.append('KDP-PROOF-002 physical proof not received')
        if d.get('inspected') is not True: errors.append('KDP-PROOF-003 physical proof not inspected')
    if d.get('blocking_findings'): errors.append('KDP-PROOF-004 blocking proof findings unresolved')
    if d.get('approval') != 'PASS': errors.append('KDP-PROOF-005 proof approval missing')
    if not d.get('approved_by'): errors.append('KDP-PROOF-006 human proof approval missing')
    return errors


def validate_publication_authorization(auth):
    d=_load(auth); errors=[]
    if d.get('channel') != 'KDP': errors.append('KDP-AUTH-001 wrong channel')
    if d.get('ready') is not True: errors.append('KDP-AUTH-002 edition not ready')
    if d.get('authorized') is not True: errors.append('KDP-AUTH-003 live publication not authorized')
    if not d.get('authorized_by'): errors.append('KDP-AUTH-004 human authorizer missing')
    return errors


def validate_amazon_listing(snapshot, expected):
    s=_load(snapshot); e=_load(expected); errors=[]
    fields=[('title','KDP-LIVE-001'),('author','KDP-LIVE-002'),('isbn','KDP-LIVE-006'),('publisher','KDP-LIVE-005')]
    for f,code in fields:
        if e.get(f) is not None and s.get(f) != e.get(f): errors.append(f'{code} {f} mismatch')
    if e.get('price') is not None and round(float(s.get('price',-1)),2) != round(float(e.get('price')),2): errors.append('KDP-LIVE-004 price mismatch')
    if e.get('cover_hash') and s.get('cover_hash') != e.get('cover_hash'): errors.append('KDP-LIVE-003 cover mismatch')
    return errors


def validate_gate_kdp01(rule_snapshot, account, metadata_records, select_decision, expanded_checks, previews, proofs, authorizations, human_gate_approval=False):
    errors=[]
    errors += validate_kdp_rule_snapshot(rule_snapshot, as_of=date(2026,10,10), max_age_days=30)
    errors += validate_kdp_account(account)
    for m in metadata_records: errors += validate_kdp_metadata(m)
    errors += validate_kdp_select(select_decision)
    for x in expanded_checks: errors += validate_expanded_distribution(x)
    for p in previews:
        if _load(p).get('format') in ('paperback','hardcover'): errors += validate_print_previewer(p)
        else: errors += validate_kindle_preview(p)
    for proof in proofs: errors += validate_kdp_proof(proof)
    for auth in authorizations: errors += validate_publication_authorization(auth)
    if not human_gate_approval: errors.append('KDP01 human KDP gate approval missing')
    return errors
