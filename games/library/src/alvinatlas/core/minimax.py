from functools import cache

from alvinatlas.core.models import GameState
from alvinatlas.core.exceptions import GameOver

class Minimax:

    def __init__(self, min_score: int, max_score: int)->None:
        self.min_score = min_score
        self.max_score = max_score

    @cache
    def get_best_gamestate(self, game_state: GameState)->GameState|None:
        """
        """
        if game_state.game_over:
            raise GameOver("Game is over")
        return max( (self.minimax(new_state, False), new_state ) \
                   for new_state in game_state.possible_next_states )

    @cache
    def minimax(self, game_state: GameState, is_maximizing: bool)->GameState:
        """
        returns the next most probable winning gamestate
        """
        if game_state.game_over:
            return self.max_score if is_maximizing else self.min_score

        return (max if is_maximizing else min) \
                ( self.minimax(next_state, not is_maximizing) for next_state in game_state.possible_next_states )

        

    
        
