import json, re
from pathlib import Path

HUMAN_BAD={'AI','CODEX','CLAUDE','ASSISTANT','MODEL'}
REAL_EVIDENCE_TYPES={'REAL_FILE','PLATFORM_RECORD','PHYSICAL_PROOF','HUMAN_REVIEW','RECEIPT','LIVE_LISTING','SIGNED_DECISION','ACTUAL_AGENT_RUN'}

def _load(x):
    if isinstance(x,(str,Path)):
        p=Path(x)
        if p.exists(): return json.loads(p.read_text(encoding='utf-8'))
    return x

def _human(name):
    return bool(name) and str(name).strip().upper() not in HUMAN_BAD

def _sha256(v): return bool(re.fullmatch(r'[0-9a-fA-F]{64}',str(v or '')))

def validate_pilot_project(record):
    d=_load(record); e=[]
    if d.get('project_type')!='professional_real_novel_pilot': e.append('PILOT-001 project_type must be professional_real_novel_pilot')
    if d.get('source',{}).get('real_manuscript') is not True: e.append('PILOT-001 real manuscript flag required')
    if not d.get('project_id'): e.append('PILOT-002 project_id missing')
    if not d.get('novpub',{}).get('candidate_version'): e.append('PILOT-002 candidate version missing')
    if d.get('pilot_status') not in {'INITIALIZED','BLOCKED_RC_PENDING','ACTIVE','PASSED','REMEDIATION_REQUIRED'}: e.append('PILOT-001 invalid pilot_status')
    return e

def validate_real_manuscript_baseline(record):
    d=_load(record); e=[]
    if d.get('authoritative_source') is not True: e.append('PILOT-002 authoritative manuscript source not established')
    if not _sha256(d.get('sha256')): e.append('PILOT-002 valid SHA-256 manuscript hash required')
    if d.get('completeness_checked') is not True: e.append('PILOT-002 completeness check required')
    if d.get('partial_export_detected') is True: e.append('PILOT-002 partial manuscript export detected')
    if d.get('human_confirmed_source') is not True or not _human(d.get('confirmed_by')): e.append('PILOT-005 human source confirmation required')
    if d.get('evidence_type') not in REAL_EVIDENCE_TYPES: e.append('PILOT-009 real source evidence required; fixture/simulated evidence not accepted')
    if not d.get('filename') or not d.get('format'): e.append('PILOT-002 source filename/format missing')
    return e

def validate_pilot_evidence_matrix(record):
    d=_load(record); e=[]; rows=d.get('skills',[])
    by={r.get('skill_id'):r for r in rows}
    for i in range(1,77):
        sid=f'NPUB-{i:02d}'; r=by.get(sid)
        if not r: e.append(f'PILOT-002 evidence row missing: {sid}'); continue
        status=r.get('pilot_status')
        if status=='REAL_EXECUTED':
            if not r.get('real_input') or not r.get('real_output') or not r.get('evidence'): e.append(f'PILOT-002 real execution evidence incomplete: {sid}')
            if r.get('validator_pass') is not True: e.append(f'PILOT-004 validator not passed: {sid}')
        elif status=='NOT_APPLICABLE_WITH_JUSTIFICATION':
            if not r.get('justification'): e.append(f'PILOT-002 N/A justification missing: {sid}')
        else: e.append(f'PILOT-001 invalid/unresolved pilot status: {sid}')
    return e

def validate_phase1_4_pilot(record):
    d=_load(record); e=[]; gates=d.get('gates',{})
    for gid in ['GATE-02','GATE-03','GATE-04','GATE-05','GATE-06','GATE-07']:
        g=gates.get(gid,{})
        if g.get('status')!='PASS': e.append(f'PILOT-001 {gid} not PASS')
        if not g.get('evidence'): e.append(f'PILOT-002 {gid} real evidence missing')
        if g.get('human_required') and not _human(g.get('approved_by')): e.append(f'PILOT-005 {gid} human approval missing/self-approved')
    return e

def validate_kdp_pilot(record):
    d=_load(record); e=[]; levels={'K1':1,'K2':2,'K3':3,'K4':4}; level=d.get('level')
    if level not in levels: e.append('PILOT-007 invalid KDP pilot level'); return e
    if d.get('package_validated') is not True: e.append('PILOT-007 KDP package not validated')
    if not d.get('real_evidence'): e.append('PILOT-009 KDP real evidence missing')
    if levels[level]>=2 and d.get('draft_validated') is not True: e.append('PILOT-007 KDP draft evidence required')
    if levels[level]>=3:
        if d.get('physical_proof_required') and d.get('physical_proof_approved') is not True: e.append('PILOT-006 required KDP physical proof not approved')
        if d.get('physical_proof_required') and not _human(d.get('proof_approved_by')): e.append('PILOT-005 KDP physical proof requires human approval')
    if levels[level]>=4 and d.get('verified_live') is not True: e.append('PILOT-007 KDP live verification missing')
    if d.get('publication_authorized') and not _human(d.get('publication_authorized_by')): e.append('PILOT-005 KDP publication self-authorization prohibited')
    return e

def validate_ingram_pilot(record):
    d=_load(record); e=[]; levels={'I1':1,'I2':2,'I3':3,'I4':4,'I5':5}; level=d.get('level')
    if level not in levels: e.append('PILOT-007 invalid Ingram pilot level'); return e
    if d.get('package_validated') is not True: e.append('PILOT-007 Ingram package not validated')
    if not d.get('real_evidence'): e.append('PILOT-009 Ingram real evidence missing')
    if levels[level]>=2 and d.get('title_draft_validated') is not True: e.append('PILOT-007 Ingram title draft evidence required')
    if levels[level]>=3 and d.get('eproof_approved') is not True: e.append('PILOT-007 Ingram eProof approval required')
    if levels[level]>=4:
        if d.get('physical_proof_approved') is not True: e.append('PILOT-006 Ingram physical proof not approved')
        if not _human(d.get('proof_approved_by')): e.append('PILOT-005 Ingram physical proof requires human approval')
    if levels[level]>=5 and d.get('distribution_verified') is not True: e.append('PILOT-007 Ingram distribution verification missing')
    if d.get('distribution_authorized') and not _human(d.get('distribution_authorized_by')): e.append('PILOT-005 Ingram distribution self-authorization prohibited')
    if d.get('same_paperback_edition') and d.get('publisher_owned_isbn') is not True: e.append('PILOT-007 shared KDP/Ingram paperback requires publisher-owned ISBN')
    if d.get('same_paperback_edition') and d.get('kdp_expanded_distribution') is not False: e.append('PILOT-007 KDP Expanded Distribution conflict')
    return e

def validate_proof_launch_pilot(record):
    d=_load(record); e=[]
    g8=d.get('gate_08',{})
    if g8.get('status')=='PASS':
        if g8.get('evidence_type')!='PHYSICAL_PROOF': e.append('PILOT-006 GATE-08 PASS requires physical proof evidence')
        if not _human(g8.get('approved_by')): e.append('PILOT-005 GATE-08 requires human proof approval')
    if d.get('launch_dry_run') is not True: e.append('PILOT-002 real launch dry-run not completed')
    g9=d.get('gate_09',{})
    if g9.get('status')=='PASS' and not _human(g9.get('approved_by')): e.append('PILOT-005 GATE-09 requires human launch authorization')
    if g9.get('status')=='PASS' and not g9.get('evidence'): e.append('PILOT-002 GATE-09 evidence missing')
    return e

def validate_postpub_pilot(record):
    d=_load(record); e=[]
    required=['sales_ledger','royalty_ledger','returns_register','errata_register','feedback_register','legal_deposit_status','publication_archive']
    for key in required:
        if d.get('controls',{}).get(key) not in {'INSTANTIATED','ACTIVE','PENDING_REAL_DATA','NOT_APPLICABLE'}: e.append(f'PILOT-002 governance control not instantiated: {key}')
    if d.get('legal_deposit',{}).get('status') in {'SUBMITTED','ACKNOWLEDGED','CLOSED'} and not d.get('legal_deposit',{}).get('evidence'): e.append('PILOT-009 legal deposit status claims real completion without evidence')
    if d.get('gate_10',{}).get('status')=='PASS':
        if not d.get('gate_10',{}).get('evidence'): e.append('PILOT-002 GATE-10 evidence missing')
        if not _human(d.get('gate_10',{}).get('approved_by')): e.append('PILOT-005 GATE-10 human approval missing')
    return e

def validate_pilot_defects(record):
    d=_load(record); e=[]
    for f in d.get('findings',[]):
        sev=f.get('severity'); st=f.get('status')
        if sev=='CRITICAL' and st not in {'CLOSED','REMEDIATED','NOT_A_DEFECT','DUPLICATE'}: e.append(f"PILOT-001 unresolved CRITICAL finding: {f.get('pilot_finding_id')}")
        if sev=='MAJOR' and f.get('release_blocking',True) and st not in {'CLOSED','REMEDIATED','NOT_A_DEFECT','DUPLICATE'}: e.append(f"PILOT-001 unresolved release-blocking MAJOR finding: {f.get('pilot_finding_id')}")
        if st in {'CLOSED','REMEDIATED'} and not f.get('regression_test'): e.append(f"PILOT-010 remediated finding lacks regression test: {f.get('pilot_finding_id')}")
        if st in {'CLOSED','REMEDIATED'} and not f.get('root_cause'): e.append(f"PILOT-010 remediated finding lacks root cause: {f.get('pilot_finding_id')}")
    return e

def validate_real_pilot_parity(record):
    d=_load(record); e=[]
    if d.get('codex_run',{}).get('evidence_type')!='ACTUAL_AGENT_RUN': e.append('PILOT-008 actual Codex run evidence missing')
    if d.get('claude_run',{}).get('evidence_type')!='ACTUAL_AGENT_RUN': e.append('PILOT-008 actual Claude run evidence missing')
    for c in d.get('comparisons',[]):
        if c.get('deterministic') and c.get('equivalent') is not True: e.append(f"PILOT-008 deterministic agent divergence: {c.get('check_id')}")
        if c.get('material_difference') and not c.get('resolution'): e.append(f"PILOT-008 unresolved material divergence: {c.get('check_id')}")
    return e

V1_REQUIREMENTS=[f'V1-{i:02d}' for i in range(1,31)]
def validate_v1_release(record):
    d=_load(record); e=[]; req=d.get('requirements',{})
    for key in V1_REQUIREMENTS:
        if req.get(key)!='PASS': e.append(f'V1-GATE {key} not PASS')
    if d.get('gate_result')!='PASS': e.append('V1-GATE production release gate not PASS')
    if d.get('professional_human_review')!='COMPLETE': e.append('V1-GATE professional human review incomplete')
    if d.get('real_pilot_status')!='PASSED': e.append('V1-GATE real pilot not passed')
    if d.get('codex_certified') is not True or d.get('claude_certified') is not True: e.append('V1-GATE actual agent certifications incomplete')
    if not _human(d.get('approved_by')) or d.get('human_release_approval') is not True: e.append('V1-GATE human production-release approval missing/self-approved')
    return e
