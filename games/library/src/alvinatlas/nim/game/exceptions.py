class InvalidGame(Exception):
    """Invalid game configuration"""

class InvalidRenderer(InvalidGame):
    """Invalid renderer"""

class BothPlayerSame(InvalidGame):
    """both players are same"""

class InvalidCurrentPlayer(InvalidGame):
    """Invalid current player set"""

class InvalidPlayer(InvalidGame):
    """Invalid player"""

