import subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; CLI=ROOT/'novpub_cli.py'; FX=ROOT/'tests/fixtures/phase8'
class Phase8CliTests(unittest.TestCase):
    def runcli(self,*args): return subprocess.run([sys.executable,str(CLI),*map(str,args)],cwd=ROOT,text=True,capture_output=True,timeout=20)
    def test_sales(self): self.assertEqual(0,self.runcli('validate-postpub-sales',FX/'sales_clean.json').returncode)
    def test_reconcile(self): self.assertEqual(0,self.runcli('validate-postpub-reconciliation',FX/'reconciliation_clean.json').returncode)
    def test_select(self): self.assertEqual(0,self.runcli('validate-select-lifecycle',FX/'select_clean.json').returncode)
    def test_revision(self): self.assertEqual(0,self.runcli('validate-revision',FX/'revision_minor.json').returncode)
    def test_return_exposure(self): self.assertEqual(0,self.runcli('validate-return-exposure',FX/'return_exposure_clean.json').returncode)
    def test_deposit(self): self.assertEqual(0,self.runcli('validate-legal-deposit',FX/'deposit_print_clean.json','--date','2026-10-10').returncode)
    def test_deadline(self):
        r=self.runcli('legal-deposit-deadline','2026-09-15','PRINTED'); self.assertEqual(0,r.returncode); self.assertIn('2026-10-15',r.stdout)
    def test_archive(self): self.assertEqual(0,self.runcli('validate-publication-archive',FX/'publication_manifest_clean.json').returncode)
if __name__=='__main__': unittest.main()
