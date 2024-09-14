from typing import TYPE_CHECKING

from alvinatlas.nim.logic.exceptions import InvalidCounter, \
    InvalidPileIndex, InvalidMove, InvalidBoardState

if TYPE_CHECKING:
    from alvinatlas.nim.logic.models import Counter, Move, \
        Counter, PileIndex, NimBoard, GameState

def validate_counter(counter: "Counter")->None:
    if counter < 0:
        raise InvalidCounter("Counter must be at least zero.")
    if not isinstance(counter, int):
        raise InvalidCounter("Counter must be an integer.")

def validate_pile_index(pile_index: "PileIndex")->None:
    if pile_index <= 0:
        raise InvalidPileIndex("Pile number must be greater than zero")
    if not isinstance(pile_index, int):
        raise InvalidPileIndex("Pile must be an integer.")

def validate_move(move: "Move")->None:
    num_counters_in_pile: int = move.before_state.board.piles[ move.pile.array_index ]
    if num_counters_in_pile < move.counter:
        raise InvalidMove(f"{move.pile} has only {num_counters_in_pile}. Not possible to draw {move.counter} counters")
    num_counters_before_move = move.before_state.board.piles[ move.pile.array_index ]
    num_counters_after_move = move.after_state.board.piles[ move.pile.array_index ]
    if num_counters_before_move != num_counters_after_move + move.counter:
        raise InvalidMove(f"before state {move.pile}#{num_counters_before_move} and after state {move.pile}#{num_counters_after_move} are not consistent after moving {move.counter} counters")
    
def validate_board(board: "NimBoard")->None:
    from alvinatlas.nim.logic.models import Counter
    num_piles = len(board.piles)

    if not isinstance(board.piles, tuple):
        raise ValueError("NimBoard can be created using tuple of Counter types only")

    for idx, pile in enumerate(board.piles):
        if not isinstance(pile, Counter):
            if(num_piles > 1): #if board has more than one counters
                raise InvalidCounter(f"pile#{idx+1} on NimBoard cannot have {type(pile)}, only Counter allowed")
            else: #if board has just one counter
                raise InvalidCounter(f"NimBoard cannot have {type(pile)}, only Counter allowed")
        if pile < 0:
            if(num_piles > 1): #if board has more than one counters
                raise InvalidBoardState(f"pile#{idx+1} cannot have {pile} counters")
            else: #if board has just one counter
                raise InvalidBoardState(f"Board cannot have {pile} counters")
            
def validate_gamestate(game_state: "GameState")->None:
    """
    validates game state object
    """
    from alvinatlas.nim.logic.models import NimBoard
    if( not isinstance(game_state.board, NimBoard) ):
        raise ValueError("Nim GameState can be created using NimBoard only")
    