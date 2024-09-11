from dataclasses import dataclass
from functools import cached_property, cache
from typing import TYPE_CHECKING

from validators import validate_counter, validate_pile_index, validate_move, validate_board
from atlas_core.core.models import GameState as CoreGameState
#if TYPE_CHECKING:
#    from atlas_core.nim.game.player import Player

@dataclass(frozen=True)
class Counter(int):
    def __post_init__(self)->None:
        #validate counter value
        validate_counter(self)

@dataclass(frozen=True)
class PileIndex(int):
    def __post_init__(self)->None:
        #validate pile number
        validate_pile_index(self)

    @cached_property
    def array_index(self)->int:
        return self - 1

@dataclass(frozen=True)
class NimBoard:
    piles: tuple[Counter]

    def __post_init__(self):
        validate_board(self)

    @cached_property
    def num_piles(self):
        return len(self.piles)
    
    @cached_property
    def total_counter(self):
        return sum(self.piles)
    
    def __repr__(self):
        return f"--{self.piles}--"

@dataclass(frozen=True)
class GameState(CoreGameState):
    board: NimBoard           #game board
    #next_player: Player      #whose turn is next

    @cache
    def possible_moves(self)->list["Move"]:
        result = []
        for idx, pile in enumerate(self.board.piles):
            for counter in range(1, pile):
                next_move = Move(Counter(counter), PileIndex(idx+1), \
                                 self, \
                                 GameState(NimBoard( self.board.piles[:idx] + (self.board.piles[idx] - counter, ) + self.board.piles[idx+1: ] ))   )
                result.append[next_move]
        return result
                
    @cache
    def possible_next_states(self)->list["GameState"]:
        result = []
        for idx, pile in enumerate(self.board.piles):
            for counter in range(1, pile):
                next_state = GameState(NimBoard( self.board.piles[:idx] + (self.board.piles[idx] - counter, ) + self.board.piles[idx+1: ] ))
                result.append[next_state]
        return result
                
    @cached_property
    def game_over(self)->bool:
        return not any(self.board.piles)
    
    @cache
    def score(self)->int|None:
        if not any(self.board.piles):
            return 1

@dataclass(frozen=True)
class Move:
    counter: Counter
    pile: PileIndex
    before_state: GameState
    after_state: GameState

    def __post_init__(self):
        validate_move(self)


