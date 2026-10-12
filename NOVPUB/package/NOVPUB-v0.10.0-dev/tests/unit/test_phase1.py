import unittest, json
from pathlib import Path
from validators.phase1 import validate_chapter_manifest, validate_editorial_gate, find_placeholders
ROOT=Path(__file__).resolve().parents[2]
class TestPhase1(unittest.TestCase):
    def test_clean_chapters(self):
        self.assertEqual(validate_chapter_manifest(ROOT/'tests/fixtures/phase1/chapter_manifest_clean.json'),[])
    def test_duplicate(self):
        self.assertIn('STRUCT-002 duplicate chapter_id',validate_chapter_manifest(ROOT/'tests/fixtures/phase1/chapter_manifest_duplicate.json'))
    def test_placeholder(self):
        self.assertTrue(find_placeholders('Text [TODO: fix ending]'))
    def test_gate_invalid(self):
        d=json.loads((ROOT/'tests/fixtures/phase1/editorial_approval_invalid.json').read_text())
        self.assertGreater(len(validate_editorial_gate(d)),0)
if __name__=='__main__': unittest.main()
