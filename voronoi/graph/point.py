import numpy as np

from voronoi.graph import Coordinate


class Point(Coordinate):

    def __init__(self, x=None, y=None, metadata=None, name=None, first_edge=None):
        """
        A point in 2D space.
        :param x: (float) The x-coordinate
        :param y: (float) The y-coordinate
        :param metadata: (dict) Optional metadata stored in a dictionary
        :param name: (str) A one-letter string (assigned automatically by algorithm)
        :param first_edge: (HalfEdge) Pointer to the first edge (assigned automatically by the algorithm)
        """
        super().__init__(x, y)

        if metadata is None:
            metadata = {}

        self.metadata = metadata
        self.name = name
        self.first_edge = first_edge

    def __repr__(self):
        if self.name is not None:
            return f"{self.name}"
        return f"Point({round(self.x, 3)}, {round(self.y, 3)})"

    def cell_size(self, digits=None):
        """
        Calculate cell size if the point is a site.
        :param digits: (int) number of digits to round to
        :return: (float) the area of the cell
        """
        x, y = self._get_xy()

        if digits is not None:
            return round(self._shoelace(x, y), digits)

        return self._shoelace(x, y)

    def get_coordinates(self):
        """
        Find the coordinates of the associated cell's vertices.
        """
        coordinates = []
        edge = self.first_edge
        start = True
        while edge != self.first_edge or start:
            if edge is None or edge.get_origin() is None:
                return None

            coordinates.append(edge.get_origin())
            edge = edge.next
            start = False

        return coordinates

    def _get_xy(self):
        coordinates = self.get_coordinates()
        x = [coordinate.x for coordinate in coordinates]
        y = [coordinate.y for coordinate in coordinates]
        return x, y

    @staticmethod
    def _shoelace(x, y):
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
