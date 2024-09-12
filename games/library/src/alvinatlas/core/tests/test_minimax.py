import unittest

from alvinatlas.core.models import SimpleNimGameState
from alvinatlas.core.minimax import Minimax

class TestMinimax(unittest.TestCase):
    """
    tests minimax algo
    """

    def test_minimax_algo_3(self):
        """
        tests simplest winning condition
        given condition - 3, best state - 1
        """
        game_state = SimpleNimGameState(3)
        minimax = Minimax(-1, 1)        

        self.assertEqual(minimax.get_best_gamestate(game_state), (1, SimpleNimGameState(1)) )

    def test_minimax_algo_6(self):
        """
        tests simplest winning condition
        given condition - 6, best state - 5
        """
        game_state = SimpleNimGameState(6)
        minimax = Minimax(-1, 1)        

        self.assertEqual(minimax.get_best_gamestate(game_state), (1, SimpleNimGameState(5)) )

    def test_minimax_algo_5(self):
        """
        tests simplest winning condition(losing in this case)
        given condition - 5, best state - 4
        """
        game_state = SimpleNimGameState(5)
        minimax = Minimax(-1, 1)        

        self.assertEqual(minimax.get_best_gamestate(game_state), (-1, SimpleNimGameState(4)) )


if __name__ == '__main__':
    unittest.main()