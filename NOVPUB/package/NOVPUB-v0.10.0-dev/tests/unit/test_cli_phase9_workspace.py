import json, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; CLI=ROOT/'novpub_cli.py'
class CliPhase9Workspace(unittest.TestCase):
  def test_init_has_phase9_workspace_and_version(self):
    with tempfile.TemporaryDirectory() as td:
      target=Path(td)/'book'; r=subprocess.run([sys.executable,str(CLI),'init',str(target),'--project-id','P9'],cwd=ROOT,text=True,capture_output=True); self.assertEqual(0,r.returncode,r.stderr)
      self.assertTrue((target/'validation/12_RELEASE').is_dir())
      m=json.loads((target/'project_manifest.json').read_text()); self.assertEqual(json.loads((ROOT/'MANIFEST.json').read_text())['version'],m['package_version'])
if __name__=='__main__': unittest.main()
