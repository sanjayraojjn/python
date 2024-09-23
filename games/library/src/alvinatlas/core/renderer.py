import abc

from typing import Iterable

from alvinatlas.nim.logic.models import GameState

class Renderer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def render(self, game_state: GameState)->None:
        """
        renders the game state on screen
        """

def clear_screen()->None:
    print("\033c", end="")  #clears the screen upto start of the screen

def blink(text:str)->str:
    return f"\033[5m{text}\033[0m"


