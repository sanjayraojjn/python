from functools import cache, cached_property
import typing

from alvinatlas.core.exceptions import InvalidCounter
#if typing.TYPE_CHECKING:
#    from alvinatlas.core.models import Move

from dataclasses import dataclass

@dataclass(frozen=True)
class GameState:
    
    @cached_property
    def possible_moves(self)->list["Move"]:
        """to be implemented by subclass"""
    
    @cached_property
    def possible_next_states(self)->list["GameState"]:
        """"""

    @cached_property
    def game_over(self)->bool:
        """to be implemented by subclass"""

    #@cached_property
    #def score(self)->int:
    #    """to be implemented by subclass"""

@dataclass(frozen=True)
class Move:
    before_state: GameState
    after_state: GameState


#######################################################
# sample implementations for testing
#######################################################


@dataclass(frozen=True)
class SimpleNimGameState(GameState):
    counter: int

    def __post_init__(self)->None:
        if self.counter < 0:
            raise InvalidCounter("counter value cannot go below zero")

    @cached_property
    def possible_moves(self)->list["Move"]:
        return [Move( before_state=self, \
                     after_state=GameState(self.counter-pick)) \
                        for pick in (1,2,3) if self.counter >= pick]
    
    @cached_property
    def possible_next_states(self)->list[GameState]:
        return [ SimpleNimGameState(self.counter - pick) for pick in (1,2,3) if self.counter >= pick ]

    @cached_property
    def game_over(self)->bool:
        return self.counter == 0
    
    def __hash__(self):
        return hash(self.counter)
    
    #@cached_property
    #def score(self)->int:
    #    return 1 if (self.counter == 0) else None
    
    def __eq__(self, another_game_state:GameState)->bool:
        return self.counter == another_game_state.counter
    
    def __ne__(self, another_game_state:GameState)->bool:
        return self.counter != another_game_state.counter
    
    def __gt__(self, another_game_state:GameState)->bool:
        return self.counter > another_game_state.counter
    
    def __lt__(self, another_game_state:GameState)->bool:
        return self.counter < another_game_state.counter
    
    def __ge__(self, another_game_state:GameState)->bool:
        return self.counter >= another_game_state.counter
    
    def __le__(self, another_game_state:GameState)->bool:
        return self.counter <= another_game_state.counter
    
    def __repr__(self):
        return f'{self.counter}[' + (f"\N{circled times} " * self.counter) + ']'

