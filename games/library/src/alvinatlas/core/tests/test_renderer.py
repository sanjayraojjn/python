from contextlib import redirect_stdout
import io
import unittest

from alvinatlas.core.renderer import blink, clear_screen



class TestRenderer(unittest.TestCase):
    """
    tests core rendering functions
    """

    def test_renderer_blink(self)->None:
        """
        tests blink function
        """
        #f = io.StringIO()
        #with redirect_stdout(f):
        #    blink("abcd")
        #s = f.getvalue()
        self.assertEqual(blink("abcd"), f"\033[5mabcd\033[0m")

    def test_clearscreen(self)->None:
        """
        tests clear screen function
        """
        f = io.StringIO()
        with redirect_stdout(f):
            clear_screen()
        s = f.getvalue()
        self.assertEqual(s, "\033c")



