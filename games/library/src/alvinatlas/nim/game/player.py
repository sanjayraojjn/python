import random
from dataclasses import dataclass

from alvinatlas.core.minimax import Minimax

from alvinatlas.nim.logic.models import GameState, Move, Counter, PileIndex, NimBoard
from alvinatlas.nim.logic.exceptions import InvalidMove

@dataclass(frozen=True)
class Player:
    
    def make_move(self, game_state: GameState)->GameState:
        #check if it is your turn
        if game_state.next_player is not self:
            raise InvalidMove(f"This is not {self}'s move")
        if (move := self.get_move(game_state) ):
            return move.after_state
        else:
            raise InvalidMove("No suitable move")

    def get_move(self, game_state: GameState)->Move|None:
        """
        returns the best move as per the current game state
        """


@dataclass(frozen=True)
class ComputerRandomPlayer(Player):
    
    def get_move(self, game_state: GameState)->Move|None:
        """
        """
        return random.choice( game_state.possible_moves() )
    
@dataclass(frozen=True)
class ConsolePlayer(Player):

    def get_move(self, game_state: GameState)->Move|None:
        """
        get a move using console input
        """
        try:
            if len(game_state.board.piles) == 1:
                ip = input("enter your move# ")
                pile = PileIndex(1)
                counter = Counter(int(ip.strip()))
            else:
                ip = input("enter next move#(pile counter) space-separated: ")
                pile, counter = ip.strip().split()
                pile = PileIndex(int(pile))
                counter = Counter(int(counter))
        except ValueError:
            raise InvalidMove("wrong inputs")
        
        return Move(counter, pile, \
                    game_state, \
                    GameState(NimBoard( self.board.piles[:pile] + (self.board.piles[pile] - counter, ) + self.board.piles[pile+1: ] ))    )
        

@dataclass(frozen=True)
class MinimaxComputerPlayer(Player):
    """coputer player implementing minimax algorithm"""

    def __init__(self):
        self.minimax = MiniMax(min_score=-1, max_score=1)
        

    def get_move(self, game_state: GameState)->Move|None:
        """
        get the move using minimax
        """
        return self.minimax.get_best_move(game_state)
