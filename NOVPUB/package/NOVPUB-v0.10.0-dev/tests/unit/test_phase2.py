import json
import unittest
from datetime import date
from pathlib import Path
from validators.phase2 import (
    validate_rights_profile, validate_permissions, validate_author_identity,
    validate_publisher_profiles, validate_edition_manifest, validate_isbn_registry,
    validate_isbn_edition_parity, validate_copyright_page, validate_legal_deposit_plan,
    validate_gate03, validate_gate04,
)
ROOT = Path(__file__).resolve().parents[2]
F = ROOT / 'tests/fixtures/phase2'
def load(name):
    return json.loads((F / name).read_text())

class TestPhase2(unittest.TestCase):
    def test_clean_rights(self):
        self.assertEqual(validate_rights_profile(load('rights_clean.json')), [])
    def test_unresolved_rights(self):
        self.assertTrue(any('RIGHTS-002' in e for e in validate_rights_profile(load('rights_unresolved.json'))))
    def test_clean_permissions(self):
        self.assertEqual(validate_permissions(load('third_party_clean.json'), load('permissions_empty.json')), [])
    def test_missing_permission(self):
        self.assertTrue(any('TPR-003' in e for e in validate_permissions(load('third_party_missing_permission.json'), load('permissions_empty.json'))))
    def test_penname_privacy(self):
        self.assertEqual(validate_author_identity(load('author_identity_penname.json')), [])
    def test_publisher_imprint(self):
        self.assertEqual(validate_publisher_profiles(load('publisher_clean.json'), load('imprint_clean.json')), [])
    def test_clean_editions(self):
        self.assertEqual(validate_edition_manifest(load('edition_manifest_clean.json')), [])
    def test_duplicate_isbn_editions(self):
        self.assertTrue(any('ISBN-003' in e for e in validate_edition_manifest(load('edition_manifest_duplicate_isbn.json'))))
    def test_isbn_registry(self):
        self.assertEqual(validate_isbn_registry(load('isbn_registry_clean.json')), [])
    def test_invalid_registry_isbn(self):
        self.assertTrue(any('ISBN-001' in e for e in validate_isbn_registry(load('isbn_registry_invalid.json'))))
    def test_isbn_edition_parity(self):
        self.assertEqual(validate_isbn_edition_parity(load('edition_manifest_clean.json'), load('isbn_registry_clean.json')), [])
    def test_copyright_page(self):
        self.assertEqual(validate_copyright_page(load('copyright_page_clean.json'), load('rights_clean.json'), load('publisher_clean.json'), load('edition_manifest_clean.json')), [])
    def test_wrong_copyright_publisher(self):
        self.assertTrue(any('COPY-002' in e for e in validate_copyright_page(load('copyright_page_wrong_publisher.json'), load('rights_clean.json'), load('publisher_clean.json'), load('edition_manifest_clean.json'))))
    def test_legal_deposit(self):
        self.assertEqual(validate_legal_deposit_plan(load('legal_deposit_clean.json'), today=date(2026,10,10)), [])
    def test_stale_rule(self):
        self.assertTrue(any('COMP-010' in e for e in validate_legal_deposit_plan(load('legal_deposit_stale.json'), today=date(2026,10,10))))
    def test_gate03_requires_human(self):
        self.assertTrue(any('G03' in e for e in validate_gate03(load('rights_clean.json'), load('third_party_clean.json'), load('permissions_empty.json'), False)))
    def test_gate03_pass(self):
        self.assertEqual(validate_gate03(load('rights_clean.json'), load('third_party_clean.json'), load('permissions_empty.json'), True), [])
    def test_gate04_pass(self):
        self.assertEqual(validate_gate04(
            load('author_identity_penname.json'), load('publisher_clean.json'), load('imprint_clean.json'),
            load('edition_manifest_clean.json'), load('isbn_registry_clean.json'), load('copyright_page_clean.json'),
            load('legal_deposit_clean.json'), load('rights_clean.json'), True, today=date(2026,10,10)), [])

if __name__ == '__main__':
    unittest.main()
