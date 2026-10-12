import json, unittest
from pathlib import Path
from decimal import Decimal
from validators.phase4 import *

ROOT=Path(__file__).resolve().parents[2]
FX=ROOT/'tests/fixtures/phase4'
def load(n): return json.loads((FX/n).read_text())

class Phase4Tests(unittest.TestCase):
    def test_metadata_master(self): self.assertEqual([],validate_metadata_master(load('metadata_master_clean.json')))
    def test_positioning(self): self.assertEqual([],validate_positioning(load('positioning_clean.json')))
    def test_classification(self): self.assertEqual([],validate_classification(load('classification_clean.json')))
    def test_keywords_clean(self): self.assertEqual([],validate_keywords(load('keywords_clean.json')))
    def test_keywords_bad(self):
        e=validate_keywords(load('keywords_bad.json'),competitor_names=['Famous Author']); self.assertTrue(any('KW-006' in x for x in e)); self.assertTrue(any('KW-007' in x for x in e))
    def test_descriptions(self): self.assertEqual([],validate_descriptions(load('descriptions_clean.json')))
    def test_pen_name_privacy(self): self.assertTrue(any('BIO-003' in x for x in validate_author_bios(load('author_bios_leak.json'),'Secret Legal Name')))
    def test_kdp_print_royalty_rate(self): self.assertEqual(Decimal('0.60'),kdp_print_royalty_rate(9.99,9.99)); self.assertEqual(Decimal('0.50'),kdp_print_royalty_rate(9.98,9.99))
    def test_kdp_print_royalty(self): self.assertEqual(Decimal('4.00'),calculate_kdp_print_royalty(15,5,.60))
    def test_kdp_ebook_royalty(self): self.assertEqual(Decimal('6.29'),calculate_kdp_ebook_royalty(9.99,.70,.70))
    def test_ingram_compensation(self): self.assertEqual(Decimal('1.75'),calculate_ingram_compensation(15,.55,5))
    def test_return_exposure(self): self.assertEqual(Decimal('67.50'),calculate_return_exposure(10,15,.55))
    def test_pricing_negative(self): self.assertTrue(any('PRICE-005' in x for x in validate_pricing_model(load('pricing_negative.json'))))
    def test_wholesale(self): self.assertEqual([],validate_wholesale(load('wholesale_clean.json'),.40,.55))
    def test_returns_clean(self): self.assertEqual([],validate_returns(load('returns_clean.json')))
    def test_returns_incomplete(self): self.assertTrue(validate_returns(load('returns_incomplete.json')))
    def test_territories(self): self.assertEqual([],validate_territories(load('territories_clean.json')))
    def test_territory_violation(self): self.assertTrue(any('TERR-001' in x for x in validate_territories(load('territories_exceed_rights.json'))))
    def test_release_clean(self): self.assertEqual([],validate_publication_strategy(load('publication_clean.json')))
    def test_release_bad(self): self.assertTrue(any('REL-002' in x for x in validate_publication_strategy(load('publication_bad_dates.json'))))
    def test_gate07_requires_human(self):
        e=validate_gate07(load('metadata_master_clean.json'),load('positioning_clean.json'),load('classification_clean.json'),load('keywords_clean.json'),load('descriptions_clean.json'),load('author_bios_clean.json'),load('pricing_clean.json'),load('wholesale_clean.json'),load('returns_clean.json'),load('territories_clean.json'),load('publication_clean.json'),False)
        self.assertIn('G07 human commercial approval missing',e)

if __name__=='__main__': unittest.main()
