class Point:
    """
    A simple point
    """

    def __init__(self, x=None, y=None, player: int = None, name=None):
        self.x: float = x
        self.y: float = y
        self.player = player
        self.name = name

    def __repr__(self):
        if self.name is not None:
            return f"Point_{self.name}"
        return f"Point({round(self.x, 3)}, {round(self.y, 3)})"
