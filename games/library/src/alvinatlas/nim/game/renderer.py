from alvinatlas.core.renderer import Renderer
from alvinatlas.nim.logic.models import GameState

class ConsoleRenderer(Renderer):

    def render(self, game_state: GameState)->None:
        print("########################")
        print(game_state)
        

