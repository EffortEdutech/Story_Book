import json, shutil, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
TMP=ROOT.parent/'_test_phase5_workspace'
class CliPhase5WorkspaceTests(unittest.TestCase):
    def tearDown(self):
        if TMP.exists(): shutil.rmtree(TMP)
    def test_init_creates_phase5_tree_and_dynamic_version(self):
        r=subprocess.run([sys.executable,str(ROOT/'novpub_cli.py'),'init',str(TMP),'--project-id','P5TEST'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(0,r.returncode,r.stdout+r.stderr)
        self.assertTrue((TMP/'07_KDP/02_KINDLE/kindle_files').exists())
        self.assertTrue((TMP/'07_KDP/08_SUBMISSION/submission_receipts').exists())
        manifest=json.loads((ROOT/'MANIFEST.json').read_text())
        project=json.loads((TMP/'project_manifest.json').read_text())
        self.assertEqual(manifest['version'],project['package_version'])
if __name__=='__main__': unittest.main()
