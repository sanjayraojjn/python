import random
from dataclasses import dataclass

from alvinatlas.core.minimax import Minimax
from alvinatlas.core.exceptions import GameOver

from alvinatlas.nim.logic.models import GameState, Move, Counter, PileIndex, NimBoard
from alvinatlas.nim.logic.exceptions import InvalidMove, InvalidCounter

@dataclass(frozen=True)
class Player:
    
    def make_move(self, game_state: GameState)->GameState:
        """
        """
        if game_state.game_over:
            raise GameOver("Game is over")
        
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
        if game_state.game_over:
            raise GameOver("Game is over")
        return random.choice( game_state.possible_moves )
    
@dataclass(frozen=True)
class ConsolePlayer(Player):

    def get_move(self, game_state: GameState)->Move|None:
        """
        get a move using console input
        """
        if game_state.game_over:
            raise GameOver("Game is over")
        try:
            if len(game_state.board.piles) == 1:
                ip = input("enter your move# ")
                pile = PileIndex(1)
                counter = Counter(int(ip.strip()))
            else:
                ip = input("enter your move#(pile counter) space-separated: ")
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
class GRPCPlayer(Player):
    """
    player for grpc server
    """
    input_stream: any

    def get_move(self, game_state: GameState)->Move|None:
        """
        get a move using GRPC request
        """
        if game_state.game_over:
            raise GameOver("Game is over")
        
        pile, counter = self.input_stream.get_input()
        
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

    def _align_gamestate(self, game_state: GameState, align_to: GameState)->GameState:
        """
        align the counter of first game state to another game state
        """
        if len(game_state.board.piles) != len(align_to.board.piles):
            raise InvalidMove("game states cannot be aligned")

        counter_map_gamestate = {}
        counter_map_align_to = {}

        for idx, pile in enumerate(game_state.board.piles):
            counter_map_gamestate[pile] = counter_map_gamestate.get(pile, 0) + 1
        for idx, pile in enumerate(align_to.board.piles):
            counter_map_align_to[pile] = counter_map_align_to.get(pile, 0) + 1
            
        #print(counter_map_gamestate)
        #print(counter_map_align_to)

        counters = []
        index_modified = None
        for idx, pile in enumerate(game_state.board.piles):
            #print(f"pile {pile}")
            if (c_value := counter_map_align_to.get(pile, 0) ) > 0:
                #print(f"{pile} pile, {c_value}")
                counter_map_gamestate[pile] -= 1
                counter_map_align_to[pile] -= 1
                if c_value == 1:
                    #print(f"{pile} removed, {c_value}")
                    #del counter_map_gamestate[pile]
                    del counter_map_align_to[pile]
                if(counter_map_gamestate[pile] == 0):
                    del counter_map_gamestate[pile]
                counters.append(pile)
            elif index_modified is None:
                index_modified = idx
                counters.append(None)
            else:
                raise InvalidMove("game states cannot be aligned")
            
        #print(counter_map_gamestate)
        #print(counter_map_align_to)
        #print(index_modified)
    
        if index_modified is not None:
            adjusted_counter = counter_map_align_to.popitem()[0]
            if(adjusted_counter > counter_map_gamestate.popitem()[0]):
                raise InvalidMove("game states cannot be aligned")
            counters[index_modified] = adjusted_counter

        #print(counters)

        return GameState(NimBoard( tuple( counters ) ))
    
    def get_move(self, game_state: GameState)->Move|None:
        """
        get the move using minimax
        """
        if game_state.game_over:
            raise GameOver("Game is over")
        score, best_gamestate = self.minimax.get_best_gamestate(game_state)
        #align the best game state to the current game state
        best_gamestate = self._align_gamestate(game_state, best_gamestate)

        #compute the move by using two given states of the game
        num_counter_moved = None
        pile_index = None
        for idx, pile in enumerate(game_state.board.piles):
            if pile != best_gamestate.board.piles[idx]:
                pile_index = idx + 1
                num_counter_moved = pile - best_gamestate.board.piles[idx]
                if(num_counter_moved < 0):
                    raise InvalidCounter("counter value cannot go below zero")
                break

        if pile_index is None or num_counter_moved is None:
            return None

        return Move( Counter(num_counter_moved), PileIndex(pile_index), \
                    game_state, best_gamestate)
