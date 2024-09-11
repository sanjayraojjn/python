import unittest
from tic_tac_toe.logic.models import Move

class TestMoveMethods(unittest.TestCase):
    pass

    # def test_move_creation(self):
    #     move = Move(1, 2, 'X')
    #     self.assertEqual(move.row, 1)
    #     self.assertEqual(move.column, 2)
    #     self.assertEqual(move.player, 'X')

    # def test_move_equality(self):
    #     move1 = Move(1, 2, 'X')
    #     move2 = Move(1, 2, 'X')
    #     move3 = Move(3, 4, 'O')
    #     self.assertEqual(move1, move2)
    #     self.assertNotEqual(move1, move3)

    # def test_move_to_string(self):
    #     move = Move(1, 2, 'X')
    #     self.assertEqual(str(move), "(1, 2): X")

    # def test_move_hash(self):
    #     move1 = Move(1, 2, 'X')
    #     move2 = Move(1, 2, 'X')
    #     move3 = Move(3, 4, 'O')
    #     self.assertEqual(hash(move1), hash(move2))
    #     self.assertNotEqual(hash(move1), hash(move3))
