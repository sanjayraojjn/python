import unittest
import random
from contextlib import redirect_stdout
import io
import sys
import time

from alvinatlas.core.utils import timer

from alvinatlas.nim.game.player import ComputerRandomPlayer, ConsolePlayer, MinimaxComputerPlayer
from alvinatlas.nim.game.engine import Nim as NimEngine
from alvinatlas.nim.game.renderer import ConsoleRenderer
from alvinatlas.nim.game.exceptions import InvalidRenderer, BothPlayerSame, \
    InvalidCurrentPlayer, InvalidPlayer

class TestNimEngine(unittest.TestCase):

    maxDiff = None

    def test_engine_creation(self)->None:
        """
        test various error condition in engine creation
        """
        player1 = ComputerRandomPlayer()
        player2 = ComputerRandomPlayer()
        player3 = ComputerRandomPlayer()
        renderer = ConsoleRenderer()

        #valid engine creation
        NimEngine(player1, player2, renderer, player1)

        #test both players same
        with self.assertRaises(BothPlayerSame, msg="both players are same"):
            NimEngine(player1, player1, "", player1)

        #test invalid current player
        with self.assertRaises(InvalidCurrentPlayer, msg="current player is not a player"):
            NimEngine(player1, player2, renderer, player3)

        #test invalid player1
        with self.assertRaises(InvalidPlayer, msg="Player1 is not set"):
            NimEngine(None, player2, renderer, player2)

        #test invalid player2
        with self.assertRaises(InvalidPlayer, msg="Player2 is not set"):
            NimEngine(player1, None, renderer, player1)

        #test invalid current player
        with self.assertRaises(InvalidCurrentPlayer, msg="Player2 is not set"):
            NimEngine(player1, player2, renderer, None)

        #test invalid renderer
        with self.assertRaises(InvalidRenderer, msg="renderer not provided"):
            NimEngine(player1, player2, "", player1)


    def test_engine_play_random(self)->None:
        """
        setup 10 random NIM games between random computer players and tests the game engine
        """
        winners = ["player1", "player2", "player1", "player2", "player1", \
                   "player1", "player1", "player2", "player2", "player1"]
        random.seed(675675)
        for i in range(10):
            player1 = ComputerRandomPlayer()
            player2 = ComputerRandomPlayer()
            current_player = player1
            renderer = ConsoleRenderer()

            engine = NimEngine(player1, player2, renderer, current_player)
            f = io.StringIO()
            with redirect_stdout(f):
                winner = engine.play()
            s = f.getvalue()
            winner = "player1" if winner is player1 else "player2"
            #print(f"winner is {winner}")
            #print(f"game# {i+1} random-random")
            self.assertTrue(winner == winners[i], msg=f"winner is not as expected")

    @timer
    def test_engine_play_minimax(self)->None:
        """
        tests 10 random games between two minimax players
        """
        t_start = time.perf_counter()
        winners = ["player2", "player2", "player2", "player2", "player2", \
                   "player1", "player2", "player2", "player1", "player2"]
        random.seed(675675)
        for i in range(10):
            player1 = MinimaxComputerPlayer()
            player2 = MinimaxComputerPlayer()
            current_player = player1
            renderer = ConsoleRenderer()

            engine = NimEngine(player1, player2, renderer, current_player)
            f = io.StringIO()
            with redirect_stdout(f):
                winner = engine.play()
            s = f.getvalue()
            winner = "player1" if winner is player1 else "player2"
            #print(f"winner is {winner}")
            self.assertTrue(winner == winners[i], msg=f"winner is not as expected")
            #print(f"game# {i+1} minimax-minimax")
        t_end = time.perf_counter()

        self.assertLessEqual(t_end - t_start, 12, msg="time taken is more than 12 seconds")


    def test_engine_play_1(self)->None:
        """
        setup a NIM game between one human and another minimax player 
        and tests the game engine
        """
        player1 = ConsolePlayer()
        player2 = MinimaxComputerPlayer()
        current_player = player1
        renderer = ConsoleRenderer()

        human_input = "5\n"
        oldstdin = sys.stdin
        sys.stdin = io.StringIO(human_input)

        engine = NimEngine(player1, player2, renderer, current_player)
        f = io.StringIO()
        with redirect_stdout(f):
            engine.play([6])
        s = f.getvalue()

        sys.stdin = oldstdin

        expected_output = "########################\n" + \
            "6[" + ("\N{circled times} " * 6) + ']\n\n' + \
            "enter your move# " + \
            "########################\n" + \
            "1[" + ("\N{circled times} " * 1) + ']\n\n' + \
            "########################\n" + \
            "0[]\n\n"
            
        self.assertEqual(s, expected_output, msg=f"Output of engine play with human_input{human_input} is not as expected")

    def test_engine_play_2(self)->None:
        """
        setup a NIM game between one human and another minimax player 
        and tests the game engine
        """
        player1 = ConsolePlayer()
        player2 = MinimaxComputerPlayer()
        current_player = player1
        renderer = ConsoleRenderer()

        human_input = "2 3\n1 1\n1 1\n"

        oldstdin = sys.stdin
        sys.stdin = io.StringIO(human_input)

        engine = NimEngine(player1, player2, renderer, current_player)
        f = io.StringIO()
        with redirect_stdout(f):
            engine.play([4, 5])
        s = f.getvalue()

        sys.stdin = oldstdin

        expected_output = "########################\n" + \
            "4[" + ("\N{circled times} " * 4) + ']\n' + "5[" + ("\N{circled times} " * 5) + ']\n\n' +\
            "enter your move#(pile counter) space-separated: " + \
            "########################\n" + \
            "4[" + ("\N{circled times} " * 4) + ']\n' + "2[" + ("\N{circled times} " * 2) + ']\n\n' +\
            "########################\n" + \
            "2[" + ("\N{circled times} " * 2) + ']\n' + "2[" + ("\N{circled times} " * 2) + ']\n\n' +\
            "enter your move#(pile counter) space-separated: " + \
            "########################\n" + \
            "1[" + ("\N{circled times} " * 1) + ']\n' + "2[" + ("\N{circled times} " * 2) + ']\n\n' +\
            "########################\n" + \
            "1[" + ("\N{circled times} " * 1) + ']\n' + "0[]\n\n" +\
            "enter your move#(pile counter) space-separated: " + \
            "########################\n" + \
            "0[]\n" + "0[]\n\n"
            
        self.assertEqual(s, expected_output, msg=f"Output of engine play with human_input{human_input} is not as expected")

            


