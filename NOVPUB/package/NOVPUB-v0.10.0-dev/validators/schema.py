import json
from pathlib import Path

def validate_json(instance_path, schema_path):
    try:
        import jsonschema
    except ImportError as exc:
        raise RuntimeError('Install jsonschema>=4.0 to run JSON Schema validation') from exc
    instance=json.loads(Path(instance_path).read_text(encoding='utf-8'))
    schema=json.loads(Path(schema_path).read_text(encoding='utf-8'))
    jsonschema.Draft202012Validator(schema).validate(instance)
    return True
