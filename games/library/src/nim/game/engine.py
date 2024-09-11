from dataclasses import dataclass

from atlas_core.nim.game.player import Player

@dataclass(frozen=True)
class Nim:
    player1: Player
    player2: Player
    