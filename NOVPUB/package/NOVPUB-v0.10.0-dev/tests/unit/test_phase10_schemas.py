import json, unittest
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parents[2]; FX=ROOT/'tests/fixtures/phase10'
class Phase10SchemaTests(unittest.TestCase):
    def test_clean_fixtures(self):
        pairs=[('pilot_project_clean.json','pilot_project.schema.json'),('baseline_clean.json','real_manuscript_baseline.schema.json'),('evidence_matrix_clean.json','pilot_evidence_matrix.schema.json'),('phase1_4_clean.json','phase1_4_pilot.schema.json'),('kdp_pilot_clean.json','kdp_pilot.schema.json'),('ingram_pilot_clean.json','ingram_pilot.schema.json'),('proof_launch_clean.json','proof_launch_pilot.schema.json'),('postpub_clean.json','postpub_pilot.schema.json'),('findings_clean.json','pilot_findings.schema.json'),('real_parity_clean.json','real_pilot_parity.schema.json'),('v1_clean_fixture.json','v1_release_gate.schema.json')]
        for f,s in pairs:
            with self.subTest(f=f): jsonschema.Draft202012Validator(json.loads((ROOT/'schemas'/s).read_text())).validate(json.loads((FX/f).read_text()))
if __name__=='__main__': unittest.main()
