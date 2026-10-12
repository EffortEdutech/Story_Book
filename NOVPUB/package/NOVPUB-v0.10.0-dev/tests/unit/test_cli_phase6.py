import subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; FX=ROOT/'tests/fixtures/phase6'
class CliPhase6Tests(unittest.TestCase):
    def run_cli(self,*args): return subprocess.run([sys.executable,str(ROOT/'novpub_cli.py'),*map(str,args)],cwd=ROOT,capture_output=True,text=True)
    def test_isbn(self):
        r=self.run_cli('validate-ingram-isbn',FX/'isbn_clean.json'); self.assertEqual(0,r.returncode,r.stdout+r.stderr); self.assertIn('PASS',r.stdout)
    def test_coexistence(self): self.assertEqual(0,self.run_cli('validate-ingram-coexistence',FX/'coexistence_clean.json').returncode)
    def test_returns(self): self.assertEqual(0,self.run_cli('validate-ingram-returns',FX/'returns_nonreturnable_clean.json').returncode)
    def test_eproof(self): self.assertEqual(0,self.run_cli('validate-ingram-eproof',FX/'eproof_clean.json').returncode)
    def test_proof(self): self.assertEqual(0,self.run_cli('validate-ingram-proof',FX/'physical_proof_clean.json').returncode)
    def test_metadata(self): self.assertEqual(0,self.run_cli('validate-ingram-metadata',FX/'metadata_clean.json').returncode)
if __name__=='__main__': unittest.main()
