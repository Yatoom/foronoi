import numpy as np


class Point:
    """
    A simple point
    """

    def __init__(self, x=None, y=None, player: int = None, name=None, first_edge=None):
        self.x: float = x
        self.y: float = y
        self.player = player
        self.name = name
        self.first_edge = first_edge

    def __repr__(self):
        if self.name is not None:
            return f"Point_{self.name}"
        return f"Point({round(self.x, 3)}, {round(self.y, 3)})"

    def cell_size(self, digits=None):
        x = []
        y = []

        edge = self.first_edge
        start = True
        while edge != self.first_edge or start:

            if edge is None or edge.get_origin() is None:
                return None

            x.append(edge.get_origin().x)
            y.append(edge.get_origin().y)
            edge = edge.next
            start = False

        if digits is not None:
            return round(self.shoelace(x, y), digits)

        return self.shoelace(x, y)

    @staticmethod
    def shoelace(x, y):
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
