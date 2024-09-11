import unittest
from functools import cache
from dataclasses import dataclass

from atlas_core.core.models import GameState
from atlas_core.core.exceptions import InvalidCounter

@dataclass(frozen=True)
class SimpleNimGameState(GameState):

    def __init__(self, counter)->None:
        self.counter = counter

    def __post_init__(self)->None:
        if self.counter < 0:
            raise InvalidCounter("counter value cannot go below zero")

    @cache
    def possible_moves(self)->list["Move"]:
        pass
    
    @cache
    def possible_next_states(self)->list[GameState]:
        return [ SimpleNimGameState(self.counter - pick) for pick in (1,2,3) ]
    
    @cache
    def game_over(self)->bool:
        return self.counter == 0
    
    @cache
    def score(self)->int:
        return 1 if (self.counter == 0) else 0
    
    def __eq__(self, another_game_state:GameState)->bool:
        return self.counter == another_game_state.counter
    
    def __ne__(self, another_game_state:GameState)->bool:
        return self.counter != another_game_state.counter
    
    def __gt__(self, another_game_state:GameState)->bool:
        return self.counter > another_game_state.counter
    
    def __lt__(self, another_game_state:GameState)->bool:
        return self.counter < another_game_state.counter
    
    def __ge__(self, another_game_state:GameState)->bool:
        return self.counter >= another_game_state.counter
    
    def __le__(self, another_game_state:GameState)->bool:
        return self.counter <= another_game_state.counter
    
    def __repr__(self):
        return f'--{self.counter}[' + ("\U0001FA99" * self.counter) + ']--'

class TestModels(unittest.TestCase):

    def test_gamestate_possible_next_state(self):
        game_state = SimpleNimGameState(6)
        
        self.assertEqual(game_state.possible_next_states(), \
                         [ SimpleNimGameState(5), SimpleNimGameState(4), SimpleNimGameState(3) ])
        
        game_state = SimpleNimGameState(3)     
        self.assertEqual(game_state.possible_next_states(), \
                         [ SimpleNimGameState(5), SimpleNimGameState(4), SimpleNimGameState(3) ])

        
    def test_gamestate_score(self):
        game_state = SimpleNimGameState(0)
        self.assertEqual( game_state.score(), 1, "Score should be 1 when counter reaches zero {game_state}")

        game_state = SimpleNimGameState(1)
        self.assertEqual( game_state.score(), 0, f"Score should be 0 when counter is not zero {game_state}"), 

        game_state = SimpleNimGameState(5)
        self.assertEqual( game_state.score(), 0, f"Score should be 0 when counter is not zero {game_state}"), 


if __name__ == "__main__":
    unittest.main()
    