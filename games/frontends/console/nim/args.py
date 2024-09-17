import argparse
from typing import NamedTuple

from alvinatlas.nim.game.player import Player, \
    ConsolePlayer, ComputerRandomPlayer, MinimaxComputerPlayer

PLAYER_CLASSES = {
    "human": ConsolePlayer,
    "random": ComputerRandomPlayer,
    "minimax": MinimaxComputerPlayer,
}

class Args(NamedTuple):
    player1: Player
    player2: Player
    current_player: Player

def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-1",
        dest="player_1",
        choices=PLAYER_CLASSES.keys(),
        default="human"
    )
    parser.add_argument(
        "-2",
        dest="player_2",
        choices=PLAYER_CLASSES.keys(),
        default="minimax"
    )
    parser.add_argument(
        "--start",
        dest="starting_player",
        choices=[1, 2],
        type=int,
        default="1"
    )
    args = parser.parse_args()

    player1 = PLAYER_CLASSES[args.player_1]()
    player2 = PLAYER_CLASSES[args.player_2]()

    print(args.player_1, args.player_2)

    if args.starting_player is 1:
        starting_player = player1
    else:
        starting_player = player2

    return Args(player1, player2, starting_player)
