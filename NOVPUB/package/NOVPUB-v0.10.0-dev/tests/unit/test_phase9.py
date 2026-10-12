import json, unittest
from pathlib import Path
from datetime import date
from validators.phase9 import *
ROOT=Path(__file__).resolve().parents[2]; FX=ROOT/'tests/fixtures/phase9'
def load(n): return json.loads((FX/n).read_text())
class Phase9Tests(unittest.TestCase):
    def test_registry(self): self.assertEqual([],validate_registry_integrity(ROOT))
    def test_gate_clean(self): self.assertEqual([],validate_gate_evidence(load('gate_clean.json')))
    def test_gate_evidence_required(self): self.assertTrue(any('GATEVAL-002' in x for x in validate_gate_evidence(load('gate_no_evidence.json'))))
    def test_gate_human(self): self.assertTrue(any('GATEVAL-003' in x for x in validate_gate_evidence(load('gate_ai_approval.json'))))
    def test_transition_blocks_rc_without_gate(self): self.assertTrue(validate_major_transition('PUBLICATION_GOVERNED','NOVPUB_V1_RC_APPROVED',{'GATE-NOVPUB-RC1':'PENDING'}))
    def test_transition_allows_rc(self): self.assertEqual([],validate_major_transition('PUBLICATION_GOVERNED','NOVPUB_V1_RC_APPROVED',{'GATE-NOVPUB-RC1':'PASS'}))
    def test_determinism_clean(self): self.assertEqual([],validate_determinism_runs(load('determinism_clean.json')))
    def test_determinism_bad(self): self.assertTrue(any('DET-001' in x for x in validate_determinism_runs(load('determinism_bad.json'))))
    def test_parity_clean(self): self.assertEqual([],validate_parity_results(load('parity_clean.json')))
    def test_parity_bad(self): self.assertTrue(validate_parity_results(load('parity_bad.json')))
    def test_provenance_clean(self): self.assertEqual([],validate_provenance_chain(load('provenance_clean.json')))
    def test_provenance_cycle(self): self.assertTrue(validate_provenance_chain(load('provenance_cycle.json')))
    def test_rule_current(self): self.assertEqual([],validate_rule_freshness_result(load('rule_current.json'),date(2026,10,10)))
    def test_rule_stale(self): self.assertTrue(any('RULE-001' in x for x in validate_rule_freshness_result(load('rule_stale.json'),date(2026,10,10))))
    def test_fixture_manifest(self): self.assertEqual([],validate_fixture_manifest(load('fixture_manifest_clean.json')))
    def test_attack_catalog(self): self.assertEqual([],validate_adversarial_catalog(load('attack_catalog_clean.json')))
    def test_attack_count(self): self.assertEqual(160,len(load('attack_catalog_clean.json')['attacks']))
    def test_agent_parity_clean(self): self.assertEqual([],validate_agent_parity(load('agent_parity_clean.json')))
    def test_agent_parity_bad(self): self.assertGreaterEqual(len(validate_agent_parity(load('agent_parity_bad.json'))),2)
    def test_professional_review_clean_fixture(self): self.assertEqual([],validate_professional_review(load('pro_review_clean_fixture.json')))
    def test_professional_review_fake(self): self.assertTrue(validate_professional_review(load('pro_review_fake.json')))
    def test_defects_clean(self): self.assertEqual([],validate_defect_register(load('defects_clean.json')))
    def test_defects_bad(self): self.assertTrue(validate_defect_register(load('defects_bad.json')))
    def test_rc_fixture(self): self.assertEqual([],validate_release_candidate(load('rc_clean_fixture.json')))
    def test_rc_bad(self): self.assertTrue(validate_release_candidate(load('rc_bad.json')))
    def test_package_live_rc_is_pending(self):
        d=json.loads((ROOT/'validation/12_RELEASE/release_candidate.json').read_text()); self.assertEqual('PENDING',d['gate_result']); self.assertNotEqual([],validate_release_candidate(d))
if __name__=='__main__': unittest.main()
