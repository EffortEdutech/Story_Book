import subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; FX=ROOT/'tests/fixtures/phase5'
class CliPhase5Tests(unittest.TestCase):
    def run_cli(self,*args): return subprocess.run([sys.executable,str(ROOT/'novpub_cli.py'),*map(str,args)],cwd=ROOT,capture_output=True,text=True)
    def test_select(self):
        r=self.run_cli('validate-kdp-select',FX/'select_wide_clean.json'); self.assertEqual(0,r.returncode,r.stdout+r.stderr); self.assertIn('PASS',r.stdout)
    def test_expanded(self):
        r=self.run_cli('validate-expanded-distribution',FX/'expanded_distribution_clean.json'); self.assertEqual(0,r.returncode,r.stdout+r.stderr)
    def test_metadata(self):
        r=self.run_cli('validate-kdp-metadata',FX/'kindle_metadata_clean.json'); self.assertEqual(0,r.returncode,r.stdout+r.stderr)
if __name__=='__main__': unittest.main()
