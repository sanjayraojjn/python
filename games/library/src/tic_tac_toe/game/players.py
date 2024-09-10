import abc
import random
import time
import re

from tic_tac_toe.logic.exceptions import InvalidMove
from tic_tac_toe.logic.minimax import find_best_move
from tic_tac_toe.logic.models import Move, GameState, Mark

class Player(metaclass=abc.ABCMeta):
    def __init__(self, mark: Mark) -> None:
        self.mark=mark

    def make_move(self, game_state: GameState) -> GameState:
        if self.mark is game_state.current_mark:
            if move := self.get_move(game_state):
                return move.after_state
            raise InvalidMove("no more possible moves")
        else:
            raise InvalidMove("It's other player's move")
        
    @abc.abstractmethod
    def get_move(self, game_state: GameState) -> Move | None:
        """return the current player's move in current state of the game"""

class ComputerPlayer(Player, metaclass=abc.ABCMeta):

    def __init__(self, mark: Mark, delay_seconds: float=0.25) -> None:
        super().__init__(mark)
        self.delay_seconds = delay_seconds

    def get_move(self, game_state: GameState) -> Move | None:
        time.sleep(self.delay_seconds)
        return self.get_computer_move(game_state)
    
    @abc.abstractmethod
    def get_computer_move(self, game_state: GameState) -> Move | None:
        """return the computer move in given game state"""

class RandonComputerPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        #try:
        #    return random.choice(game_state.possible_moves)
        #except IndexError:
        #    return None
        return game_state.make_random_move()
        
class ConsolePlayer(Player):
    def get_move(self, game_state: GameState) -> Move | None:
        while not game_state.game_over:
            try:
                index = grid_to_index(input(f"{self.mark}'s move: ").strip())
            except ValueError:
                print("Please provide coordinates in the form of A1 or 1A")
            else:
                try:
                    return game_state.make_move_to(index)
                except InvalidMove:
                    print("Not a valid move. That cell is already occupied.")

class MinimaxComputerPlayer(ComputerPlayer):

    def get_computer_move(self, game_state: GameState) -> Move | None:
        #return find_best_move(game_state)
        if game_state.game_not_started:
            return game_state.make_random_move()
        else:
            return find_best_move(game_state)

def grid_to_index(grid: str) -> int:
    if re.match(r"[abcABC][123]", grid):
        col, row = grid
    elif re.match(r"[123][abcABC]", grid):
        row, col = grid
    else:
        raise ValueError("Invlid grid coordinates")
    
    return 3 * (int(row) - 1) + (ord(col.upper()) - ord("A"))