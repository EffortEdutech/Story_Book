import json, hashlib
from pathlib import Path
from datetime import date, datetime

VALID_GATE_STATUSES={'PENDING','PASS','FAIL','CONDITIONAL','NOT_APPLICABLE'}

def _load(x):
    if isinstance(x,(str,Path)):
        p=Path(x)
        if p.exists(): return json.loads(p.read_text(encoding='utf-8'))
    return x

def validate_registry_integrity(package_root):
    root=Path(package_root); errors=[]
    skills=json.loads((root/'registry/skill_registry.json').read_text())['skills']
    ids=[s.get('skill_id') for s in skills]
    if len(ids)!=96 or len(set(ids))!=96: errors.append('STATIC-001/002 skill registry must contain NPUB-01..NPUB-96 exactly once')
    expected={f'NPUB-{i:02d}' for i in range(1,97)}
    if set(ids)!=expected: errors.append('STATIC-002 missing/unexpected skill IDs')
    manifest=json.loads((root/'MANIFEST.json').read_text())
    implemented=set(manifest.get('implemented_skills',[]))
    regimpl={s['skill_id'] for s in skills if s.get('implementation_status')=='implemented'}
    if implemented!=regimpl: errors.append('STATIC-010 manifest/skill registry implementation mismatch')
    for s in skills:
        if s.get('implementation_status')=='implemented' and not (root/s.get('skill_file','')).exists(): errors.append(f"STATIC-002 missing skill file: {s['skill_id']}")
    gates=json.loads((root/'registry/gate_registry.json').read_text())['gates']
    gids=[g.get('gate_id') for g in gates]
    if len(gids)!=len(set(gids)): errors.append('STATIC-006 duplicate gate ID')
    states=json.loads((root/'registry/state_registry.json').read_text())['states']
    if len(states)!=len(set(states)): errors.append('STATIC-007 duplicate state')
    vals=json.loads((root/'registry/validator_registry.json').read_text())['validators']
    vids=[v.get('validator_id') for v in vals]
    if len(vids)!=len(set(vids)): errors.append('STATIC-008 duplicate validator ID')
    for v in vals:
        if not (root/v.get('path','')).exists(): errors.append(f"STATIC-008 validator path missing: {v.get('validator_id')}")
    for phase in manifest.get('implemented_phases',[]):
        if not (root/f'workflows/phase{phase}.yaml').exists(): errors.append(f'STATIC-010 workflow missing: phase{phase}')
    return errors

def validate_gate_evidence(record):
    d=_load(record); errors=[]
    if d.get('result') not in VALID_GATE_STATUSES: errors.append('GATEVAL-008 invalid gate status')
    if d.get('result')=='PASS' and not d.get('evidence'): errors.append('GATEVAL-002 PASS without evidence')
    if d.get('human_required') and d.get('result')=='PASS':
        if not d.get('approved_by') or str(d.get('approved_by')).strip().upper() in {'AI','CODEX','CLAUDE','ASSISTANT'}: errors.append('GATEVAL-003 human approval missing/self-approved')
    if d.get('uses_superseded_evidence'): errors.append('GATEVAL-007 superseded evidence used')
    if d.get('result')=='NOT_APPLICABLE' and not d.get('na_reason'): errors.append('GATEVAL-005 NOT_APPLICABLE lacks justification')
    return errors

ALLOWED_MAJOR_TRANSITIONS={
'MANUSCRIPT_COMPLETE':{'INTAKE_COMPLETE','EDITORIAL_REVIEW'},
'EDITORIAL_APPROVED':{'RIGHTS_REVIEW','RIGHTS_CLEARED'},
'RIGHTS_CLEARED':{'PUBLICATION_IDENTITY_REVIEW','PUBLICATION_IDENTITY_APPROVED'},
'PUBLICATION_IDENTITY_APPROVED':{'PRODUCTION_REVIEW','FORMAT_STRATEGY_APPROVED'},
'PRODUCTION_ASSETS_APPROVED':{'COMMERCIAL_REVIEW','COMMERCIAL_METADATA_APPROVED'},
'COMMERCIAL_METADATA_APPROVED':{'KDP_RULES_CURRENT','INGRAM_RULES_CURRENT'},
'KDP_VERIFIED':{'INGRAM_RULES_CURRENT','LAUNCH_STRATEGY_APPROVED','WIDE_DISTRIBUTION_VERIFIED'},
'WIDE_DISTRIBUTION_VERIFIED':{'LAUNCH_STRATEGY_APPROVED','SOFT_LAUNCH_QA'},
'PUBLICLY_LAUNCHED':{'POST_PUBLICATION_ACTIVE','FINANCIAL_RECONCILIATION_ACTIVE'},
'PUBLICATION_GOVERNED':{'NOVPUB_V1_RC_APPROVED'},
'NOVPUB_V1_RC_APPROVED':{'PILOT_INITIALIZED'},
'NOVPUB_V1_FREEZE_READY':{'NOVPUB_V1_0_0_RELEASED'},
}

def validate_major_transition(current_state,next_state,gate_statuses=None):
    errors=[]; gate_statuses=gate_statuses or {}
    allowed=ALLOWED_MAJOR_TRANSITIONS.get(current_state,set())
    if next_state not in allowed: errors.append('GATEVAL-004 invalid major state transition')
    required={
      ('PUBLICATION_GOVERNED','NOVPUB_V1_RC_APPROVED'):'GATE-NOVPUB-RC1',
      ('NOVPUB_V1_FREEZE_READY','NOVPUB_V1_0_0_RELEASED'):'GATE-NOVPUB-V1',
    }.get((current_state,next_state))
    if required and gate_statuses.get(required)!='PASS': errors.append('GATEVAL-001 gate bypass')
    return errors

def validate_determinism_runs(runs):
    rows=_load(runs); rows=rows.get('runs',rows) if isinstance(rows,dict) else rows
    errors=[]; groups={}
    for r in rows:
        key=(r.get('engine'),r.get('input_hash'))
        groups.setdefault(key,set()).add(r.get('output_hash'))
    for key,outs in groups.items():
        if len(outs)>1: errors.append(f'DET-001 non-deterministic result: {key[0]}')
    return errors

def validate_parity_results(results):
    rows=_load(results); rows=rows.get('results',rows) if isinstance(rows,dict) else rows
    errors=[]
    for r in rows:
        if r.get('parity_class')=='MUST_MATCH' and r.get('expected')!=r.get('actual'): errors.append(f"PARITY-001/010 MUST_MATCH drift: {r.get('field')}")
        if r.get('pass') is False and r.get('parity_class')=='MUST_MATCH': errors.append(f"PARITY-008 parity failed: {r.get('field')}")
    return errors

def validate_provenance_chain(record):
    d=_load(record); errors=[]; nodes={n.get('id') for n in d.get('nodes',[]) if n.get('id')}
    adj={n:set() for n in nodes}
    for e in d.get('edges',[]):
        a,b=e.get('from'),e.get('to')
        if a not in nodes or b not in nodes: errors.append('PARITY-008 provenance edge references missing node'); continue
        adj[a].add(b)
    temp=set(); perm=set()
    def visit(n):
        if n in temp: return False
        if n in perm: return True
        temp.add(n)
        for x in adj[n]:
            if not visit(x): return False
        temp.remove(n); perm.add(n); return True
    for n in nodes:
        if not visit(n): errors.append('PARITY-008 provenance cycle detected'); break
    if d.get('required_terminal') and d.get('required_terminal') not in nodes: errors.append('PARITY-008 required terminal missing')
    return errors

def validate_rule_freshness_result(record,current_date=None):
    d=_load(record); errors=[]; today=current_date or date.today()
    if d.get('authoritative') is not True: errors.append('RULE-008 rule source not authoritative/provenance missing')
    if not d.get('verified_at'): errors.append('RULE-003 critical rule verification date unknown'); return errors
    try: checked=date.fromisoformat(str(d['verified_at'])[:10])
    except Exception: errors.append('RULE-003 invalid verification date'); return errors
    ttl=int(d.get('ttl_days',0)); stale=(today-checked).days>ttl
    if stale or d.get('status')=='STALE': errors.append('RULE-001 snapshot stale')
    if d.get('status')=='UNKNOWN': errors.append('RULE-003 critical rule unknown')
    return errors

def validate_fixture_manifest(record):
    d=_load(record); rows=d.get('fixtures',[]); errors=[]; ids=[]
    classes={'UNIT','PHASE','CROSS_PHASE','END_TO_END','NEGATIVE','BOUNDARY','RECOVERY'}
    for r in rows:
        ids.append(r.get('fixture_id'))
        if r.get('class') not in classes: errors.append(f"FIX-004 invalid fixture class: {r.get('fixture_id')}")
        if 'expected' not in r: errors.append(f"FIX-004 expected result missing: {r.get('fixture_id')}")
    if len(ids)!=len(set(ids)): errors.append('FIX-005 duplicate/non-reproducible fixture IDs')
    return errors

def validate_adversarial_catalog(record):
    d=_load(record); attacks=d.get('attacks',[]); errors=[]
    ids=[a.get('attack_id') for a in attacks]
    expected=[f'ADV-{i:03d}' for i in range(1,161)]
    if ids!=expected: errors.append('ADV-CAT-001 catalog must contain ordered ADV-001 through ADV-160')
    for a in attacks:
        if not a.get('description') or not a.get('expected_control'): errors.append(f"ADV-CAT-002 incomplete attack: {a.get('attack_id')}")
    return errors

def validate_adversarial_results(record):
    d=_load(record); rows=d.get('results',[]); errors=[]
    for r in rows:
        if r.get('passed') is not True and r.get('severity') in ('CRITICAL','HIGH'): errors.append(f"ADV-FAIL release-blocking attack failed: {r.get('attack_id')}")
    return errors

def validate_agent_parity(record):
    d=_load(record); rows=d.get('comparisons',[d]) if isinstance(d,dict) else d; errors=[]
    for r in rows:
        if r.get('deterministic') and r.get('equivalent') is not True: errors.append(f"AGENT-001 deterministic divergence: {r.get('fixture_id')}")
        if r.get('material_difference') and not r.get('resolution'): errors.append(f"AGENT-002 unresolved material divergence: {r.get('fixture_id')}")
    return errors

def validate_professional_review(record):
    d=_load(record); findings=d.get('findings',[]); errors=[]
    if d.get('review_status')=='COMPLETE' and not d.get('human_review_evidence'): errors.append('PRO-001 professional review marked complete without human evidence')
    for f in findings:
        if f.get('reviewer_is_human') is not True: errors.append(f"PRO-002 non-human reviewer cannot certify: {f.get('finding_id')}")
        if f.get('severity') in ('CRITICAL','MAJOR') and f.get('status') not in ('CLOSED','REMEDIATED'): errors.append(f"PRO-003 release-blocking professional finding open: {f.get('finding_id')}")
    return errors

def validate_defect_register(record):
    d=_load(record); errors=[]
    for f in d.get('defects',[]):
        if f.get('severity') in ('CRITICAL','MAJOR') and f.get('status') not in ('CLOSED','NOT_A_DEFECT','DUPLICATE'):
            errors.append(f"DEFECT-OPEN release-blocking defect: {f.get('defect_id')}")
        if f.get('status')=='CLOSED' and not f.get('regression_test'): errors.append(f"DEFECT-REG closed defect lacks regression coverage: {f.get('defect_id')}")
    return errors

RC_REQUIREMENTS=[f'RC-{i:02d}' for i in range(1,25)]
def validate_release_candidate(record):
    d=_load(record); errors=[]; req=d.get('requirements',{})
    for key in RC_REQUIREMENTS:
        if req.get(key)!='PASS': errors.append(f'RC-GATE {key} not PASS')
    if d.get('professional_review_status')!='COMPLETE': errors.append('RC-GATE professional review incomplete')
    if d.get('human_release_approval') is not True or not d.get('approved_by') or str(d.get('approved_by')).strip().upper() in {'AI','CODEX','CLAUDE','ASSISTANT'}:
        errors.append('RC-GATE human release approval missing/self-approved')
    return errors
