import json, unittest
from pathlib import Path
from datetime import date
from validators.phase5 import *
ROOT=Path(__file__).resolve().parents[2]; FX=ROOT/'tests/fixtures/phase5'
def load(n): return json.loads((FX/n).read_text())
class Phase5Tests(unittest.TestCase):
    def test_rule_current(self): self.assertEqual([],validate_kdp_rule_snapshot(load('rule_current.json'),date(2026,10,10)))
    def test_rule_stale(self): self.assertTrue(any('KDP-RULE-003' in x for x in validate_kdp_rule_snapshot(load('rule_stale.json'),date(2026,10,10))))
    def test_account_ready(self): self.assertEqual([],validate_kdp_account(load('account_ready.json')))
    def test_account_not_ready(self): self.assertTrue(validate_kdp_account(load('account_not_ready.json')))
    def test_metadata_clean(self): self.assertEqual([],validate_kdp_metadata(load('kindle_metadata_clean.json')))
    def test_keyword_limit(self): self.assertTrue(any('KDP-META-002' in x for x in validate_kdp_metadata(load('kindle_8_keywords.json'))))
    def test_category_limit(self): self.assertTrue(any('KDP-META-003' in x for x in validate_kdp_metadata(load('kindle_4_categories.json'))))
    def test_print_isbn(self): self.assertEqual([],validate_kdp_print_isbn(load('paperback_metadata_clean.json'),True,'9780306406157','Pilot Press',False))
    def test_free_isbn_external_conflict(self): self.assertTrue(any('ARCHITECTURE' in x for x in validate_kdp_print_isbn(load('paperback_metadata_clean.json'),True,'9780306406157','Pilot Press',True)))
    def test_print_isbn_separate(self): self.assertEqual([],validate_print_format_pair(load('paperback_metadata_clean.json'),load('hardcover_metadata_clean.json')))
    def test_content_origin_clean(self): self.assertEqual([],validate_content_origin(load('content_origin_clean.json')))
    def test_content_origin_disclosure(self): self.assertTrue(any('KDP-AI-002' in x for x in validate_content_origin(load('content_origin_bad_disclosure.json'))))
    def test_select_wide(self): self.assertEqual([],validate_kdp_select(load('select_wide_clean.json')))
    def test_select_conflict(self):
        e=validate_kdp_select(load('select_conflict.json')); self.assertTrue(any('KDP-SELECT-001' in x for x in e)); self.assertTrue(any('KDP-SELECT-003' in x for x in e))
    def test_expanded_clean(self): self.assertEqual([],validate_expanded_distribution(load('expanded_distribution_clean.json')))
    def test_expanded_conflict(self): self.assertTrue(any('KDP-ED-001' in x for x in validate_expanded_distribution(load('expanded_distribution_conflict.json'))))
    def test_preorder_clean(self): self.assertEqual([],validate_kindle_preorder('2027-10-01','2026-10-10'))
    def test_preorder_too_far(self): self.assertTrue(any('KDP-PRE-003' in x for x in validate_kindle_preorder('2028-10-01','2026-10-10')))
    def test_scheduled_print_clean(self): self.assertEqual([],validate_scheduled_print_release('2026-12-01','2026-10-10'))
    def test_scheduled_print_too_far(self): self.assertTrue(any('KDP-REL-003' in x for x in validate_scheduled_print_release('2027-03-01','2026-10-10')))
    def test_kindle_preview(self): self.assertEqual([],validate_kindle_preview(load('kindle_preview_clean.json')))
    def test_print_preview(self): self.assertEqual([],validate_print_previewer(load('paperback_preview_clean.json')))
    def test_print_preview_blocked(self): self.assertTrue(any('KDP-PREV-006' in x for x in validate_print_previewer(load('print_preview_blocked.json'))))
    def test_proof_approved(self): self.assertEqual([],validate_kdp_proof(load('proof_approved.json')))
    def test_proof_fake(self): self.assertTrue(validate_kdp_proof(load('proof_fake_approval.json')))
    def test_authorization(self): self.assertEqual([],validate_publication_authorization(load('authorization_approved.json')))
    def test_authorization_missing(self): self.assertTrue(any('KDP-AUTH-003' in x for x in validate_publication_authorization(load('authorization_missing.json'))))
    def test_listing_clean(self):
        exp={'title':'Pilot Novel','author':'A. Author','isbn':'9780306406157','publisher':'Pilot Press','price':15.0,'cover_hash':'cover123'}
        self.assertEqual([],validate_amazon_listing(load('listing_clean.json'),exp))
    def test_listing_wrong_price(self):
        exp={'title':'Pilot Novel','author':'A. Author','isbn':'9780306406157','publisher':'Pilot Press','price':15.0,'cover_hash':'cover123'}
        self.assertTrue(any('KDP-LIVE-004' in x for x in validate_amazon_listing(load('listing_wrong_price.json'),exp)))
    def test_gate_requires_human(self):
        e=validate_gate_kdp01(load('rule_current.json'),load('account_ready.json'),[load('kindle_metadata_clean.json')],load('select_wide_clean.json'),[load('expanded_distribution_clean.json')],[load('kindle_preview_clean.json')],[load('proof_approved.json')],[load('authorization_approved.json')],False)
        self.assertIn('KDP01 human KDP gate approval missing',e)
if __name__=='__main__': unittest.main()
