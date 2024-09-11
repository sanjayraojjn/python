from functools import cache

from dataclasses import dataclass

@dataclass(frozen=True)
class GameState:
    
    @cache
    def possible_moves(self)->list["Move"]:
        """to be implemented by subclass"""
    
    @cache
    def possible_next_states(self)->list["GameState"]:
        """"""

    @cache
    def game_over(self)->bool:
        """to be implemented by subclass"""

    @cache
    def score(self)->int:
        """to be implemented by subclass"""


@dataclass(frozen=True)
class Move:
    before_state: GameState
    after_state: GameState

