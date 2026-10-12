import json, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

class TestCLIPhase3(unittest.TestCase):
    def test_init_creates_phase3_workspace(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'project'
            r=subprocess.run([sys.executable,str(ROOT/'novpub_cli.py'),'init',str(p),'--project-id','T-P3'],cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertTrue((p/'05_PRODUCTION/07_EPUB/source').is_dir())
            m=json.loads((p/'project_manifest.json').read_text())
            manifest=json.loads((ROOT/'MANIFEST.json').read_text())
            self.assertEqual(m['package_version'],manifest['version'])
    def test_pdf_cli(self):
        f=ROOT/'tests/fixtures/phase3/clean_6x9.pdf'
        r=subprocess.run([sys.executable,str(ROOT/'novpub_cli.py'),'preflight-pdf',str(f),'--width','6','--height','9','--pages','2'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertTrue(json.loads(r.stdout)['passed'])
    def test_epub_cli(self):
        f=ROOT/'tests/fixtures/phase3/clean.epub'
        r=subprocess.run([sys.executable,str(ROOT/'novpub_cli.py'),'validate-epub',str(f)],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertTrue(json.loads(r.stdout)['passed'])
if __name__=='__main__': unittest.main()
