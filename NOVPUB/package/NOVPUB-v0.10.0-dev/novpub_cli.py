#!/usr/bin/env python3
import argparse, json, sys
from datetime import datetime, timezone
from pathlib import Path
from validators.state import validate_state
from validators.isbn import validate_isbn13, normalize_isbn13
from validators.phase3 import preflight_pdf, validate_epub_file
from validators.phase4 import calculate_kdp_print_royalty, calculate_kdp_ebook_royalty, calculate_ingram_compensation
from validators.phase5 import validate_kdp_select, validate_expanded_distribution, validate_kdp_metadata
from validators.phase6 import validate_ingram_isbn_reconciliation, validate_kdp_ingram_coexistence, validate_ingram_return_policy, validate_ingram_eproof, validate_ingram_physical_proof, validate_ingram_metadata
from validators.phase7 import validate_reviewer_outreach, validate_marketing_claims, validate_launch_calendar, validate_launch_authorization
from validators.phase8 import validate_sales_records, validate_financial_reconciliation, validate_select_lifecycle, validate_revision_classification, validate_return_exposure, validate_legal_deposit, validate_publication_manifest, validate_gate10, legal_deposit_deadline
from validators.phase9 import validate_registry_integrity, validate_adversarial_catalog, validate_agent_parity, validate_professional_review, validate_release_candidate
from validators.phase10 import validate_pilot_project, validate_real_manuscript_baseline, validate_pilot_evidence_matrix, validate_phase1_4_pilot, validate_kdp_pilot, validate_ingram_pilot, validate_proof_launch_pilot, validate_postpub_pilot, validate_pilot_defects, validate_real_pilot_parity, validate_v1_release

PACKAGE_ROOT=Path(__file__).resolve().parent
PACKAGE_VERSION=json.loads((PACKAGE_ROOT/'MANIFEST.json').read_text(encoding='utf-8'))['version']

def now():
    return datetime.now(timezone.utc).isoformat()

def write_json(path,obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def init_project(target, project_id):
    target=Path(target)
    target.mkdir(parents=True,exist_ok=True)
    dirs=['00_PROJECT_CONTROL','01_SOURCE','02_EDITORIAL/00_INTAKE','02_EDITORIAL/01_FREEZE','02_EDITORIAL/02_STRUCTURE','02_EDITORIAL/03_CONTINUITY','02_EDITORIAL/04_STYLE','02_EDITORIAL/05_COPYEDIT','02_EDITORIAL/06_PROOFREAD','02_EDITORIAL/07_RECONCILIATION','02_EDITORIAL/08_APPROVED','03_RIGHTS/00_RIGHTS_AUDIT','03_RIGHTS/01_THIRD_PARTY','03_RIGHTS/01_THIRD_PARTY/permissions','03_RIGHTS/02_AUTHOR_IDENTITY','03_RIGHTS/03_PUBLISHER','04_ISBN_PUBLISHER/04_EDITIONS','04_ISBN_PUBLISHER/05_ISBN/isbn_evidence','04_ISBN_PUBLISHER/06_PNM/isbn_application_pack','04_ISBN_PUBLISHER/06_PNM/pdp_application_pack','04_ISBN_PUBLISHER/07_COPYRIGHT_PAGE','05_PRODUCTION/00_CANONICAL','05_PRODUCTION/01_FORMAT_STRATEGY','05_PRODUCTION/02_TRIM','05_PRODUCTION/03_TYPOGRAPHY','05_PRODUCTION/04_PAGE_ARCHITECTURE','05_PRODUCTION/05_TYPESETTING','05_PRODUCTION/06_PREFLIGHT','05_PRODUCTION/07_EPUB/source','05_PRODUCTION/08_COVER/assets','05_PRODUCTION/08_COVER/templates','05_PRODUCTION/08_COVER/masters','05_PRODUCTION/08_COVER/channel_outputs','05_PRODUCTION/09_COVER_QA','05_PRODUCTION/11_APPROVAL','06_METADATA/00_MASTER','06_METADATA/01_POSITIONING','06_METADATA/02_CLASSIFICATION','06_METADATA/03_KEYWORDS','06_METADATA/04_DESCRIPTIONS','06_METADATA/05_AUTHOR','06_METADATA/06_PRICING','06_METADATA/07_WHOLESALE','06_METADATA/08_TERRITORIES','06_METADATA/09_RELEASE','06_METADATA/10_CHANNEL_MAPS','06_METADATA/11_APPROVAL','07_KDP/00_RULES','07_KDP/01_ACCOUNT','07_KDP/02_KINDLE/kindle_files','07_KDP/03_PAPERBACK/paperback_files','07_KDP/04_HARDCOVER/hardcover_files','07_KDP/05_SELECT','07_KDP/06_EXPANDED_DISTRIBUTION','07_KDP/07_PROOFS','07_KDP/08_SUBMISSION/submission_receipts','07_KDP/09_LIVE_QA','07_KDP/10_COMPLETION','08_INGRAMSPARK/00_RULES','08_INGRAMSPARK/01_ACCOUNT','08_INGRAMSPARK/02_METADATA','08_INGRAMSPARK/03_PRINT_CONFIGURATION','08_INGRAMSPARK/04_ISBN','08_INGRAMSPARK/05_FILES/interiors','08_INGRAMSPARK/05_FILES/covers','08_INGRAMSPARK/06_PRICING','08_INGRAMSPARK/07_RETURNS','08_INGRAMSPARK/08_EPROOF','08_INGRAMSPARK/09_PHYSICAL_PROOF','08_INGRAMSPARK/10_DISTRIBUTION','08_INGRAMSPARK/11_LIVE_QA','08_INGRAMSPARK/12_COMPLETION','09_PROOFS','10_LAUNCH/00_STRATEGY','10_LAUNCH/01_ARC/arc_files','10_LAUNCH/02_REVIEWERS','10_LAUNCH/03_LAUNCH_TEAM','10_LAUNCH/04_AUTHOR_CENTRAL','10_LAUNCH/05_WEBSITE','10_LAUNCH/06_MEDIA_KIT/author_bio','10_LAUNCH/06_MEDIA_KIT/book_factsheet','10_LAUNCH/06_MEDIA_KIT/press_release','10_LAUNCH/06_MEDIA_KIT/media_pitch','10_LAUNCH/06_MEDIA_KIT/interview_topics','10_LAUNCH/06_MEDIA_KIT/approved_images','10_LAUNCH/07_CAMPAIGN_CONTENT/social','10_LAUNCH/07_CAMPAIGN_CONTENT/email','10_LAUNCH/07_CAMPAIGN_CONTENT/graphics','10_LAUNCH/07_CAMPAIGN_CONTENT/excerpts','10_LAUNCH/07_CAMPAIGN_CONTENT/quote_cards','10_LAUNCH/08_CALENDAR','10_LAUNCH/09_LAUNCH_DAY','10_LAUNCH/10_ANALYTICS','10_LAUNCH/11_APPROVAL','11_PNM_COMPLIANCE','12_POST_PUBLICATION/00_STATE','12_POST_PUBLICATION/01_SALES/raw_reports','12_POST_PUBLICATION/02_ROYALTIES','12_POST_PUBLICATION/03_KDP_SELECT','12_POST_PUBLICATION/04_OPTIMIZATION','12_POST_PUBLICATION/05_ERRATA','12_POST_PUBLICATION/06_EDITION_CONTROL','12_POST_PUBLICATION/07_INGRAM_OPERATIONS','12_POST_PUBLICATION/08_READER_INTELLIGENCE','12_POST_PUBLICATION/09_MALAYSIA_COMPLIANCE/deposit_evidence','12_POST_PUBLICATION/10_RIGHTS_EXPANSION','12_POST_PUBLICATION/11_ARCHIVE/asset_archive','12_POST_PUBLICATION/12_GOVERNANCE','validation/00_REGISTRY','validation/01_SCHEMAS','validation/02_STATIC','validation/03_GATES','validation/04_DETERMINISTIC','validation/05_PARITY','validation/06_RULES','validation/07_FIXTURES','validation/08_ADVERSARIAL/results','validation/08_ADVERSARIAL/prompt_injection_tests','validation/08_ADVERSARIAL/unsafe_action_tests','validation/09_AGENT_PARITY/codex_runs','validation/09_AGENT_PARITY/claude_runs','validation/10_PROFESSIONAL_REVIEW/review_pack','validation/10_PROFESSIONAL_REVIEW/reviewer_notes','validation/11_REMEDIATION','validation/12_RELEASE','13_PILOT_FINDINGS','14_AGENT_PARITY/codex_runs','14_AGENT_PARITY/claude_runs','15_RELEASE_EVIDENCE','validation/13_PILOT','99_ARCHIVE']
    for d in dirs:(target/d).mkdir(parents=True,exist_ok=True)
    if not (target/'project_manifest.json').exists():
        write_json(target/'project_manifest.json',{'project_id':project_id,'package':'NOVPUB','package_version':PACKAGE_VERSION,'created_at':now(),'timezone':'Asia/Kuala_Lumpur','current_phase':1,'title':None,'author_display_name':None,'channels':{'kdp':True,'ingramspark':True}})
    if not (target/'publishing_state.json').exists():
        gates={g['gate_id']:'PENDING' for g in json.loads((PACKAGE_ROOT/'registry/gate_registry.json').read_text())['gates']}
        write_json(target/'publishing_state.json',{'project_id':project_id,'package_version':PACKAGE_VERSION,'current_phase':1,'current_state':'MANUSCRIPT_COMPLETE','gates':gates,'blocking_issues':[],'human_decisions_required':[],'updated_at':now()})
    for name,obj in [('issue_register.json',{'issues':[]}),('approval_register.json',{'approvals':[]}),('artifact_manifest.json',{'artifacts':[]})]:
        if not (target/name).exists(): write_json(target/name,obj)
    (target/'decision_log.jsonl').touch(exist_ok=True)
    print(f'Initialized NOVPUB project: {target}')

def init_pilot(target, project_id):
    init_project(target, project_id)
    t=Path(target)
    manifest=json.loads((t/'project_manifest.json').read_text())
    manifest.update({'project_type':'professional_real_novel_pilot','source':{'real_manuscript':False},'novpub':{'candidate_version':'NOVPUB-v1.0.0-RC'},'pilot_status':'BLOCKED_RC_PENDING'})
    write_json(t/'project_manifest.json',manifest)
    write_json(t/'pilot_evidence_matrix.json',{'skills':[{'skill_id':f'NPUB-{i:02d}','pilot_status':'PENDING_REAL_EVIDENCE'} for i in range(1,77)]})
    write_json(t/'pilot_findings.json',{'findings':[]})
    write_json(t/'pilot_decision_register.json',{'decisions':[]})
    write_json(t/'14_AGENT_PARITY/real_pilot_parity_report.json',{'codex_run':{'evidence_type':'PENDING'},'claude_run':{'evidence_type':'PENDING'},'comparisons':[]})
    write_json(t/'15_RELEASE_EVIDENCE/v1_release_gate.json',{'requirements':{f'V1-{i:02d}':'PENDING' for i in range(1,31)},'gate_result':'PENDING','professional_human_review':'PENDING','real_pilot_status':'PENDING','codex_certified':False,'claude_certified':False,'human_release_approval':False,'approved_by':None})
    print(f'Initialized NOVPUB real-pilot workspace: {t}')

def status(target):
    t=Path(target); state=json.loads((t/'publishing_state.json').read_text())
    print(json.dumps({'project_id':state.get('project_id'),'phase':state.get('current_phase'),'state':state.get('current_state'),'blocking_issues':state.get('blocking_issues',[]),'human_decisions_required':state.get('human_decisions_required',[]),'passed_gates':[k for k,v in state.get('gates',{}).items() if v=='PASS']},indent=2))

def main():
    p=argparse.ArgumentParser(prog='novpub')
    sub=p.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('init'); a.add_argument('target'); a.add_argument('--project-id',default='NOVPUB-PROJECT-001')
    a=sub.add_parser('init-pilot'); a.add_argument('target'); a.add_argument('--project-id',default='NOVPUB-PILOT-001')
    a=sub.add_parser('status'); a.add_argument('target')
    a=sub.add_parser('validate-state'); a.add_argument('target')
    a=sub.add_parser('check-isbn'); a.add_argument('isbn')
    a=sub.add_parser('preflight-pdf'); a.add_argument('pdf'); a.add_argument('--width',type=float); a.add_argument('--height',type=float); a.add_argument('--pages',type=int)
    a=sub.add_parser('validate-epub'); a.add_argument('epub')
    a=sub.add_parser('calc-kdp-print'); a.add_argument('price',type=float); a.add_argument('print_cost',type=float); a.add_argument('rate',type=float)
    a=sub.add_parser('calc-kdp-ebook'); a.add_argument('price',type=float); a.add_argument('rate',type=float); a.add_argument('--delivery-cost',type=float,default=0)
    a=sub.add_parser('calc-ingram'); a.add_argument('price',type=float); a.add_argument('discount',type=float); a.add_argument('print_cost',type=float); a.add_argument('--other-charges',type=float,default=0)
    a=sub.add_parser('validate-kdp-select'); a.add_argument('json_file')
    a=sub.add_parser('validate-expanded-distribution'); a.add_argument('json_file')
    a=sub.add_parser('validate-kdp-metadata'); a.add_argument('json_file')
    a=sub.add_parser('validate-ingram-isbn'); a.add_argument('json_file')
    a=sub.add_parser('validate-ingram-coexistence'); a.add_argument('json_file')
    a=sub.add_parser('validate-ingram-returns'); a.add_argument('json_file')
    a=sub.add_parser('validate-ingram-eproof'); a.add_argument('json_file')
    a=sub.add_parser('validate-ingram-proof'); a.add_argument('json_file')
    a=sub.add_parser('validate-ingram-metadata'); a.add_argument('json_file')
    a=sub.add_parser('validate-launch-review-outreach'); a.add_argument('json_file')
    a=sub.add_parser('validate-marketing-claims'); a.add_argument('json_file')
    a=sub.add_parser('validate-launch-calendar'); a.add_argument('json_file'); a.add_argument('--live-listing-ready',action='store_true')
    a=sub.add_parser('validate-launch-authorization'); a.add_argument('json_file')
    a=sub.add_parser('validate-postpub-sales'); a.add_argument('json_file')
    a=sub.add_parser('validate-postpub-reconciliation'); a.add_argument('json_file')
    a=sub.add_parser('validate-select-lifecycle'); a.add_argument('json_file')
    a=sub.add_parser('validate-revision'); a.add_argument('json_file')
    a=sub.add_parser('validate-return-exposure'); a.add_argument('json_file')
    a=sub.add_parser('validate-legal-deposit'); a.add_argument('json_file'); a.add_argument('--date')
    a=sub.add_parser('legal-deposit-deadline'); a.add_argument('publication_date'); a.add_argument('material_type',choices=['PRINTED','NON_PRINTED'])
    a=sub.add_parser('validate-publication-archive'); a.add_argument('json_file')
    a=sub.add_parser('validate-phase9-package')
    a=sub.add_parser('validate-adversarial-catalog'); a.add_argument('json_file')
    a=sub.add_parser('validate-agent-parity'); a.add_argument('json_file')
    a=sub.add_parser('validate-professional-review'); a.add_argument('json_file')
    a=sub.add_parser('validate-release-candidate'); a.add_argument('json_file')
    a=sub.add_parser('validate-pilot-project'); a.add_argument('json_file')
    a=sub.add_parser('validate-real-baseline'); a.add_argument('json_file')
    a=sub.add_parser('validate-pilot-evidence'); a.add_argument('json_file')
    a=sub.add_parser('validate-phase1-4-pilot'); a.add_argument('json_file')
    a=sub.add_parser('validate-kdp-pilot'); a.add_argument('json_file')
    a=sub.add_parser('validate-ingram-pilot'); a.add_argument('json_file')
    a=sub.add_parser('validate-proof-launch-pilot'); a.add_argument('json_file')
    a=sub.add_parser('validate-postpub-pilot'); a.add_argument('json_file')
    a=sub.add_parser('validate-pilot-findings'); a.add_argument('json_file')
    a=sub.add_parser('validate-real-pilot-parity'); a.add_argument('json_file')
    a=sub.add_parser('validate-v1-release'); a.add_argument('json_file')
    args=p.parse_args()
    if args.cmd=='init': init_project(args.target,args.project_id)
    elif args.cmd=='init-pilot': init_pilot(args.target,args.project_id)
    elif args.cmd=='status': status(args.target)
    elif args.cmd=='validate-state':
        errs=validate_state(Path(args.target)/'publishing_state.json',PACKAGE_ROOT)
        print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='check-isbn':
        digits=normalize_isbn13(args.isbn); ok=validate_isbn13(args.isbn)
        print(json.dumps({'isbn':digits,'valid':ok},indent=2)); sys.exit(0 if ok else 1)
    elif args.cmd=='preflight-pdf':
        result=preflight_pdf(args.pdf,args.width,args.height,args.pages); print(json.dumps(result,indent=2)); sys.exit(0 if result.get('passed') else 1)
    elif args.cmd=='validate-epub':
        result=validate_epub_file(args.epub); print(json.dumps(result,indent=2)); sys.exit(0 if result.get('passed') else 1)
    elif args.cmd=='calc-kdp-print':
        print(json.dumps({'royalty':str(calculate_kdp_print_royalty(args.price,args.print_cost,args.rate))},indent=2))
    elif args.cmd=='calc-kdp-ebook':
        print(json.dumps({'royalty':str(calculate_kdp_ebook_royalty(args.price,args.rate,args.delivery_cost))},indent=2))
    elif args.cmd=='calc-ingram':
        print(json.dumps({'publisher_compensation':str(calculate_ingram_compensation(args.price,args.discount,args.print_cost,args.other_charges))},indent=2))
    elif args.cmd=='validate-kdp-select':
        errs=validate_kdp_select(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-expanded-distribution':
        errs=validate_expanded_distribution(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-kdp-metadata':
        errs=validate_kdp_metadata(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-ingram-isbn':
        errs=validate_ingram_isbn_reconciliation(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-ingram-coexistence':
        errs=validate_kdp_ingram_coexistence(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-ingram-returns':
        errs=validate_ingram_return_policy(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-ingram-eproof':
        errs=validate_ingram_eproof(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-ingram-proof':
        errs=validate_ingram_physical_proof(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-ingram-metadata':
        errs=validate_ingram_metadata(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-launch-review-outreach':
        errs=validate_reviewer_outreach(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-marketing-claims':
        errs=validate_marketing_claims(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-launch-calendar':
        errs=validate_launch_calendar(args.json_file,args.live_listing_ready); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-launch-authorization':
        errs=validate_launch_authorization(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-postpub-sales':
        errs=validate_sales_records(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-postpub-reconciliation':
        errs=validate_financial_reconciliation(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-select-lifecycle':
        errs=validate_select_lifecycle(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-revision':
        errs=validate_revision_classification(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-return-exposure':
        errs=validate_return_exposure(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-legal-deposit':
        from datetime import date as _date
        d=_date.fromisoformat(args.date) if args.date else None
        errs=validate_legal_deposit(args.json_file,d); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='legal-deposit-deadline':
        print(legal_deposit_deadline(args.publication_date,args.material_type).isoformat())
    elif args.cmd=='validate-publication-archive':
        errs=validate_publication_manifest(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-phase9-package':
        errs=validate_registry_integrity(PACKAGE_ROOT); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-adversarial-catalog':
        errs=validate_adversarial_catalog(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-agent-parity':
        errs=validate_agent_parity(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-professional-review':
        errs=validate_professional_review(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-release-candidate':
        errs=validate_release_candidate(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-pilot-project':
        errs=validate_pilot_project(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-real-baseline':
        errs=validate_real_manuscript_baseline(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-pilot-evidence':
        errs=validate_pilot_evidence_matrix(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-phase1-4-pilot':
        errs=validate_phase1_4_pilot(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-kdp-pilot':
        errs=validate_kdp_pilot(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-ingram-pilot':
        errs=validate_ingram_pilot(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-proof-launch-pilot':
        errs=validate_proof_launch_pilot(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-postpub-pilot':
        errs=validate_postpub_pilot(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-pilot-findings':
        errs=validate_pilot_defects(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-real-pilot-parity':
        errs=validate_real_pilot_parity(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
    elif args.cmd=='validate-v1-release':
        errs=validate_v1_release(args.json_file); print('PASS' if not errs else '\n'.join(errs)); sys.exit(0 if not errs else 1)
if __name__=='__main__': main()
