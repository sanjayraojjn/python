import unittest
from functools import cache
from dataclasses import dataclass

from alvinatlas.core.models import GameState, Move, SimpleNimGameState
from alvinatlas.core.exceptions import InvalidCounter

class TestModels(unittest.TestCase):

    def test_gamestate_counter(self):
        """
        tests game state counter values
        """
        with self.assertRaises(InvalidCounter, msg="Simple nim counter must not allow -1"):
            SimpleNimGameState(-1)
        with self.assertRaises(InvalidCounter, msg="Simple nim counter must not allow -100"):
            SimpleNimGameState(-100)

    def test_gamestate_possible_next_state(self):
        """
        tests possible next states for the given game states
        """
        game_state = SimpleNimGameState(6)
        
        self.assertEqual(game_state.possible_next_states, \
                         [ SimpleNimGameState(5), SimpleNimGameState(4), SimpleNimGameState(3) ], \
                            "next states must be 5,4,3 for 6")
        
        game_state = SimpleNimGameState(3)     
        self.assertEqual(game_state.possible_next_states, \
                         [ SimpleNimGameState(2), SimpleNimGameState(1), SimpleNimGameState(0) ], \
                            "next states must be 2,1,0 for 3")

        
    # def test_gamestate_score(self):
    #     """
    #     tests score of given game state
    #     """
    #     game_state = SimpleNimGameState(0)
    #     self.assertEqual( game_state.score, 1, "Score must be 1 when counter reaches zero {game_state}")

    #     game_state = SimpleNimGameState(1)
    #     self.assertIsNone( game_state.score, f"Score must be 0 when counter is not zero {game_state}"), 

    #     game_state = SimpleNimGameState(5)
    #     self.assertEqual( game_state.score, 0, f"Score must be 0 when counter is not zero {game_state}"), 

    def test_gamestate_game_over(self):
        """
        tests game over flag
        """
        game_state = SimpleNimGameState(0)
        self.assertTrue(game_state.game_over, \
                        "game must be over after counter reaches 0 in simple nim")

        game_state = SimpleNimGameState(1)
        self.assertFalse(game_state.game_over, \
                         "game state must not indicate game over if counter is more than 0 in simple nim")

if __name__ == "__main__":
    unittest.main()


