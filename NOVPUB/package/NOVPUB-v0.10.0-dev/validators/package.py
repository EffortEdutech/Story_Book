import json
from pathlib import Path


def validate_package(package_root):
    root = Path(package_root)
    errors = []
    manifest = json.loads((root / 'MANIFEST.json').read_text(encoding='utf-8'))
    registry = json.loads((root / 'registry/skill_registry.json').read_text(encoding='utf-8'))
    skills = registry.get('skills', [])
    ids = [s['skill_id'] for s in skills]
    if len(ids) != 96 or len(set(ids)) != 96:
        errors.append('PKG-001 skill registry must contain 96 unique skills')
    implemented = set(manifest.get('implemented_skills', []))
    registry_implemented = {s['skill_id'] for s in skills if s.get('implementation_status') == 'implemented'}
    if implemented != registry_implemented:
        errors.append('PKG-005 manifest/registry implemented skill mismatch')
    for skill in skills:
        if skill.get('implementation_status') == 'implemented' and not (root / skill['skill_file']).exists():
            errors.append(f"PKG-002 implemented skill file missing: {skill['skill_id']}")
    for rel in ['SKILL.md', 'README.md', 'MANIFEST.json', 'registry/gate_registry.json',
                'registry/state_registry.json', 'registry/artefact_registry.json', 'registry/validator_registry.json']:
        if not (root / rel).exists():
            errors.append(f'PKG-003 required package file missing: {rel}')
    for schema in (root / 'schemas').glob('*.json'):
        try:
            json.loads(schema.read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f'PKG-004 invalid JSON schema file {schema.name}: {exc}')
    for phase in manifest.get('implemented_phases', []):
        if not (root / f'workflows/phase{phase}.yaml').exists():
            errors.append(f'PKG-006 workflow missing for implemented phase {phase}')
    return errors
