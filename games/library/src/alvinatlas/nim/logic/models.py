from dataclasses import dataclass
from functools import cached_property, cache
from typing import TYPE_CHECKING

from alvinatlas.nim.logic.validators import validate_counter, \
    validate_pile_index, validate_move, validate_board, validate_gamestate
from alvinatlas.core.models import GameState as CoreGameState
from alvinatlas.core.exceptions import GameOver
#if TYPE_CHECKING:
#    from alvinatlas.nim.game.player import Player

#@dataclass(frozen=True)
class Counter(int):
    def __init__(self, *args, **kwargs):
        validate_counter(args[0])
        super(Counter, self).__init__()

class PileIndex(int):
    def __init__(self, *args, **kwargs):
        validate_pile_index(args[0])
        super(PileIndex, self).__init__()

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
    def total_counters(self):
        return sum(self.piles)
    
    def __repr__(self):
        out = f""
        for idx, pile in enumerate(self.piles):
            out = out + f'{idx} -> [' + (f"\N{circled times} " * pile) + f"] {pile}" + "\n"
        return out

@dataclass(frozen=True)
class GameState(CoreGameState):
    board: NimBoard           #game board
    #next_player: Player      #whose turn is next

    def __post_init__(self):
        validate_gamestate(self)

    @cached_property
    def possible_moves(self)->list["Move"]:
        if self.game_over:
            raise GameOver("No more moves possible")
        result = []
        for idx, pile in enumerate(self.board.piles):
            for counter in range(1, pile+1):
                next_move = Move(Counter(counter), PileIndex(idx+1), \
                                 self, \
                                 GameState(NimBoard( self.board.piles[:idx] + \
                                                ( Counter(self.board.piles[idx] - counter), ) + \
                                                    self.board.piles[idx+1: ] ))   )
                result.append(next_move)
        return result
                
    @cached_property
    def possible_next_states(self)->list["GameState"]:
        result = []
        for idx, pile in enumerate(self.board.piles):
            for counter in range(1, pile+1):
                next_state = GameState(NimBoard( self.board.piles[:idx] + \
                                                ( Counter(self.board.piles[idx] - counter), ) + \
                                                    self.board.piles[idx+1: ] ))
                result.append(next_state)
        return result
                
    @cached_property
    def game_over(self)->bool:
        return not any(self.board.piles)
    
    #@cached_property
    #def score(self)->int|None:
    #    if not any(self.board.piles):
    #        return 1
    
    def __eq__(self, another_game_state:"GameState")->bool:
        return sorted(self.board.piles) == sorted(another_game_state.board.piles)
    
    def __ne__(self, another_game_state:"GameState")->bool:
        return sorted(self.board.piles) != sorted(another_game_state.board.piles)
    
    def __gt__(self, another_game_state:"GameState")->bool:
        return self.board.total_counters > another_game_state.board.total_counters
    
    def __lt__(self, another_game_state:"GameState")->bool:
        return self.board.total_counters < another_game_state.board.total_counters
    
    def __ge__(self, another_game_state:"GameState")->bool:
        return self.board.total_counters >= another_game_state.board.total_counters
    
    def __le__(self, another_game_state:"GameState")->bool:
        return self.board.total_counters <= another_game_state.board.total_counters
    
    def __repr__(self):
        out = f""
        for pile in self.board.piles:
            out = out + f'{pile}[' + \
                (f"\N{circled times} " * pile) + ']\n'
        return out
    
    def __hash__(self):
        return hash( tuple(sorted(self.board.piles) ) )


@dataclass(frozen=True)
class Move:
    counter: Counter
    pile: PileIndex
    before_state: GameState
    after_state: GameState

    def __post_init__(self):
        validate_move(self)

    def __eq__(self, another_move:"Move")->bool:
        return self.before_state == another_move.before_state and \
                self.after_state == another_move.after_state and \
                self.counter == another_move.counter and \
                self.pile == another_move.pile
    
    def __ne__(self, another_move:"Move")->bool:
        return self.before_state != another_move.before_state or \
                self.after_state != another_move.after_state or \
                self.counter != another_move.counter or \
                self.pile != another_move.pile


