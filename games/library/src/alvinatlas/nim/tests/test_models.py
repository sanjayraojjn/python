import unittest

from alvinatlas.nim.logic.models import GameState as NimGameState
from alvinatlas.nim.logic.models import Counter, PileIndex, NimBoard, Move
from alvinatlas.nim.logic.exceptions import InvalidCounter, InvalidPileIndex

class TestCounter(unittest.TestCase):

    def test_counter_values(self)->None:
        """
        tests different values of the counter
        """
        #larger values
        self.assertEqual(100, (counter := Counter(100) ) )
        #min values
        self.assertEqual(1, (counter := Counter(1) ) )
        self.assertEqual(0, (counter := Counter(0) ) )
        #Counter(-1)

    def test_counter_values_negative_cases(self)->None:
        #negative cases
        with self.assertRaises(InvalidCounter, msg="counter must not allow less than zero"):
            counter = Counter(-1)
        with self.assertRaises(InvalidCounter, msg="counter must not allow less than zero"):
            counter = Counter(-100)
        
    def test_counter_unsupported_value_types(self)->None:
        """
        test counter value types
        """
        with self.assertRaises(ValueError, msg="counter must be integer type only, not string"):
            counter = Counter("abc")
        with self.assertRaises(InvalidCounter, msg="counter must be integer type only, not float/double"):
            counter = Counter(11.5)

class TestPileIndex(unittest.TestCase):

    def test_pile_index_values(self)->None:
        """
        tests different values of the pile index
        """
        # larger values
        self.assertEqual(10, (pile_index := PileIndex(10)))
        self.assertEqual(9, pile_index.array_index)
        # smaller values
        self.assertEqual(1, (pile_index := PileIndex(1)))
        self.assertEqual(0, pile_index.array_index)

    def test_pile_index_values_negative_cases(self)->None:
        # min values
        with self.assertRaises(InvalidPileIndex, msg="pile index must be greater than zero"):
            pile_index = PileIndex(0)
        # negative cases
        with self.assertRaises(InvalidPileIndex, msg="pile index must not allow less than zero"):
            pile_index = PileIndex(-1)
        with self.assertRaises(InvalidPileIndex, msg="pile index must not allow less than zero"):
            pile_index = PileIndex(-100)

    def test_pile_index_value_types(self)->None:
        """
        test pile index value types
        """
        with self.assertRaises(ValueError, msg="pile index must be integer type only, not string"):
            pile_index = PileIndex("abc")
        with self.assertRaises(InvalidPileIndex, msg="pile index must be integer type only, not float/double"):
            pile_index = PileIndex(11.5)

class TestNimBoard(unittest.TestCase):
    """
    tests Nim board
    """

    def test_nimboard_creation(self)->None:
        """
        tests basic functionality of NimBoard
        """
        #postivie cases
        board = NimBoard( (Counter(5), Counter(10), Counter(3) ) )
        self.assertEqual(board.num_piles, 3, f"board length should be 3")
        self.assertEqual(board.total_counters, 18, "total counters should be 18")

    def test_nimboard_creation_negative_cases(self)->None:

        with self.assertRaises(InvalidCounter, msg="None of the counters in Nimboard can be less than zero"):
            board = NimBoard( (Counter(5), Counter(-1)) )

        with self.assertRaises(InvalidCounter, msg="NimBoard can have Counter type only"):
            board = NimBoard( (1,2,3) )

        with self.assertRaises(ValueError, msg="only tuple of Counter type allowed"):
            board = NimBoard( [Counter(5), Counter(10), Counter(3) ] )

class TestGameState(unittest.TestCase):
    """
    tests Nim Game state
    """

    def test_gamestate_creation(self)->None:
        """
        tests creation of new game state
        """
        board = NimBoard( ( Counter(5), Counter(10) ) )
        game_state = NimGameState(board)

    def test_gamestate_creation_negative_cases(self)->None:
        """
        negative test cases - tests creation of new game state
        """
        board = ( (1,2,3,4) )
        with self.assertRaises(ValueError, msg="Nim GameState can be created using NimBoard only"):
            game_state = NimGameState(board)

    def test_gamestate_possible_next_states(self)->None:
        """
        test possible next states of the given game state
        """
        #test-1
        board = NimBoard( ( Counter(4), Counter(5) ) )
        game_state = NimGameState(board)
        self.assertEqual(sorted(game_state.possible_next_states) , \
                         sorted( [ NimGameState( NimBoard( ( Counter(3), Counter(5)) ) ),
                         NimGameState( NimBoard( ( Counter(2), Counter(5)) ) ),
                         NimGameState( NimBoard( ( Counter(1), Counter(5)) ) ),
                         NimGameState( NimBoard( ( Counter(0), Counter(5)) ) ),
                         NimGameState( NimBoard( ( Counter(4), Counter(4)) ) ),
                         NimGameState( NimBoard( ( Counter(4), Counter(3)) ) ),
                         NimGameState( NimBoard( ( Counter(4), Counter(2)) ) ),
                         NimGameState( NimBoard( ( Counter(4), Counter(1)) ) ),
                         NimGameState( NimBoard( ( Counter(4), Counter(0)) ) ) ] ) )
        
        #test-2
        board = NimBoard( ( Counter(0), Counter(0), Counter(1) ) )
        game_state = NimGameState(board)
        self.assertEqual(sorted(game_state.possible_next_states) , \
                         sorted( [ NimGameState( NimBoard( ( Counter(0), Counter(0), Counter(0) ) ) ),
                                    ] ) )

    def test_gamestate_possible_next_states_negative_cases(self)->None:
        """
        test possible next states of the given game state
        """        
        #test-2
        board = NimBoard( ( Counter(0), Counter(0), Counter(0) ) )
        game_state = NimGameState(board)
        self.assertEqual(sorted(game_state.possible_next_states) , \
                         sorted( [ ] ) )

    def test_gamestate_possible_moves(self)->None:
        """
        test possible moves of the given game state
        """
        #test-1
        board = NimBoard( ( Counter(4), Counter(5) ) )
        game_state = NimGameState(board)

        self.assertEqual(game_state.possible_moves , \
                         [ 
                             Move( Counter(1), PileIndex(1), game_state, \
                                NimGameState( NimBoard( ( Counter(3), Counter(5)) ) ) ),
                             Move( Counter(2), PileIndex(1), game_state, \
                                NimGameState( NimBoard( ( Counter(2), Counter(5)) ) ) ),
                             Move( Counter(3), PileIndex(1), game_state, \
                                NimGameState( NimBoard( ( Counter(1), Counter(5)) ) ) ),
                             Move( Counter(4), PileIndex(1), game_state, \
                                NimGameState( NimBoard( ( Counter(0), Counter(5)) ) ) ),
                             Move( Counter(1), PileIndex(2), game_state, \
                                NimGameState( NimBoard( ( Counter(4), Counter(4)) ) ) ),
                             Move( Counter(2), PileIndex(2), game_state, \
                                NimGameState( NimBoard( ( Counter(4), Counter(3)) ) ) ),
                             Move( Counter(3), PileIndex(2), game_state, \
                                NimGameState( NimBoard( ( Counter(4), Counter(2)) ) ) ),
                             Move( Counter(4), PileIndex(2), game_state, \
                                NimGameState( NimBoard( ( Counter(4), Counter(1)) ) ) ),
                             Move( Counter(5), PileIndex(2), game_state, \
                                NimGameState( NimBoard( ( Counter(4), Counter(0)) ) ) ),
                          ] )
        
        #test-2
        board = NimBoard( ( Counter(0), Counter(0), Counter(1) ) )
        game_state = NimGameState(board)
        self.assertEqual(game_state.possible_moves , \
                         [ Move( Counter(1), PileIndex(3), game_state, \
                            NimGameState( NimBoard( ( Counter(0), Counter(0), Counter(0) ) ) ) ),
                                    ] )

    def test_gamestate_game_over(self)->None:
        """
        test game over
        """
        #test-1
        board = NimBoard( ( Counter(4), Counter(5) ) )
        game_state = NimGameState(board)
        self.assertFalse( game_state.game_over )
        #test-1
        board = NimBoard( ( Counter(0), Counter(0), Counter(1) ) )
        game_state = NimGameState(board)
        self.assertFalse( game_state.game_over )
        #test-1
        board = NimBoard( ( Counter(0), Counter(0) ) )
        game_state = NimGameState(board)
        self.assertTrue( game_state.game_over )




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

