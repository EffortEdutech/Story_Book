import json, shutil, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; TMP=ROOT.parent/'_test_phase6_workspace'
class CliPhase6WorkspaceTests(unittest.TestCase):
    def tearDown(self):
        if TMP.exists(): shutil.rmtree(TMP)
    def test_init_phase6_tree_dynamic_version(self):
        r=subprocess.run([sys.executable,str(ROOT/'novpub_cli.py'),'init',str(TMP),'--project-id','P6TEST'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(0,r.returncode,r.stdout+r.stderr)
        self.assertTrue((TMP/'08_INGRAMSPARK/05_FILES/interiors').exists())
        self.assertTrue((TMP/'08_INGRAMSPARK/09_PHYSICAL_PROOF').exists())
        self.assertTrue((TMP/'08_INGRAMSPARK/12_COMPLETION').exists())
        manifest=json.loads((ROOT/'MANIFEST.json').read_text()); project=json.loads((TMP/'project_manifest.json').read_text())
        self.assertEqual(manifest['version'],project['package_version'])
if __name__=='__main__': unittest.main()
