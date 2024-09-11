import unittest

class TestMinimax(unittest.TestCase):

    def test_minimax_algo(self):


    def test_initial_state(self):
        grid = Grid()
        self.assertEqual(grid.cells, " "*9)

    def test_update_cell(self):
        grid = Grid("X         ")
        self.assertEqual(grid.cells, "X"+ " "*8)

    def test_invalid_cell_update(self):
        with self.assertRaises(ValueError):
            grid = Grid("A         ")
        with self.assertRaises(ValueError):
            grid = Grid("   ")
        with self.assertRaises(ValueError):
            grid = Grid("            ")

    def test_is_full(self):
        grid = Grid("")
        self.assertFalse(grid.is_full())
        grid = Grid("XOXOXOXOX")
        self.assertTrue(grid.is_full())

if __name__ == '__main__':
    unittest.main()