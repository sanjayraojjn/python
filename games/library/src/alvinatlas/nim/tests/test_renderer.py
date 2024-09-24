import unittest
from contextlib import redirect_stdout
import io

from alvinatlas.nim.game.renderer import ConsoleRenderer
from alvinatlas.nim.logic.models import GameState as NimGameState, NimBoard, Counter

class TestConsoleRenderer(unittest.TestCase):
    """
    tests console renderer
    """

    def test_consolerenderer_creation(self)->None:
        """
        test creation of console renderer
        """
        console_renderer = ConsoleRenderer()

    def test_consolerender_render(self)->None:
        """
        test render method of console renderer
        """
        board = NimBoard( ( Counter(4), Counter(5) ) )
        game_state = NimGameState(board)

        sout = io.StringIO()

        with redirect_stdout(sout):
            console_renderer = ConsoleRenderer()
            console_renderer.render(game_state)
        
        console_output = sout.getvalue()

        #expected_output = ("4[" + f"\N{circled times} " * 4) + ']\n' + "5[" + (f"\N{circled times} " * 5) + ']\n'
        expected_output = "########################\n" + \
            "4[" + ("\N{circled times} " * 4) + ']\n' + \
            "5[" + ("\N{circled times} " * 5) + ']\n' + \
            "\n"

        self.assertEqual(console_output, expected_output, 
                         msg="Output of console renderer is not as expected")
