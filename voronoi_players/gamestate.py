class GameState:
    """
    The current state of the game.
    It will hold the settings of the game board and a list of place points
    """
    points = []

    def __init__(self, width: int = 100, height: int = 100, m: int = None, n: int = None):
        self.width = width
        self.height = height
        self.m = m
        self.n = n