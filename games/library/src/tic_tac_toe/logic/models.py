import enum
import typing
import re
from dataclasses import dataclass
from functools import cached_property
import random

from tic_tac_toe.logic.validators import validate_grid, validate_game_state
from tic_tac_toe.logic.exceptions import InvalidGameState, InvalidMove, UnknownGameScore

class Mark(enum.StrEnum):
    CROSS = 'X'
    NAUGHT = 'O'

    @property
    def other(self) -> typing.Self:
        return Mark.NAUGHT if self is Mark.CROSS else Mark.CROSS
    
def preview(cells):
     print(cells[:3], cells[3:6], cells[6:], sep="\n")


@dataclass(frozen=True)
class Grid:
    cells: str = " " * 9

    def __post_init__(self) -> None:
        validate_grid(self)
        
    @cached_property
    def empty_count(self):
        return self.cells.count(" ")
    
    @cached_property
    def x_count(self):
        return self.cells.count("X")
    
    @cached_property
    def o_count(self):
        return self.cells.count("O")
        
    @cached_property
    def is_full(self):
        return self.empty_count == 0
    
    @cached_property
    def is_empty(self):
        return self.empty_count == 9
    
    @cached_property
    def is_valid(self):
        return self.x_count - self.o_count in [0, 1]

@dataclass(frozen=True)
class Move:
    mark: Mark
    cell_index: int
    before_state: "GameState"
    after_state: "GameState"

WINNING_PATTERNS = ( "???......",  "...???...", "......???",  "?..?..?..", \
                    ".?..?..?.",  "..?..?..?", "?...?...?", "..?.?.?.." )

@dataclass(frozen=True)
class GameState:
    grid: Grid
    starting_mark: Mark = Mark("X")

    def __post_init__(self)->None:
        validate_game_state(self)

    @cached_property
    def current_mark(self)->Mark:
        if self.grid.x_count == self.grid.o_count:
            return self.starting_mark
        else:
            return self.starting_mark.other
        
    @cached_property
    def game_not_started(self) -> bool:
        return self.grid.empty_count == 9
    
    @cached_property
    def game_over(self) -> bool:
        return self.winner is not None or self.tie
    
    @cached_property
    def tie(self) -> bool:
        return self.winner is None and self.grid.empty_count == 0
    
    @cached_property
    def winner(self) -> Mark:
        for mark in Mark:
            for p in WINNING_PATTERNS:
                if re.match( p.replace("?", mark), self.grid.cells ):
                    return mark
        return None
    
    @cached_property
    def winning_cells(self) -> list[int]:
        for mark in Mark:
            for p in WINNING_PATTERNS:
                if re.match( p.replace("?", mark), self.grid.cells ):
                    return [ match.start() for match in re.finditer(r"\?", p) ]
        return []
    
    @cached_property
    def possible_moves(self) -> list[Move]:
        moves = []
        if not self.game_over:
            for match in re.finditer(r"\s", self.grid.cells):
                moves.append( self.make_move_to( match.start() ) )
        return moves
    
    def make_move_to(self, index: int)->Move:
        if self.grid.cells[index] != " ":
            raise InvalidMove("Cell is not empty")
        return Move(mark=self.current_mark,
                    cell_index=index, 
                    before_state=self, 
                    after_state=GameState( Grid( 
                                            self.grid.cells[:index]
                                            + self.current_mark
                                            + self.grid.cells[index+1: ] ),
                               self.starting_mark )
                    )
    
    def make_random_move(self) -> Move | None:
        try:
            return random.choice(self.possible_moves)
        except IndexError:
            return None
    
    def evaluate_score(self, mark: Mark) -> int:
        if self.game_over:
            if self.tie:
                return 0
            if self.winner is mark:
                return 1
            else:
                return -1
        raise UnknownGameScore("Game is not over yet")
        


