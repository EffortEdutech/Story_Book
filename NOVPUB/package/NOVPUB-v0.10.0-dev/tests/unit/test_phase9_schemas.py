import json, unittest
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parents[2]; FX=ROOT/'tests/fixtures/phase9'
class Phase9SchemaTests(unittest.TestCase):
    def test_phase9_clean_fixtures_validate(self):
        pairs=[('fixture_manifest_clean.json','fixture_manifest.schema.json'),('attack_catalog_clean.json','adversarial_catalog.schema.json'),('agent_parity_clean.json','agent_parity.schema.json'),('rc_clean_fixture.json','release_candidate.schema.json')]
        for fixture,schema in pairs:
            with self.subTest(fixture=fixture):
                instance=json.loads((FX/fixture).read_text()); sc=json.loads((ROOT/'schemas'/schema).read_text()); jsonschema.Draft202012Validator(sc).validate(instance)
if __name__=='__main__': unittest.main()
