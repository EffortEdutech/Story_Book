import json, unittest
from pathlib import Path
from validators.phase10 import *
ROOT=Path(__file__).resolve().parents[2]; FX=ROOT/'tests/fixtures/phase10'
def load(n): return json.loads((FX/n).read_text())
class Phase10Tests(unittest.TestCase):
    def test_project(self): self.assertEqual([],validate_pilot_project(load('pilot_project_clean.json')))
    def test_baseline(self): self.assertEqual([],validate_real_manuscript_baseline(load('baseline_clean.json')))
    def test_baseline_rejects_fake(self): self.assertGreaterEqual(len(validate_real_manuscript_baseline(load('baseline_fake.json'))),2)
    def test_evidence_matrix(self): self.assertEqual([],validate_pilot_evidence_matrix(load('evidence_matrix_clean.json')))
    def test_phase1_4(self): self.assertEqual([],validate_phase1_4_pilot(load('phase1_4_clean.json')))
    def test_kdp(self): self.assertEqual([],validate_kdp_pilot(load('kdp_pilot_clean.json')))
    def test_kdp_proof(self): self.assertTrue(any('PILOT-006' in x for x in validate_kdp_pilot(load('kdp_pilot_bad.json'))))
    def test_ingram(self): self.assertEqual([],validate_ingram_pilot(load('ingram_pilot_clean.json')))
    def test_proof_launch(self): self.assertEqual([],validate_proof_launch_pilot(load('proof_launch_clean.json')))
    def test_postpub(self): self.assertEqual([],validate_postpub_pilot(load('postpub_clean.json')))
    def test_findings(self): self.assertEqual([],validate_pilot_defects(load('findings_clean.json')))
    def test_findings_block(self): self.assertTrue(validate_pilot_defects(load('findings_bad.json')))
    def test_parity(self): self.assertEqual([],validate_real_pilot_parity(load('real_parity_clean.json')))
    def test_parity_bad(self): self.assertGreaterEqual(len(validate_real_pilot_parity(load('real_parity_bad.json'))),2)
    def test_v1_fixture(self): self.assertEqual([],validate_v1_release(load('v1_clean_fixture.json')))
    def test_v1_bad(self): self.assertTrue(validate_v1_release(load('v1_bad.json')))
    def test_live_v1_pending(self):
        d=json.loads((ROOT/'validation/13_PILOT/v1_release_gate.json').read_text()); self.assertEqual('PENDING',d['gate_result']); self.assertTrue(validate_v1_release(d))
if __name__=='__main__': unittest.main()
