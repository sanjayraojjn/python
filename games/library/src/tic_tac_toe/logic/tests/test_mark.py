import unittest

from tic_tac_toe.logic.models import Mark

class TestMarkMethods(unittest.TestCase):

    def test_equality(self):
        self.assertEqual(Mark("X"), Mark.CROSS)
        self.assertEqual(Mark("O"), Mark.NAUGHT)
        self.assertEqual(Mark("X").value, Mark.CROSS)
        self.assertEqual(Mark("O").value, Mark.NAUGHT)
        self.assertEqual(Mark("X"), Mark("X"))
        self.assertEqual(Mark("O"), Mark("O"))
        self.assertNotEqual(Mark("X"), Mark("O"))

    def test_names(self):
        self.assertEqual(Mark("X").name, "CROSS")
        self.assertEqual(Mark("O").name, "NAUGHT")

    def test_str_matching(self):
        self.assertEqual(Mark.NAUGHT, 'O')
        self.assertEqual(Mark.CROSS, 'X')
        self.assertEqual(Mark["NAUGHT"], "O")
        self.assertEqual(Mark["CROSS"], 'X')
        self.assertEqual(Mark.CROSS.lower(), "x")
        self.assertEqual(Mark.NAUGHT.lower(), "o")

        self.assertTrue( isinstance(Mark.CROSS, str) )
        self.assertTrue( isinstance(Mark.NAUGHT, str) )

    def test_invalid_mark(self):
        with self.assertRaises(ValueError):
            Mark("A")

    def test_mark_count(self):
        self.assertEqual(len(Mark), 2)

if __name__ == '__main__':
    unittest.main()