from alvinatlas.core.renderer import Renderer

from alvinatlas.nim.logic.models import GameState, NimBoard, Counter


class ConsoleRenderer(Renderer):

    def render(self, game_state: GameState)->None:
        print("########################")
        print(game_state)


class GrpcClientRenderer(Renderer):

    def render(self, grpc_game_state)->None:
        board = NimBoard( [Counter(c) for c in grpc_game_state.piles ] )
        game_state = GameState(board)
        print("########################")
        print(game_state)
