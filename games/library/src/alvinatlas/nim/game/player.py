import random
from dataclasses import dataclass

from alvinatlas.core.minimax import Minimax
from alvinatlas.core.exceptions import GameOver

from alvinatlas.nim.logic.models import GameState, Move, Counter, PileIndex, NimBoard
from alvinatlas.nim.logic.exceptions import InvalidMove, InvalidCounter

@dataclass(frozen=True)
class Player:
    
    def make_move(self, game_state: GameState)->GameState:
        #check if it is your turn
        if (move := self.get_move(game_state) ):
            return move.after_state
        else:
            raise GameOver("Game is over")

    def get_move(self, game_state: GameState)->Move|None:
        """
        returns the best move as per the current game state
        """


@dataclass(frozen=True)
class ComputerRandomPlayer(Player):
    
    def get_move(self, game_state: GameState)->Move|None:
        """
        """
        return random.choice( game_state.possible_moves )
    
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
        
        if len(game_state.board.piles) < pile:
            raise InvalidMove(f"wrong pile index {pile}, there are only {len(game_state.board.piles)} piles in the game.")

        if counter > game_state.board.piles[pile.array_index]:
            raise InvalidMove(f"wrong counter, there are only {game_state.board.piles[pile.array_index]} counters in the specified pile.")
        
        after_state = GameState(NimBoard( game_state.board.piles[:pile.array_index] + \
                            (Counter(game_state.board.piles[pile.array_index] - counter), ) + \
                            game_state.board.piles[pile.array_index+1: ] ))
        
        return Move(counter, pile, \
                    game_state, \
                    after_state)
        

@dataclass(frozen=True)
class MinimaxComputerPlayer(Player):
    minimax: Minimax = Minimax(min_score=-1, max_score=1)
    """coputer player implementing minimax algorithm"""

    def get_move(self, game_state: GameState)->Move|None:
        """
        get the move using minimax
        """
        score, best_gamestate = self.minimax.get_best_gamestate(game_state)

        #compute the move by using two given states of the game
        num_counter_moved = None
        pile_index = None
        for idx, pile in enumerate(game_state.board.piles):
            if pile != best_gamestate.board.piles[idx]:
                pile_index = idx + 1
                num_counter_moved = pile - best_gamestate.board.piles[idx]
                break

        if pile_index is None or num_counter_moved is None:
            return None

        return Move( Counter(num_counter_moved), PileIndex(pile_index), \
                    game_state, best_gamestate)
