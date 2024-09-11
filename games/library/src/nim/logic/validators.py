from typing import TYPE_CHECKING

from exceptions import InvalidCounter, InvalidPile, InvalidMove, InvalidBoardState

if TYPE_CHECKING:
    from models import Move, Counter, PileIndex, NimBoard

def validate_counter(counter: Counter)->None:
    if counter < 0:
        raise InvalidCounter("Counter must be at least zero.")
    if not isinstance(counter, int):
        raise InvalidCounter("Counter must be an integer.")

def validate_pile_index(pile_index: PileIndex)->None:
    if pile_index <= 0:
        raise InvalidPile("Pile number must be greater than zero")
    if not isinstance(pile_index, int):
        raise InvalidPile("Pile must be an integer.")

def validate_move(move: Move)->None:
    num_counters_in_pile: int = move.before_state.board.piles[ move.pile.array_index ]
    if num_counters_in_pile < move.counter:
        raise InvalidMove(f"{move.pile} has only {num_counters_in_pile}. Not possible to draw {move.counter} counters")
    num_counters_before_move = move.before_state.board.piles[ move.pile.array_index ]
    num_counters_after_move = move.after_state.board.piles[ move.pile.array_index ]
    if num_counters_before_move != num_counters_after_move + move.counter:
        raise InvalidMove(f"before state {move.pile}#{num_counters_before_move} and after state {move.pile}#{num_counters_after_move} are not consistent after moving {move.counter} counters")
    
def validate_board(board: NimBoard)->None:
    for idx, pile in enumerate(board.piles):
        if pile < 0:
            if(len(board.piles) > 1):
                raise InvalidBoardState(f"pile#{idx+1} cannot have {pile} counters")
            else:
                raise InvalidBoardState(f"Board cannot have {pile} counters")
    