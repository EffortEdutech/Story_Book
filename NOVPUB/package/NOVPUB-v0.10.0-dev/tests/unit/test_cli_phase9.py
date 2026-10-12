import subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; CLI=ROOT/'novpub_cli.py'; FX=ROOT/'tests/fixtures/phase9'
class CliPhase9(unittest.TestCase):
    def runcli(self,*args): return subprocess.run([sys.executable,str(CLI),*map(str,args)],cwd=ROOT,text=True,capture_output=True)
    def test_package(self): self.assertEqual(0,self.runcli('validate-phase9-package').returncode)
    def test_catalog(self): self.assertEqual(0,self.runcli('validate-adversarial-catalog',FX/'attack_catalog_clean.json').returncode)
    def test_parity(self): self.assertEqual(0,self.runcli('validate-agent-parity',FX/'agent_parity_clean.json').returncode)
    def test_professional_fixture(self): self.assertEqual(0,self.runcli('validate-professional-review',FX/'pro_review_clean_fixture.json').returncode)
    def test_fake_professional_review_fails(self): self.assertNotEqual(0,self.runcli('validate-professional-review',FX/'pro_review_fake.json').returncode)
    def test_rc_fixture(self): self.assertEqual(0,self.runcli('validate-release-candidate',FX/'rc_clean_fixture.json').returncode)
    def test_live_rc_pending_fails(self): self.assertNotEqual(0,self.runcli('validate-release-candidate',ROOT/'validation/12_RELEASE/release_candidate.json').returncode)
if __name__=='__main__': unittest.main()
