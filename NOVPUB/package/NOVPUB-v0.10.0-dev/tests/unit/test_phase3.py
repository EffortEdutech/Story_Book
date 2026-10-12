import json, unittest
from pathlib import Path
from validators.phase3 import *

ROOT=Path(__file__).resolve().parents[2]
FX=ROOT/'tests/fixtures/phase3'
def load(name): return json.loads((FX/name).read_text())

class Phase3Tests(unittest.TestCase):
    def test_book_model(self): self.assertEqual([],validate_book_model(load('book_model_clean.json')))
    def test_format(self): self.assertEqual([],validate_format_strategy(load('format_strategy_clean.json')))
    def test_trim_cross_channel(self): self.assertTrue(any('TRIM-004' in x for x in validate_trim_profile(load('trim_unsupported.json'),['KDP','INGRAM'])))
    def test_fonts_clean(self): self.assertEqual([],validate_font_register(load('fonts_clean.json')))
    def test_fonts_unlicensed(self): self.assertTrue(validate_font_register(load('fonts_unlicensed.json')))
    def test_typography(self): self.assertEqual([],validate_typography(load('typography_clean.json'),load('fonts_clean.json')))
    def test_page_architecture(self): self.assertEqual([],validate_page_architecture(load('page_architecture_clean.json')))
    def test_text_integrity_whitespace(self): self.assertEqual([],validate_text_integrity('Hello\nworld','Hello world'))
    def test_text_integrity_change(self): self.assertTrue(validate_text_integrity('Hello world','Hello brave world'))
    def test_pdf_clean(self):
        r=preflight_pdf(FX/'clean_6x9.pdf',6,9,2,require_embedded_fonts=True); self.assertTrue(r['passed'],r)
    def test_pdf_wrong_size(self):
        r=preflight_pdf(FX/'wrong_size.pdf',6,9,2); self.assertFalse(r['passed']); self.assertTrue(any('PDF-002' in x for x in r['errors']))
    def test_pdf_mixed_size(self):
        r=preflight_pdf(FX/'mixed_size.pdf'); self.assertFalse(r['passed']); self.assertIn('PDF-003 inconsistent page dimensions',r['errors'])
    def test_epub_clean(self): self.assertTrue(validate_epub_file(FX/'clean.epub')['passed'])
    def test_epub_broken(self): self.assertFalse(validate_epub_file(FX/'broken.epub')['passed'])
    def test_cover_spec(self): self.assertEqual([],validate_cover_spec(load('cover_spec_clean.json'),load('pagination_clean.json')))
    def test_cover_wrong_page_count(self): self.assertTrue(any('COV-006' in x for x in validate_cover_spec(load('cover_spec_wrong_pages.json'),load('pagination_clean.json'))))
    def test_cover_parity(self):
        expected={'title':'Pilot Novel','author':'A. Author','isbn':'9780306406157','publisher':'Test Press'}
        self.assertEqual([],validate_cover_parity(load('cover_qa_clean.json'),expected))
    def test_proof_plan(self): self.assertEqual([],validate_proof_plan(load('proof_plan_clean.json')))
    def test_fake_physical_approval(self): self.assertTrue(len(validate_physical_proof(load('physical_proof_fake_approval.json')))>=3)
    def test_gate05_requires_human(self):
        epub=validate_epub_file(FX/'clean.epub'); epub['reading_qa']='PASS'
        pdf=preflight_pdf(FX/'clean_6x9.pdf',6,9,2)
        errs=validate_gate05(load('book_model_clean.json'),load('source_manifest_clean.json'),load('trim_clean.json'),load('typography_clean.json'),load('fonts_clean.json'),load('page_architecture_clean.json'),pdf,epub,False)
        self.assertIn('G05 human interior approval missing',errs)
    def test_gate06_requires_human(self):
        expected={'title':'Pilot Novel','author':'A. Author','isbn':'9780306406157','publisher':'Test Press'}
        errs=validate_gate06(load('cover_spec_clean.json'),load('pagination_clean.json'),load('cover_qa_clean.json'),expected,False)
        self.assertIn('G06 human cover approval missing',errs)

if __name__=='__main__': unittest.main()
