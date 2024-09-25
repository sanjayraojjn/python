import unittest
import sys
from dataclasses import dataclass
from contextlib import redirect_stdout
import io

from alvinatlas.core.exceptions import GameOver
from alvinatlas.core.tests.threading import ThreadWithReturnValue

from alvinatlas.nim.game.player import Player, ComputerRandomPlayer, \
    ConsolePlayer, MinimaxComputerPlayer
from alvinatlas.nim.logic.models import NimBoard, \
    Counter, GameState as NimGameState, PileIndex, Move
from alvinatlas.nim.logic.exceptions import InvalidMove

@dataclass
class WrappedException:
    excep: Exception

def wrapper_function(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as exp:
        return WrappedException(exp)

class TestPlayer(unittest.TestCase):
    """
    test cases for testing NIM players base class
    """

    def test_player_creation(self)->None:
        """
        test creation of players
        """
        abs_player = Player()

class TestComputerRandomPlayer(unittest.TestCase):
    """
    test cases for computer random player
    """

    def test_player_creation(self)->None:
        """
        test creation of random computer players
        """
        random_player = ComputerRandomPlayer()

    def test_randomplayer_move(self)->None:
        """
        test a few random moves of random player
        """
        #test-1
        board = NimBoard( ( Counter(4), Counter(5) ) )
        game_state = NimGameState(board)

        random_player = ComputerRandomPlayer()
        self.assertTrue(random_player.get_move(game_state) in game_state.possible_moves)

    def test_randomplayer_makemove(self)->None:
        """
        test random player's makemove 
        """
        #test-1
        board = NimBoard( ( Counter(4), Counter(5) ) )
        game_state = NimGameState(board)

        random_player = ComputerRandomPlayer()
        self.assertTrue(random_player.make_move(game_state) in game_state.possible_next_states)

    def test_randomplayer_makemove_negative_cases(self)->None:
        """
        test random player's makemove negative cases
        """
        #test-1
        board = NimBoard( ( Counter(0), Counter(0) ) )
        game_state = NimGameState(board)

        random_player = ComputerRandomPlayer()
        with self.assertRaises(GameOver, msg="no more moves possible"):
            random_player.make_move(game_state)

class TestConsolePlayer(unittest.TestCase):
    """
    test case for console player
    """

    def test_player_creation(self)->None:
        """
        test creation of console players
        """
        console_player = ConsolePlayer()

    def test_consoleplayer_getmove(self)->None:
        """
        test get move of the console player
        """
        sout = io.StringIO()
        with redirect_stdout(sout):
            #first move #1
            board = NimBoard( ( Counter(4), Counter(5) ) )
            game_state = NimGameState(board)

            console_player = ConsolePlayer()

            oldstdin = sys.stdin

            #1st move        
            sys.stdin = io.StringIO('1 3\n')
            th = ThreadWithReturnValue(target=console_player.get_move, args=(game_state, ))
            th.start()
            #sys.stdin.write("1 3\n")
            move = th.join()

            #expected board
            expected_board = NimBoard( ( Counter(1), Counter(5) ) )
            expected_gamestate = NimGameState(expected_board)
            expected_move = Move(Counter(3), PileIndex(1), game_state, expected_gamestate)

            self.assertEqual(move, expected_move)

        #print(s := sout.getvalue())

        sout = io.StringIO()

        with redirect_stdout(sout):
            #second move#2
            game_state = expected_gamestate
            sys.stdin = io.StringIO('1 1\n')
            th = ThreadWithReturnValue(target=console_player.get_move, args=(game_state, ))
            th.start()
            #sys.stdin.write("1 3\n")
            move = th.join()

            #revert to old stdin
            sys.stdin = oldstdin

            #expected board
            expected_board = NimBoard( ( Counter(0), Counter(5) ) )
            expected_gamestate = NimGameState(expected_board)
            expected_move = Move(Counter(1), PileIndex(1), game_state, expected_gamestate)

            self.assertEqual(move, expected_move)
        #print(s := sout.getvalue())

    def test_consoleplayer_getmove_negative_cases(self)->None:
        """
        test few negative cased of get move of the console player
        """
        sout = io.StringIO()
        with redirect_stdout(sout):
            #pile-1 does not allow any move
            board = NimBoard( ( Counter(0), Counter(5) ) )
            game_state = NimGameState(board)

            console_player = ConsolePlayer()

            oldstdin = sys.stdin

            #1st move        
            sys.stdin = io.StringIO('1 1\n')
            th = ThreadWithReturnValue(target=wrapper_function, args=(console_player.get_move, game_state, ))
            th.start()
            move = th.join()

            #revert to old stdin
            sys.stdin = oldstdin

            #this input should have raised an exception("InvalidMove")
            self.assertTrue(isinstance(move, WrappedException))
            self.assertTrue(isinstance(move.excep, InvalidMove))
        #print(s := sout.getvalue())

    def test_consoleplayer_makemove(self)->None:
        """
        test make move of console player
        """
        sout = io.StringIO()
        with redirect_stdout(sout):
            #valid move
            board = NimBoard( ( Counter(4), Counter(5) ) )
            game_state = NimGameState(board)

            console_player = ConsolePlayer()

            oldstdin = sys.stdin

            #1st move        
            sys.stdin = io.StringIO('1 4\n')
            th = ThreadWithReturnValue(target=console_player.make_move, args=(game_state, ))
            th.start()
            new_gamestate = th.join()

            #revert to old stdin
            sys.stdin = oldstdin

            #expected board
            expected_board = NimBoard( ( Counter(0), Counter(5) ) )
            expected_gamestate = NimGameState(expected_board)

            self.assertEqual(new_gamestate, expected_gamestate)

        #print(s := sout.getvalue())

    def test_consoleplayer_makemove_negative_cases(self)->None:
        """
        test make move of console player
        """
        sout = io.StringIO()
        with redirect_stdout(sout):
            #pile-1 does not allow any move
            board = NimBoard( ( Counter(0), Counter(5) ) )
            game_state = NimGameState(board)

            console_player = ConsolePlayer()

            oldstdin = sys.stdin

            #1st invalid move(1st pile does not have any counter left)
            sys.stdin = io.StringIO('1 1\n')
            th = ThreadWithReturnValue(target=wrapper_function, args=(console_player.make_move, game_state, ))
            th.start()
            new_gamestate = th.join()

            #revert to old stdin
            sys.stdin = oldstdin

            #this input should have raised an exception("InvalidMove")
            self.assertTrue(isinstance(new_gamestate, WrappedException))
            self.assertTrue(isinstance(new_gamestate.excep, InvalidMove))

            #next invalid move(there are only 2 piles)
            sys.stdin = io.StringIO('3 1\n')
            th = ThreadWithReturnValue(target=wrapper_function, args=(console_player.make_move, game_state, ))
            th.start()
            new_gamestate = th.join()

            #revert to old stdin
            sys.stdin = oldstdin

            #this input should have raised an exception("InvalidMove")
            self.assertTrue(isinstance(new_gamestate, WrappedException))
            self.assertTrue(isinstance(new_gamestate.excep, InvalidMove))

        #print(s := sout.getvalue())        

class TestMiniMaxPlayer(unittest.TestCase):
    """
    test case for minimax computer player
    """

    def test_minimaxplayer_creation(self)->None:
        """
        test creation of minimax computer players
        """
        minimax_player = MinimaxComputerPlayer()

    def test_minimaxplayer_getmove(self)->None:
        """
        test getmove of minimax player
        """
        #test-1
        board = NimBoard( ( Counter(4), Counter(5) ) )
        game_state = NimGameState(board)

        minimax_player = MinimaxComputerPlayer()

        #expected board
        expected_board = NimBoard( ( Counter(4), Counter(4) ) )
        expected_gamestate = NimGameState(expected_board)
        expected_move = Move(Counter(1), PileIndex(2), game_state, expected_gamestate)

        self.assertEqual(minimax_player.get_move(game_state), expected_move)

        #test-2
        board = NimBoard( ( Counter(6), ) )
        game_state = NimGameState(board)

        #expected board
        expected_board = NimBoard( ( Counter(1), ) )
        expected_gamestate = NimGameState(expected_board)
        expected_move = Move(Counter(5), PileIndex(1), game_state, expected_gamestate)

        self.assertEqual(minimax_player.get_move(game_state), expected_move)

    def test_minimaxplayer_getmove_negative_cases(self)->None:
        """
        test getmove of minimax player with a few negative cases
        """
        #test-1
        board = NimBoard( ( Counter(0), Counter(1) ) )
        game_state = NimGameState(board)

        minimax_player = MinimaxComputerPlayer()

        #expected board
        expected_board = NimBoard( ( Counter(0), Counter(0) ) )
        expected_gamestate = NimGameState(expected_board)
        expected_move = Move(Counter(1), PileIndex(2), game_state, expected_gamestate)

        self.assertEqual(minimax_player.get_move(game_state), expected_move)

    def test_minimaxplayer_makemove(self)->None:
        """
        test makemove method of minimaxcomputer player
        """
        #test-1
        board = NimBoard( ( Counter(4), Counter(5) ) )
        game_state = NimGameState(board)

        minimax_player = MinimaxComputerPlayer()

        #expected board
        expected_board = NimBoard( ( Counter(4), Counter(4) ) )
        expected_gamestate = NimGameState(expected_board)
        #expected_move = Move(Counter(1), PileIndex(2), game_state, expected_gamestate)

        self.assertEqual(minimax_player.make_move(game_state), expected_gamestate)

    def test_minimaxplayer_makemove_negative_cases(self)->None:
        """
        test random player's makemove negative cases
        """
        #test-1
        board = NimBoard( ( Counter(0), Counter(0) ) )
        game_state = NimGameState(board)

        minimax_player = MinimaxComputerPlayer()
        with self.assertRaises(GameOver, msg="no more moves possible"):
            minimax_player.make_move(game_state)

        #test-2
        board = NimBoard( ( Counter(1), Counter(0) ) )
        game_state = NimGameState(board)

        minimax_player = MinimaxComputerPlayer()

        #expected board
        expected_board = NimBoard( ( Counter(0), Counter(0) ) )
        expected_gamestate = NimGameState(expected_board)
        
        self.assertEqual(minimax_player.make_move(game_state), expected_gamestate)

    def test_minimaxplayer_align_gamestate(self)->None:
        """
        test align_gamestate method of minimax computer player
        """
        #test-1

        #gamestate
        board = NimBoard( ( Counter(2), Counter(0), Counter(2), Counter(0) ) )
        game_state = NimGameState(board)

        #best gamestate
        board_align_to = NimBoard( ( Counter(0), Counter(0), Counter(1), Counter(2) ) )
        game_state_align_to = NimGameState(board_align_to)

        #aligned gamestate
        board_aligned_expected = NimBoard( ( Counter(2), Counter(0), Counter(1), Counter(0) ) )
        game_state_aligned_expected = NimGameState(board_aligned_expected)

        minimax_player = MinimaxComputerPlayer()
        self.assertEqual( minimax_player._align_gamestate(game_state, game_state_align_to), \
                         game_state_aligned_expected)

        #test-2

        #gamestate
        board = NimBoard( ( Counter(6), ) )
        game_state = NimGameState(board)

        #best gamestate
        board_align_to = NimBoard( ( Counter(1), ) )
        game_state_align_to = NimGameState(board_align_to)

        #aligned gamestate
        board_aligned_expected = NimBoard( ( Counter(1),  ) )
        game_state_aligned_expected = NimGameState(board_aligned_expected)

        minimax_player = MinimaxComputerPlayer()
        self.assertEqual( minimax_player._align_gamestate(game_state, game_state_align_to), \
                         game_state_aligned_expected)

    def test_minimaxplayer_align_gamestate_negative_cases(self)->None:
        """
        test negative test cases of align_gamestate method of minimax computer player
        """
        #test-1

        #gamestate
        board = NimBoard( ( Counter(2), Counter(0), Counter(2), Counter(0) ) )
        game_state = NimGameState(board)

        #best gamestate
        board_align_to = NimBoard( ( Counter(0), Counter(2), Counter(1), Counter(2) ) )
        game_state_align_to = NimGameState(board_align_to)

        #aligned gamestate
        board_aligned_expected = NimBoard( ( Counter(2), Counter(0), Counter(1), Counter(0) ) )
        game_state_aligned_expected = NimGameState(board_aligned_expected)

        minimax_player = MinimaxComputerPlayer()

        #minimax_player._align_gamestate(game_state, game_state_align_to)
        with self.assertRaises(InvalidMove, msg="game states cannot be aligned"):
            minimax_player._align_gamestate(game_state, game_state_align_to)

        #test-2

        #gamestate
        board = NimBoard( ( Counter(2), Counter(0), Counter(2), Counter(0) ) )
        game_state = NimGameState(board)

        #best gamestate
        board_align_to = NimBoard( ( Counter(0), Counter(1), Counter(1), Counter(0) ) )
        game_state_align_to = NimGameState(board_align_to)

        #aligned gamestate
        board_aligned_expected = NimBoard( ( Counter(2), Counter(0), Counter(1), Counter(0) ) )
        game_state_aligned_expected = NimGameState(board_aligned_expected)

        minimax_player = MinimaxComputerPlayer()

        #minimax_player._align_gamestate(game_state, game_state_align_to)
        with self.assertRaises(InvalidMove, msg="game states cannot be aligned"):
            minimax_player._align_gamestate(game_state, game_state_align_to)
