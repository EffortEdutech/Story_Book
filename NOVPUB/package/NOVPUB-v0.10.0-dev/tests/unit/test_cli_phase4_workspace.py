import json, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class TestCLIPhase4Workspace(unittest.TestCase):
    def test_init_creates_phase4_workspace(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'project'
            r=subprocess.run([sys.executable,str(ROOT/'novpub_cli.py'),'init',str(p),'--project-id','T-P4'],cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertTrue((p/'06_METADATA/00_MASTER').is_dir())
            self.assertTrue((p/'06_METADATA/10_CHANNEL_MAPS').is_dir())
            self.assertTrue((p/'06_METADATA/11_APPROVAL').is_dir())
            manifest=json.loads((ROOT/'MANIFEST.json').read_text())
            project=json.loads((p/'project_manifest.json').read_text())
            self.assertEqual(project['package_version'],manifest['version'])
if __name__=='__main__': unittest.main()
