import unittest
from validators.gate import validate_gate_record
class TestGate(unittest.TestCase):
    def test_pass_needs_evidence(self):
        self.assertTrue(validate_gate_record({'status':'PASS','evidence':[]},False))
    def test_human_gate(self):
        self.assertTrue(validate_gate_record({'status':'PASS','evidence':['x'],'approved_by':None},True))
    def test_valid(self):
        self.assertEqual(validate_gate_record({'status':'PASS','evidence':['x'],'approved_by':'publisher'},True),[])
if __name__=='__main__': unittest.main()
