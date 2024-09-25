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
        this method caches results and returns the best possible gamestate.
        - Counters might be in different order if hash function of GameState is 
        independent of the order of counters
        - This method stores the results in cache to optimize the performance, 
            - cache key is the hash of the gamestate object
            - if same states( (4, 0, 0) and (0, 0, 4) ) do not have the same hash 
            then the cache will not work
        """
        if game_state.game_over:
            raise GameOver("Game is over")
        possible_next_states = set(game_state.possible_next_states)

        #print(f">>>>before {len(game_state.possible_next_states)} after {len(possible_next_states)}")
        return max( (self.minimax_unordered(new_state, False), new_state ) \
                   for new_state in possible_next_states )

    @cache
    def minimax_unordered(self, game_state: GameState, is_maximizing: bool)->GameState:
        """
        returns the next most probable winning gamestate but can be in different order
        """
        if game_state.game_over:
            return self.max_score if is_maximizing else self.min_score

        return (max if is_maximizing else min) \
                ( self.minimax_unordered(next_state, not is_maximizing) for next_state in game_state.possible_next_states )

        

    
        
