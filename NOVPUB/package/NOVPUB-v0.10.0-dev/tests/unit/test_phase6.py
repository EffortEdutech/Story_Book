import json, unittest
from pathlib import Path
from datetime import date
from validators.phase6 import *
ROOT=Path(__file__).resolve().parents[2]; FX=ROOT/'tests/fixtures/phase6'
def load(n): return json.loads((FX/n).read_text())
class Phase6Tests(unittest.TestCase):
    def test_rule_current(self): self.assertEqual([],validate_ingram_rule_snapshot(load('rule_current.json'),date(2026,10,10)))
    def test_rule_stale(self): self.assertTrue(any('ING-RULE-003' in x for x in validate_ingram_rule_snapshot(load('rule_stale.json'),date(2026,10,10))))
    def test_account_ready(self): self.assertEqual([],validate_ingram_account(load('account_ready.json')))
    def test_account_not_ready(self): self.assertTrue(validate_ingram_account(load('account_not_ready.json')))
    def test_metadata_clean(self): self.assertEqual([],validate_ingram_metadata(load('metadata_clean.json')))
    def test_metadata_bad_isbn(self): self.assertTrue(any('ING-META-005' in x for x in validate_ingram_metadata(load('metadata_bad_isbn.json'))))
    def test_manufacturing_clean(self): self.assertEqual([],validate_ingram_manufacturing(load('manufacturing_clean.json'),320,{'interior':'int123','cover':'cov123'}))
    def test_stale_cover_template(self): self.assertTrue(any('ING-PRD-009' in x for x in validate_ingram_manufacturing(load('manufacturing_stale_template.json'))))
    def test_isbn_clean(self): self.assertEqual([],validate_ingram_isbn_reconciliation(load('isbn_clean.json'),'9780306406157'))
    def test_free_isbn_conflict(self): self.assertTrue(any('ING-ISBN-005' in x for x in validate_ingram_isbn_reconciliation(load('isbn_free.json'))))
    def test_print_pair(self): self.assertEqual([],validate_print_isbn_pair(load('isbn_clean.json'),load('isbn_hardcover_clean.json')))
    def test_print_pair_collision(self): self.assertTrue(any('ING-ISBN-006' in x for x in validate_print_isbn_pair(load('isbn_clean.json'),load('isbn_hardcover_collision.json'))))
    def test_coexistence_clean(self): self.assertEqual([],validate_kdp_ingram_coexistence(load('coexistence_clean.json')))
    def test_coexistence_conflict(self): self.assertTrue(any('ING-ISBN-008' in x for x in validate_kdp_ingram_coexistence(load('coexistence_conflict.json'))))
    def test_historical_expanded_distribution(self): self.assertTrue(any('ING-ISBN-009' in x for x in validate_kdp_ingram_coexistence(load('coexistence_historical.json'))))
    def test_pricing_clean(self): self.assertEqual([],validate_ingram_market_pricing(load('pricing_clean.json')))
    def test_pricing_discount(self): self.assertTrue(any('ING-WHL-004' in x for x in validate_ingram_market_pricing(load('pricing_bad_discount.json'))))
    def test_pricing_compensation(self): self.assertTrue(any('ING-WHL-009' in x for x in validate_ingram_market_pricing(load('pricing_bad_comp.json'))))
    def test_returns_nonreturnable(self): self.assertEqual([],validate_ingram_return_policy(load('returns_nonreturnable_clean.json')))
    def test_returns_yes_destroy(self): self.assertEqual([],validate_ingram_return_policy(load('returns_yes_destroy_clean.json')))
    def test_returns_unapproved(self): self.assertTrue(any('ING-RET-006' in x for x in validate_ingram_return_policy(load('returns_unapproved.json'))))
    def test_return_tail(self): self.assertEqual([],validate_ingram_return_policy(load('returns_tail_clean.json')))
    def test_return_tail_short(self): self.assertTrue(any('ING-RET-008' in x for x in validate_ingram_return_policy(load('returns_tail_short.json'))))
    def test_eproof(self): self.assertEqual([],validate_ingram_eproof(load('eproof_clean.json')))
    def test_eproof_blocked(self): self.assertTrue(validate_ingram_eproof(load('eproof_blocked.json')))
    def test_physical_proof(self): self.assertEqual([],validate_ingram_physical_proof(load('physical_proof_clean.json')))
    def test_physical_proof_fake(self): self.assertTrue(validate_ingram_physical_proof(load('physical_proof_fake.json')))
    def test_gate08_requires_all(self): self.assertEqual([],validate_gate08_components({'kdp_paperback':'PASS','ingram_paperback':'PASS','hardcover':'NOT_APPLICABLE'},True))
    def test_gate08_pending(self): self.assertTrue(validate_gate08_components({'kdp_paperback':'PASS','ingram_paperback':'PENDING'},True))
    def test_distribution_auth(self): self.assertEqual([],validate_ingram_distribution_authorization(load('distribution_authorization_clean.json')))
    def test_distribution_blocked(self): self.assertTrue(validate_ingram_distribution_authorization(load('distribution_authorization_blocked.json')))
    def test_listing_clean(self):
        e={'title':'Pilot Novel','author':'A. Author','isbn':'9780306406157','publisher':'Pilot Press','price':15.0,'cover_hash':'cov123'}
        self.assertEqual([],validate_retailer_listing(load('retailer_listing_clean.json'),e))
    def test_listing_wrong_price(self):
        e={'title':'Pilot Novel','author':'A. Author','isbn':'9780306406157','publisher':'Pilot Press','price':15.0,'cover_hash':'cov123'}
        self.assertTrue(any('ING-LIVE-005' in x for x in validate_retailer_listing(load('retailer_listing_wrong_price.json'),e)))
    def test_gate_passes_clean(self):
        e=validate_gate_ingram01(load('rule_current.json'),load('account_ready.json'),[load('metadata_clean.json')],[load('manufacturing_clean.json')],[load('isbn_clean.json')],[load('coexistence_clean.json')],[load('pricing_clean.json')],[load('returns_nonreturnable_clean.json')],[load('eproof_clean.json')],[load('physical_proof_clean.json')],[load('distribution_authorization_clean.json')],True)
        self.assertEqual([],e)
    def test_gate_requires_human(self):
        e=validate_gate_ingram01(load('rule_current.json'),load('account_ready.json'),[load('metadata_clean.json')],[load('manufacturing_clean.json')],[load('isbn_clean.json')],[load('coexistence_clean.json')],[load('pricing_clean.json')],[load('returns_nonreturnable_clean.json')],[load('eproof_clean.json')],[load('physical_proof_clean.json')],[load('distribution_authorization_clean.json')],False)
        self.assertIn('ING01 human Ingram gate approval missing',e)
if __name__=='__main__': unittest.main()
