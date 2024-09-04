from tic_tac_toe.logic.models import Mark

from tic_tac_toe.game.engine import TicTacToe
from tic_tac_toe.game.players import RandonComputerPlayer

from tic_tac_toe.game.renderers import ConsoleRenderer
from tic_tac_toe.game.players import ConsolePlayer

player1 = ConsolePlayer( Mark("X") )
player2 = RandonComputerPlayer( Mark("O") )

TicTacToe(player1, player2, ConsoleRenderer() ).play()