import json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; CLI=ROOT/'novpub_cli.py'
class Phase8WorkspaceTests(unittest.TestCase):
    def test_init_contains_phase8_workspace(self):
        tmp=Path(tempfile.mkdtemp())/'pilot'
        try:
            r=subprocess.run([sys.executable,str(CLI),'init',str(tmp),'--project-id','B8'],cwd=ROOT,text=True,capture_output=True,timeout=20)
            self.assertEqual(0,r.returncode,r.stderr)
            for rel in ['12_POST_PUBLICATION/00_STATE','12_POST_PUBLICATION/01_SALES/raw_reports','12_POST_PUBLICATION/03_KDP_SELECT','12_POST_PUBLICATION/05_ERRATA','12_POST_PUBLICATION/07_INGRAM_OPERATIONS','12_POST_PUBLICATION/09_MALAYSIA_COMPLIANCE/deposit_evidence','12_POST_PUBLICATION/11_ARCHIVE/asset_archive','12_POST_PUBLICATION/12_GOVERNANCE']:
                self.assertTrue((tmp/rel).is_dir(),rel)
            m=json.loads((tmp/'project_manifest.json').read_text()); expected=json.loads((ROOT/'MANIFEST.json').read_text())['version']; self.assertEqual(expected,m['package_version'])
        finally: shutil.rmtree(tmp.parent,ignore_errors=True)
if __name__=='__main__': unittest.main()
