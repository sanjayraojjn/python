from alvinatlas.nim.game.engine import Nim as NimEngine
from alvinatlas.nim.game.renderer import ConsoleRenderer

from .args import parse_args


def main() -> None:
    player1, player2, starting_player = parse_args()
    NimEngine(player1, player2, ConsoleRenderer(), starting_player ).play([100, 100])
