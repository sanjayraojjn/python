from functools import cache

from models import GameState, Move

class Minimax:

    def __init__(self, min_score: int, max_score: int)->None:
        self.min_score = min_score
        self.max_score = max_score

    @cache
    def get_best_move(self, game_state: GameState)->Move|None:
        """
        """
        if game_state.game_over:
            return None
        return self.minimax(game_state, True)

    @cache
    def minimax(self, game_state: GameState, is_maximizing: bool)->int:
        """
        """
        if game_state.game_over:
            return self.max_score if is_maximizing else self.min_score

        if (score := game_state.score() ) is not None:
            return score
        
        return (max if is_maximizing else min) \
            ( self.minimax(next_state, not is_maximizing) for next_state in game_state.possible_next_states() )

        

    
        
