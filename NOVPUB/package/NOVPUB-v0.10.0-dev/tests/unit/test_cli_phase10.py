import json, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; CLI=ROOT/'novpub_cli.py'; FX=ROOT/'tests/fixtures/phase10'
class CliPhase10(unittest.TestCase):
    def runok(self,*args): return subprocess.run([sys.executable,str(CLI),*map(str,args)],cwd=ROOT,capture_output=True,text=True,timeout=20)
    def test_project(self): self.assertEqual(0,self.runok('validate-pilot-project',FX/'pilot_project_clean.json').returncode)
    def test_baseline(self): self.assertEqual(0,self.runok('validate-real-baseline',FX/'baseline_clean.json').returncode)
    def test_evidence(self): self.assertEqual(0,self.runok('validate-pilot-evidence',FX/'evidence_matrix_clean.json').returncode)
    def test_kdp(self): self.assertEqual(0,self.runok('validate-kdp-pilot',FX/'kdp_pilot_clean.json').returncode)
    def test_ingram(self): self.assertEqual(0,self.runok('validate-ingram-pilot',FX/'ingram_pilot_clean.json').returncode)
    def test_findings(self): self.assertEqual(0,self.runok('validate-pilot-findings',FX/'findings_clean.json').returncode)
    def test_parity(self): self.assertEqual(0,self.runok('validate-real-pilot-parity',FX/'real_parity_clean.json').returncode)
    def test_v1(self): self.assertEqual(0,self.runok('validate-v1-release',FX/'v1_clean_fixture.json').returncode)
    def test_init_pilot(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'pilot'; r=self.runok('init-pilot',p,'--project-id','NOVPUB-PILOT-TEST')
            self.assertEqual(0,r.returncode,r.stderr); m=json.loads((p/'project_manifest.json').read_text()); self.assertEqual('professional_real_novel_pilot',m['project_type']); self.assertEqual(json.loads((ROOT/'MANIFEST.json').read_text())['version'],m['package_version']); self.assertTrue((p/'15_RELEASE_EVIDENCE/v1_release_gate.json').exists())
if __name__=='__main__': unittest.main()
