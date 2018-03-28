class Coordinate:
    def __init__(self, x=None, y=None):
        """
        A point in 2D space.
        :param x: (float) The x-coordinate
        :param y: (float) The y-coordinate
        """
        self.x: float = x
        self.y: float = y

    def __repr__(self):
        return f"({round(self.x, 3)}, {round(self.y, 3)})"
