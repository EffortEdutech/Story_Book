import json, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class CliPhase4Tests(unittest.TestCase):
    def run_cli(self,*args): return subprocess.run([sys.executable,str(ROOT/'novpub_cli.py'),*map(str,args)],cwd=ROOT,capture_output=True,text=True)
    def test_kdp_print_calc(self):
        r=self.run_cli('calc-kdp-print',15,5,.6); self.assertEqual(0,r.returncode,r.stderr); self.assertEqual('4.00',json.loads(r.stdout)['royalty'])
    def test_ingram_calc(self):
        r=self.run_cli('calc-ingram',15,.55,5); self.assertEqual(0,r.returncode,r.stderr); self.assertEqual('1.75',json.loads(r.stdout)['publisher_compensation'])
if __name__=='__main__': unittest.main()
