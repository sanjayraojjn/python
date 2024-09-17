import unittest
import random

from alvinatlas.nim.logic.models import GameState as NimGameState
from alvinatlas.nim.logic.models import Counter, PileIndex, NimBoard, Move
from alvinatlas.nim.logic.exceptions import InvalidCounter, InvalidPileIndex

from alvinatlas.nim.game.player import ComputerRandomPlayer
from alvinatlas.nim.game.engine import Nim as NimEngine
from alvinatlas.nim.game.renderer import ConsoleRenderer

class TestNimEngine(unittest.TestCase):

    def test_engine(self)->None:
        """
        setup 10 random NIM games between random computer players ans tests the game engine
        """
        random.seed(675675)
        for i in range(10):
            player1 = ComputerRandomPlayer()
            player2 = ComputerRandomPlayer()
            current_player = player1
            renderer = ConsoleRenderer()

            engine = NimEngine(player1, player2, renderer, player1)
            engine.play()

            


