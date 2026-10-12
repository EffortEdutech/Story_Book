import unittest
from pathlib import Path
from validators.package import validate_package
ROOT=Path(__file__).resolve().parents[2]
class TestPackage(unittest.TestCase):
    def test_package_self_check(self):
        self.assertEqual(validate_package(ROOT),[])
if __name__=='__main__': unittest.main()
