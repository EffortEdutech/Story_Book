import json
from pathlib import Path

PLACEHOLDER_TERMS = ['TODO','TBD','FIXME','[INSERT','[AUTHOR NOTE','[EDITOR NOTE']

def validate_chapter_manifest(path):
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    chapters=data.get('chapters',[])
    errors=[]
    ids=[c.get('chapter_id') for c in chapters]
    if len(ids) != len(set(ids)):
        errors.append('STRUCT-002 duplicate chapter_id')
    orders=[c.get('order') for c in chapters]
    if orders and sorted(orders) != list(range(1, len(orders)+1)):
        errors.append('STRUCT-006 broken chapter sequence')
    if any(c.get('word_count',0)==0 for c in chapters):
        errors.append('STRUCT-003 empty chapter')
    return errors

def find_placeholders(text):
    upper=text.upper()
    return [term for term in PLACEHOLDER_TERMS if term.upper() in upper]

def validate_editorial_gate(approval, unresolved_queries=None):
    errors=[]
    if approval.get('unresolved_blocking_issues',0) != 0:
        errors.append('G02 unresolved blocking issues')
    if approval.get('structural_audit') != 'passed':
        errors.append('G02 structural audit not passed')
    if approval.get('continuity_audit') != 'passed':
        errors.append('G02 continuity audit not passed')
    if approval.get('copyedit') != 'complete':
        errors.append('G02 copyedit incomplete')
    if approval.get('proofread') != 'complete':
        errors.append('G02 proofread incomplete')
    if approval.get('status') == 'EDITORIAL_APPROVED' and not approval.get('human_approval'):
        errors.append('G02 human approval missing')
    if unresolved_queries:
        blocking=[q for q in unresolved_queries if q.get('blocking') and q.get('status')=='open']
        if blocking:
            errors.append('G02 blocking author queries unresolved')
    return errors
