import unittest
from validators.isbn import validate_isbn13, isbn13_check_digit
class TestISBN(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate_isbn13('9780306406157'))
    def test_invalid_digit(self):
        self.assertFalse(validate_isbn13('9780306406158'))
    def test_compute(self):
        self.assertEqual(isbn13_check_digit('978030640615'),7)
if __name__=='__main__': unittest.main()
