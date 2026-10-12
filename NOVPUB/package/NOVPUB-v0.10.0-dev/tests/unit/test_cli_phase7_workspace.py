import json, shutil, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; TMP=ROOT.parent/'_test_phase7_workspace'
class CliPhase7WorkspaceTests(unittest.TestCase):
    def tearDown(self):
        if TMP.exists(): shutil.rmtree(TMP)
    def test_init_phase7_tree_dynamic_version(self):
        r=subprocess.run([sys.executable,str(ROOT/'novpub_cli.py'),'init',str(TMP),'--project-id','P7TEST'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(0,r.returncode,r.stdout+r.stderr)
        self.assertTrue((TMP/'10_LAUNCH/01_ARC/arc_files').exists())
        self.assertTrue((TMP/'10_LAUNCH/06_MEDIA_KIT/approved_images').exists())
        self.assertTrue((TMP/'10_LAUNCH/10_ANALYTICS').exists())
        self.assertTrue((TMP/'10_LAUNCH/11_APPROVAL').exists())
        manifest=json.loads((ROOT/'MANIFEST.json').read_text()); project=json.loads((TMP/'project_manifest.json').read_text())
        self.assertEqual(manifest['version'],project['package_version'])
if __name__=='__main__': unittest.main()
