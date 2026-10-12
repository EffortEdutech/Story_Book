import json, unittest
from pathlib import Path
from datetime import date
from validators.phase8 import *
ROOT=Path(__file__).resolve().parents[2]; FX=ROOT/'tests/fixtures/phase8'
def load(n): return json.loads((FX/n).read_text())
class Phase8Tests(unittest.TestCase):
    def test_sales_clean(self): self.assertEqual([],validate_sales_records(load('sales_clean.json')))
    def test_sales_duplicate(self): self.assertTrue(any('FIN-004' in x for x in validate_sales_records(load('sales_duplicate.json'))))
    def test_dedup(self): self.assertEqual(1,len(deduplicate_sales_records(load('sales_duplicate.json'))))
    def test_reconciliation_clean(self): self.assertEqual([],validate_financial_reconciliation(load('reconciliation_clean.json')))
    def test_reconciliation_bad(self): self.assertTrue(any('FIN-007' in x for x in validate_financial_reconciliation(load('reconciliation_bad.json'))))
    def test_payment(self): self.assertEqual([],validate_payment_record(load('payment_clean.json')))
    def test_select_clean(self): self.assertEqual([],validate_select_lifecycle(load('select_clean.json'),date(2026,10,10)))
    def test_select_conflict(self): self.assertTrue(any('SEL-003' in x for x in validate_select_lifecycle(load('select_conflict.json'),date(2026,10,10))))
    def test_opt_clean(self): self.assertEqual([],validate_optimization(load('optimization_clean.json')))
    def test_opt_identity(self): self.assertTrue(any('OPT-004' in x for x in validate_optimization(load('optimization_identity_bad.json'))))
    def test_classify(self):
        self.assertEqual('R1_MINOR_CORRECTION',classify_revision({'minor_typo':True}))
        self.assertEqual('R3_NEW_EDITION',classify_revision({'new_ending':True}))
        self.assertEqual('R4_NEW_FORMAT',classify_revision({'new_format':True}))
    def test_revision_minor(self): self.assertEqual([],validate_revision_classification(load('revision_minor.json')))
    def test_revision_bad(self): self.assertTrue(validate_revision_classification(load('revision_new_edition_bad.json')))
    def test_erratum(self): self.assertEqual([],validate_erratum(load('erratum_clean.json')))
    def test_return_exposure(self): self.assertEqual([],validate_return_exposure(load('return_exposure_clean.json')))
    def test_return_tail_short(self): self.assertTrue(any('INGOPS-003' in x for x in validate_return_exposure(load('return_exposure_short.json'))))
    def test_return_record(self): self.assertEqual([],validate_return_record(load('return_record_clean.json')))
    def test_feedback_preference(self): self.assertEqual([],validate_feedback(load('feedback_preference.json')))
    def test_feedback_defect(self): self.assertEqual([],validate_feedback(load('feedback_defect.json')))
    def test_deadline_print(self): self.assertEqual(date(2026,10,15),legal_deposit_deadline('2026-09-15','PRINTED'))
    def test_deadline_nonprint(self): self.assertEqual(date(2027,9,15),legal_deposit_deadline('2026-09-15','NON_PRINTED'))
    def test_deposit_clean(self): self.assertEqual([],validate_legal_deposit(load('deposit_print_clean.json'),date(2026,10,10)))
    def test_deposit_overdue(self): self.assertTrue(any('MYCOMP-004' in x for x in validate_legal_deposit(load('deposit_print_overdue.json'),date(2026,10,10))))
    def test_rights_opportunity(self): self.assertEqual([],validate_rights_opportunity(load('rights_opportunity_clean.json')))
    def test_rights_conflict(self): self.assertGreaterEqual(len(validate_rights_opportunity(load('rights_opportunity_conflict.json'))),2)
    def test_manifest(self): self.assertEqual([],validate_publication_manifest(load('publication_manifest_clean.json')))
    def test_provenance(self): self.assertEqual([],validate_provenance_graph(load('provenance_clean.json')))
    def test_provenance_bad(self): self.assertTrue(validate_provenance_graph(load('provenance_bad.json')))
    def test_recovery(self): self.assertEqual([],validate_recovery_manifest(load('recovery_clean.json')))
    def test_gate10_clean(self):
        e=validate_gate10('PASS',load('postpub_state_clean.json'),load('reconciliation_clean.json'),load('select_clean.json'),load('return_exposure_clean.json'),[load('deposit_print_clean.json')],load('publication_manifest_clean.json'),load('provenance_clean.json'),load('recovery_clean.json'),True)
        self.assertEqual([],e)
    def test_gate10_requires_human(self):
        e=validate_gate10('PASS',load('postpub_state_clean.json'),load('reconciliation_clean.json'),load('select_clean.json'),load('return_exposure_clean.json'),[load('deposit_print_clean.json')],load('publication_manifest_clean.json'),load('provenance_clean.json'),load('recovery_clean.json'),False)
        self.assertIn('G10 human post-publication governance approval missing',e)
if __name__=='__main__': unittest.main()
