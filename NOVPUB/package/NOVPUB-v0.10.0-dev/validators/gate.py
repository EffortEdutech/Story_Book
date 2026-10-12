def validate_gate_record(record: dict, human_required: bool = False):
    errors=[]
    status=record.get('status')
    evidence=record.get('evidence') or []
    if status == 'PASS' and not evidence:
        errors.append('GATEVAL-002 PASS without evidence')
    if human_required and status == 'PASS' and not record.get('approved_by'):
        errors.append('GATEVAL-003 human approval missing')
    if status == 'PASS' and record.get('approved_by') == 'AI':
        errors.append('GATEVAL-003 agent cannot self-approve human gate')
    return errors
