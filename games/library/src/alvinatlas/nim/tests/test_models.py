import unittest

from alvinatlas.nim.logic.models import GameState as NimGameState
from alvinatlas.nim.logic.models import Counter
from alvinatlas.nim.logic.exceptions import InvalidCounter
import unittest
from alvinatlas.nim.logic.models import GameState as NimGameState
from alvinatlas.nim.logic.models import Counter, PileIndex
from alvinatlas.nim.logic.exceptions import InvalidCounter, InvalidPileIndex

class TestCounter(unittest.TestCase):

    def test_counter_values(self):
        """
        tests different values of the counter
        """
        #larger values
        self.assertEqual(100, (counter := Counter(100) ) )
        #min values
        self.assertEqual(1, (counter := Counter(1) ) )
        self.assertEqual(0, (counter := Counter(0) ) )
        #Counter(-1)
        #negative cases
        with self.assertRaises(InvalidCounter, msg="counter must not allow less than zero"):
            counter = Counter(-1)
        with self.assertRaises(InvalidCounter, msg="counter must not allow less than zero"):
            counter = Counter(-100)
        
    def test_counter_value_types(self):
        """
        test counter value types
        """
        with self.assertRaises(ValueError, msg="counter must be integer type only, not string"):
            counter = Counter("abc")
        with self.assertRaises(InvalidCounter, msg="counter must be integer type only, not float/double"):
            counter = Counter(11.5)

class TestPileIndex(unittest.TestCase):

    def test_pile_index_values(self):
        """
        tests different values of the pile index
        """
        # larger values
        self.assertEqual(10, (pile_index := PileIndex(10)))
        # larger values
        self.assertEqual(1, (pile_index := PileIndex(1)))
        # min values
        with self.assertRaises(InvalidPileIndex, msg="pile index must be greater than zero"):
            pile_index = PileIndex(0)
        # negative cases
        with self.assertRaises(InvalidPileIndex, msg="pile index must not allow less than zero"):
            pile_index = PileIndex(-1)
        with self.assertRaises(InvalidPileIndex, msg="pile index must not allow less than zero"):
            pile_index = PileIndex(-100)

    def test_pile_index_value_types(self):
        """
        test pile index value types
        """
        with self.assertRaises(ValueError, msg="pile index must be integer type only, not string"):
            pile_index = PileIndex("abc")
        with self.assertRaises(InvalidPileIndex, msg="pile index must be integer type only, not float/double"):
            pile_index = PileIndex(11.5)

if __name__ == "__main__":
    unittest.main()


# class TestBoard(unittest.TestCase):
#     """Test board positions"""

# class TestModels(unittest.TestCase):

#     def test_gamestate_counter(self):
#         """
#         tests game state counter values
#         """
#         with self.assertRaises(InvalidCounter, msg="Simple nim counter must not allow -1"):
#             SimpleNimGameState(-1)
#         with self.assertRaises(InvalidCounter, msg="Simple nim counter must not allow -100"):
#             SimpleNimGameState(-100)

#     def test_gamestate_possible_next_state(self):
#         """
#         tests possible next states for the given game states
#         """
#         game_state = SimpleNimGameState(6)
        
#         self.assertEqual(game_state.possible_next_states, \
#                          [ SimpleNimGameState(5), SimpleNimGameState(4), SimpleNimGameState(3) ], \
#                             "next states must be 5,4,3 for 6")
        
#         game_state = SimpleNimGameState(3)     
#         self.assertEqual(game_state.possible_next_states, \
#                          [ SimpleNimGameState(2), SimpleNimGameState(1), SimpleNimGameState(0) ], \
#                             "next states must be 2,1,0 for 3")

        
#     def test_gamestate_score(self):
#         """
#         tests score of given game state
#         """
#         game_state = SimpleNimGameState(0)
#         self.assertEqual( game_state.score, 1, "Score must be 1 when counter reaches zero {game_state}")

#         game_state = SimpleNimGameState(1)
#         self.assertEqual( game_state.score, 0, f"Score must be 0 when counter is not zero {game_state}"), 

#         game_state = SimpleNimGameState(5)
#         self.assertEqual( game_state.score, 0, f"Score must be 0 when counter is not zero {game_state}"), 

#     def test_gamestate_gameover(self):
#         """
#         tests game over flag
#         """
#         game_state = SimpleNimGameState(0)
#         self.assertTrue(game_state.game_over, \
#                         "game must be over after counter reaches 0 in simple nim")

#         game_state = SimpleNimGameState(1)
#         self.assertFalse(game_state.game_over, \
#                          "game state must not indicate game over if counter is more than 0 in simple nim")
        
#     def test_gamestate_score(self):
#         """
#         tests game score
#         """
#         game_state = SimpleNimGameState(0)
#         self.assertEqual(game_state.score, 1, "gamestate score must be 1 when counter is 0")

#         game_state = SimpleNimGameState(1)
#         self.assertIsNone(game_state.score, "gamestate score must be None when counter is greater than 0")

if __name__ == "__main__":
    unittest.main()

