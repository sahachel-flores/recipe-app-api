"""
Sample test
"""

from django.test import SimpleTestCase

from app import calc


class CalcTest(SimpleTestCase):
    """ Test calc module """
    def test_add_numers(self):
        res = calc.add(5, 6)
        self.assertEqual(res, 11)

    def test_subtract_numbers(self):
        """Test subtracting numbers"""
        res = calc.subtract(10, 10)
        self.assertEqual(res, 0)
