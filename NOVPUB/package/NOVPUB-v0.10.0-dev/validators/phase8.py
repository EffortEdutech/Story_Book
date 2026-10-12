import json, hashlib, calendar
from datetime import date, datetime
from pathlib import Path
from decimal import Decimal


def _load(x):
    if isinstance(x,(str,Path)):
        return json.loads(Path(x).read_text(encoding='utf-8'))
    return x


def add_months(d, months):
    if isinstance(d,str): d=date.fromisoformat(d)
    m=d.month-1+months; y=d.year+m//12; m=m%12+1
    day=min(d.day, calendar.monthrange(y,m)[1])
    return date(y,m,day)


def legal_deposit_deadline(publication_date, material_type):
    d=date.fromisoformat(publication_date) if isinstance(publication_date,str) else publication_date
    if material_type=='PRINTED': return add_months(d,1)
    if material_type=='NON_PRINTED': return date(d.year+1,d.month,min(d.day,calendar.monthrange(d.year+1,d.month)[1]))
    raise ValueError('unsupported material_type')


def validate_sales_records(records):
    rows=_load(records); rows=rows.get('records',rows) if isinstance(rows,dict) else rows
    errors=[]; keys=set()
    for r in rows:
        rid=r.get('record_id','?')
        for f in ('channel','edition_id','currency','period','transaction_class','source_reference'):
            if not r.get(f): errors.append(f'FIN-001/003 missing {f}: {rid}')
        if len(str(r.get('currency','')))!=3: errors.append(f'FIN-005 invalid currency: {rid}')
        key=(r.get('source_hash'),r.get('source_reference'),r.get('record_id'))
        if key in keys: errors.append(f'FIN-004 duplicate sales record: {rid}')
        keys.add(key)
    return errors


def deduplicate_sales_records(records):
    rows=_load(records); rows=rows.get('records',rows) if isinstance(rows,dict) else rows
    seen=set(); out=[]
    for r in rows:
        key=(r.get('source_hash'),r.get('source_reference'),r.get('record_id'))
        if key not in seen: out.append(r); seen.add(key)
    return out


def validate_financial_reconciliation(record):
    d=_load(record); errors=[]
    if len(str(d.get('currency','')))!=3: errors.append('FIN-005 currency mismatch/invalid')
    expected=Decimal(str(d.get('expected',0))); reported=Decimal(str(d.get('reported',0))); paid=Decimal(str(d.get('paid',0)))
    abs_thr=Decimal(str(d.get('threshold_absolute',0))); pct_thr=Decimal(str(d.get('threshold_percentage',0)))
    er=abs(expected-reported); rp=abs(reported-paid)
    pct=(er/abs(expected)*Decimal('100')) if expected else Decimal('0')
    if er>abs_thr and pct>pct_thr: errors.append('FIN-007 expected/reported variance exceeds threshold')
    if d.get('status')=='MATCHED' and (er>abs_thr or rp>abs_thr): errors.append('FIN-007 status MATCHED conflicts with variance')
    return errors


def validate_payment_record(record):
    d=_load(record); errors=[]
    if d.get('status')=='PAID' and not d.get('payment_date'): errors.append('FIN-008 paid payment missing payment date')
    if d.get('status')=='PAID' and Decimal(str(d.get('actual_payment',0)))==0 and Decimal(str(d.get('gross_payable',0)))!=0: errors.append('FIN-008 paid amount missing')
    return errors


def validate_select_lifecycle(record, current_date=None):
    d=_load(record); errors=[]; today=current_date or date.today()
    if d.get('enrolled'):
        if d.get('auto_renew') is None: errors.append('SEL-002 auto-renewal state unknown')
        if not d.get('term_start') or not d.get('term_end'): errors.append('SEL-001 Select term dates unknown')
        else:
            start=date.fromisoformat(d['term_start']); end=date.fromisoformat(d['term_end'])
            delta=(end-start).days
            if delta not in (89,90): errors.append('SEL-001 Select term is not approximately 90 days')
        if d.get('wide_ebook_distribution'): errors.append('SEL-003 wide eBook distribution conflicts with Select exclusivity')
        if d.get('decision') in ('RENEW_SELECT','OPT_OUT_AT_END') and (d.get('human_approved') is not True or not d.get('approved_by')): errors.append('SEL-004 Select lifecycle decision lacks human approval')
    return errors


def validate_optimization(record):
    d=_load(record); errors=[]
    if not d.get('baseline'): errors.append('OPT-001 baseline missing')
    if not d.get('hypothesis'): errors.append('OPT-002 hypothesis missing')
    if d.get('identity_critical'): errors.append('OPT-004 identity-critical field requires edition review')
    if d.get('misleading'): errors.append('OPT-006 misleading metadata/category/keyword proposal')
    if d.get('field')=='price' and d.get('economics_recalculated') is not True: errors.append('OPT-008 price economics not recalculated')
    if d.get('approved') is not True or not d.get('approved_by'): errors.append('OPT-003 post-publication change lacks human approval')
    if d.get('reversion_available') is not True: errors.append('OPT-009 reversion state unavailable')
    return errors


def classify_revision(change):
    d=_load(change)
    if d.get('new_format'): return 'R4_NEW_FORMAT'
    if d.get('new_chapters') or d.get('new_ending') or d.get('major_structural_revision') or d.get('new_translation'): return 'R3_NEW_EDITION'
    if d.get('material_textual_changes') or d.get('significant_back_matter'): return 'R2_MATERIAL_REVIEW'
    if d.get('minor_typo') or d.get('minor_layout_fix'): return 'R1_MINOR_CORRECTION'
    return 'R0_METADATA'


def validate_revision_classification(record):
    d=_load(record); errors=[]
    if not d.get('recommended_classification'): errors.append('EDM-001 revision not classified'); return errors
    if d.get('recommended_classification') in ('R3_NEW_EDITION','R4_NEW_FORMAT') and d.get('new_isbn_review') is not True: errors.append('EDM-002/003 new edition/format lacks identifier review')
    if d.get('recommended_classification')=='R3_NEW_EDITION' and d.get('reopen_phase1') is not True: errors.append('EDM-007 new edition bypasses editorial gate')
    if d.get('human_decision') is not True or not d.get('approved_by'): errors.append('EDM-001 revision classification lacks human approval')
    return errors


def validate_erratum(record):
    d=_load(record); errors=[]
    if d.get('verified') is not True and d.get('status') not in ('REPORTED','REJECTED'): errors.append('ERR-001 unverified report advanced')
    if d.get('severity')=='MISSING_CONTENT' and d.get('status') in ('RELEASED','CORRECTED') and not d.get('correct_text_or_resolution'): errors.append('ERR-002 missing-content correction lacks resolution')
    return errors


def validate_return_exposure(record, current_date=None):
    d=_load(record); errors=[]
    if d.get('returnability') not in ('NON_RETURNABLE','YES_DELIVER','YES_DESTROY'): errors.append('INGOPS-002 returnability unknown')
    if d.get('change_date') and d.get('tail_end_date'):
        start=date.fromisoformat(d['change_date']); end=date.fromisoformat(d['tail_end_date'])
        if d.get('tail_days',0) and (end-start).days < int(d['tail_days'])-1: errors.append('INGOPS-003 return tail shorter than declared policy')
        if d.get('tail_days')==180 and (end-start).days < 179: errors.append('INGOPS-003 180-day return tail not tracked')
    if Decimal(str(d.get('worst_case_exposure',0))) < Decimal(str(d.get('current_exposure',0))): errors.append('INGOPS-002 worst-case exposure below current exposure')
    return errors


def validate_return_record(record):
    d=_load(record); errors=[]
    if d.get('reconciled') is not True: errors.append('INGOPS-001 return report not reconciled')
    calc=Decimal(str(d.get('wholesale_value',0)))+Decimal(str(d.get('shipping_handling',0)))
    if abs(calc-Decimal(str(d.get('total_cost',0))))>Decimal('0.01'): errors.append('INGOPS-008 return cost does not reconcile')
    return errors


def validate_feedback(record):
    d=_load(record); errors=[]
    if not d.get('source'): errors.append('QI-001 feedback source missing')
    if d.get('feedback_type')=='READER_PREFERENCE' and d.get('action_required') and d.get('verified') is not True: errors.append('QI-002 reader preference misclassified as verified defect')
    if d.get('feedback_type')=='PRODUCTION_DEFECT' and d.get('verified') and d.get('action_required') is not True: errors.append('QI-003 verified defect signal ignored')
    return errors


def validate_legal_deposit(record, current_date=None):
    d=_load(record); errors=[]; today=current_date or date.today()
    if not d.get('rule_snapshot_verified_at'): errors.append('MYCOMP-010 rule snapshot missing')
    try: expected=legal_deposit_deadline(d['publication_date'],d['material_type'])
    except Exception: errors.append('MYCOMP-002/003 invalid publication/material data'); return errors
    try: actual=date.fromisoformat(d.get('deadline',''))
    except Exception: errors.append('MYCOMP-003 deadline missing/invalid'); actual=None
    if actual and actual!=expected: errors.append('MYCOMP-003 deadline does not match current rule snapshot')
    expected_units=5 if d.get('material_type')=='PRINTED' else 2
    if d.get('copies_or_units_required')!=expected_units: errors.append('MYCOMP-005 wrong copies/units for current snapshot')
    if actual and today>actual and not d.get('submitted'): errors.append('MYCOMP-004 legal deposit overdue')
    if d.get('closed') and not d.get('evidence'): errors.append('MYCOMP-009 compliance closed without evidence')
    if d.get('status')=='CLOSED' and d.get('closed') is not True: errors.append('MYCOMP-009 CLOSED status without closed flag')
    return errors


def validate_rights_opportunity(record):
    d=_load(record); errors=[]
    if d.get('rights_available') is not True: errors.append('RIGHTSOP-001 right not owned/available')
    if d.get('existing_exclusive_conflict'): errors.append('RIGHTSOP-003 existing exclusive licence conflict')
    if d.get('type') in ('AUDIOBOOK','TRANSLATION','LARGE_PRINT','SPECIAL_EDITION') and not d.get('format'): errors.append('RIGHTSOP-004 new format lacks format definition')
    return errors


def validate_publication_manifest(record):
    d=_load(record); errors=[]
    if d.get('archive_verified') is not True: errors.append('ARCVE-001 archive not verified')
    if not d.get('active_editions'): errors.append('ARCVE-003 active edition mapping incomplete')
    assets=d.get('current_assets',{})
    for k in ('manuscript','metadata'):
        if not assets.get(k): errors.append(f'ARCVE-001 authoritative asset missing: {k}')
    return errors


def validate_provenance_graph(record):
    d=_load(record); errors=[]
    nodes={n.get('id') for n in d.get('nodes',[])}
    if not nodes: errors.append('ARCVE-005 provenance graph empty')
    for e in d.get('edges',[]):
        if e.get('from') not in nodes or e.get('to') not in nodes: errors.append('ARCVE-005 provenance edge references missing node')
    return errors


def validate_recovery_manifest(record):
    d=_load(record); errors=[]
    if not d.get('required_source_files'): errors.append('ARCVE-006 recovery source files missing')
    if d.get('credential_policy')!='REFERENCE_ONLY_NO_SECRETS': errors.append('ARCVE-007 sensitive credential policy invalid')
    return errors


def validate_gate10(gate09_status, publication_state, financial_reconciliation, select_state, return_exposure, legal_deposits, publication_manifest, provenance_graph, recovery_manifest, human_approval=False):
    errors=[]
    if gate09_status!='PASS': errors.append('G10 GATE-09 not PASS')
    ps=_load(publication_state)
    if not ps.get('active_editions'): errors.append('G10 active editions not verified')
    if ps.get('channel_status') is None: errors.append('G10 channel status missing')
    errors += validate_financial_reconciliation(financial_reconciliation)
    ss=_load(select_state)
    if ss.get('enrolled'): errors += validate_select_lifecycle(ss)
    errors += validate_return_exposure(return_exposure)
    deps=_load(legal_deposits); deps=deps.get('deposits',deps) if isinstance(deps,dict) else deps
    for dep in deps: errors += validate_legal_deposit(dep)
    errors += validate_publication_manifest(publication_manifest)
    errors += validate_provenance_graph(provenance_graph)
    errors += validate_recovery_manifest(recovery_manifest)
    if not human_approval: errors.append('G10 human post-publication governance approval missing')
    return errors
