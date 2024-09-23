import unittest
import random
from contextlib import redirect_stdout
import io

from alvinatlas.nim.logic.models import GameState as NimGameState
from alvinatlas.nim.logic.models import Counter, PileIndex, NimBoard, Move
from alvinatlas.nim.logic.exceptions import InvalidCounter, InvalidPileIndex

from alvinatlas.nim.game.player import ComputerRandomPlayer
from alvinatlas.nim.game.engine import Nim as NimEngine
from alvinatlas.nim.game.renderer import ConsoleRenderer
from alvinatlas.nim.game.exceptions import InvalidRenderer, BothPlayerSame, \
    InvalidCurrentPlayer, InvalidPlayer

class TestNimEngine(unittest.TestCase):

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


    def test_engine(self)->None:
        """
        setup 10 random NIM games between random computer players and tests the game engine
        """
        random.seed(675675)
        for i in range(10):
            player1 = ComputerRandomPlayer()
            player2 = ComputerRandomPlayer()
            current_player = player1
            renderer = ConsoleRenderer()

            engine = NimEngine(player1, player2, renderer, player1)
            f = io.StringIO()
            with redirect_stdout(f):
                engine.play()
            s = f.getvalue()

            


