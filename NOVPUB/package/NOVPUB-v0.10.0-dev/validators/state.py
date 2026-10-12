import json
from pathlib import Path

ALLOWED_GATE_STATUS = {'PENDING','PASS','FAIL','CONDITIONAL','NOT_APPLICABLE'}

def load_registry(package_root: Path):
    return json.loads((package_root/'registry/state_registry.json').read_text(encoding='utf-8'))

def validate_state(state_path, package_root):
    state = json.loads(Path(state_path).read_text(encoding='utf-8'))
    registry = load_registry(Path(package_root))
    errors=[]
    if state.get('current_state') not in set(registry['states']):
        errors.append('STATE-001 current_state is not registered')
    phase=state.get('current_phase')
    if not isinstance(phase,int) or not (1 <= phase <= 10):
        errors.append('STATE-002 current_phase must be 1..10')
    for gate,status in state.get('gates',{}).items():
        if status not in ALLOWED_GATE_STATUS:
            errors.append(f'STATE-003 invalid gate status for {gate}: {status}')
    return errors
