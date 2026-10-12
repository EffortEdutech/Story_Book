import subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; FX=ROOT/'tests/fixtures/phase7'
class CliPhase7Tests(unittest.TestCase):
    def runcli(self,*args): return subprocess.run([sys.executable,str(ROOT/'novpub_cli.py'),*map(str,args)],cwd=ROOT,capture_output=True,text=True)
    def test_review_outreach(self): self.assertEqual(0,self.runcli('validate-launch-review-outreach',FX/'outreach_clean.json').returncode)
    def test_review_outreach_bad(self): self.assertNotEqual(0,self.runcli('validate-launch-review-outreach',FX/'outreach_bad.json').returncode)
    def test_claims(self): self.assertEqual(0,self.runcli('validate-marketing-claims',FX/'claims_clean.json').returncode)
    def test_claims_bad(self): self.assertNotEqual(0,self.runcli('validate-marketing-claims',FX/'claims_bad.json').returncode)
    def test_calendar(self): self.assertEqual(0,self.runcli('validate-launch-calendar',FX/'calendar_clean.json','--live-listing-ready').returncode)
    def test_authorization(self): self.assertEqual(0,self.runcli('validate-launch-authorization',FX/'authorization_clean.json').returncode)
if __name__=='__main__': unittest.main()
