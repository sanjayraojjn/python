from dataclasses import dataclass
from typing import Callable, TypeAlias
import random
import logging

from alvinatlas.core.renderer import Renderer
from alvinatlas.core.exceptions import GameOver

from alvinatlas.nim.logic.exceptions import InvalidMove
from alvinatlas.nim.logic.models import GameState, NimBoard, Counter
from alvinatlas.nim.game.player import Player
from alvinatlas.nim.game.exceptions import InvalidRenderer, \
    BothPlayerSame, InvalidCurrentPlayer, InvalidPlayer

ErrorHandler: TypeAlias = Callable[[Exception ], None]

@dataclass(frozen=True)
class Nim:
    player1: Player
    player2: Player
    renderer: Renderer
    current_player: Player
    error_handler: ErrorHandler | None = None

    def __post_init__(self)->None:
        id_p1 = id(self.player1)
        id_p2 = id(self.player2)
        id_cp = id(self.current_player)

        if id_p1 == id_p2:
            raise BothPlayerSame("Both players are same")
        if (id_cp != id_p1) and (id_cp != id_p2):
            raise InvalidCurrentPlayer("Wrong current player set")
        if self.player1 is None:
            raise InvalidPlayer("First Player is not defined")
        if self.player2 is None:
            raise InvalidPlayer("Second player is not defined")
        if self.current_player is None:
            raise InvalidCurrentPlayer("current player is not defined")
        if not isinstance(self.renderer, Renderer):
            raise InvalidRenderer("Not a valid renderer provided")
        
    def play(self, starting_conf:list[int]|None=None)->Player:
        """
        """
        if starting_conf is None: #random game
            num_piles = random.randint(1, 5)
            board = NimBoard( tuple( [Counter(random.randint(1, 10)) for c in range(num_piles) ] ) )
        else:
            board = NimBoard( tuple( [Counter(c) for c in starting_conf] ) )

        game_state = GameState( board )
        current_player = self.current_player

        while True:
            self.renderer.render(game_state)
            if game_state.game_over:
                break
            try:
                game_state = current_player.make_move(game_state)
                current_player = self.player1 if current_player is self.player2 \
                    else self.player2
            except InvalidMove as ex:
                logging.exception("invalid move detected")
                if self.error_handler:
                    self.error_handler(ex)
                continue
            except GameOver as ex:
                if self.error_handler:
                    self.error_handler(ex)
                break
        return self.player1 if current_player is self.player2 \
                    else self.player2
