import numpy as np

from foronoi.graph.vertex import Vertex
from foronoi.graph.coordinate import Coordinate


class Point(Coordinate):

    def __init__(self, x=None, y=None, name=None, first_edge=None):
        """
        A cell point a.k.a. a site. Extends the :class:`Coordinate` class.

        Examples
        --------
        Site operations

        >>> size: float = site.area()                 # The area of the cell
        >>> borders: List[HalfEdge] = site.borders()  # Borders around this cell point
        >>> vertices: List[Vertex] = site.vertices()  # Vertices around this cell point
        >>> site_x: float = site.x                    # X-coordinate of the site
        >>> site_xy: [float, float] = site.xy         # (x, y)-coordinates of the site
        >>> first_edge: HalfEdge = site.first_edge    # First edge of the site's border

        Parameters
        ----------
        x: Decimal
            The x-coordinate of the point
        y: Decimal
            They y-coordinate of the point
        metadata: dict
            Optional metadata stored in a dictionary
        name: str
            A name to easily identify this point
        first_edge: HalfEdge
            Pointer to the first edge

        Attributes
        ----------
        name: str
            A name to easily identify this point
        first_edge: HalfEdge
            Pointer to the first edge
        """
        super().__init__(x, y)

        self.name = name
        self.first_edge = first_edge

    def __repr__(self):
        if self.name is not None:
            return f"P{self.name}"
        return f"Point({self.xd:.2f}, {self.xd:.2f})"

    def area(self, digits=None):
        """
        Calculate the cell size of the cell that this point is the cell point of.
        Under the hood, the shoelace algorithm is used.

        Parameters
        ----------
        digits: int
            The number of digits to round to

        Returns
        -------
        area: float
            The area of the cell
        """
        x, y = self._get_xy()

        if digits is not None:
            return round(self._shoelace(x, y), digits)

        return float(self._shoelace(x, y))

    def borders(self):
        """
        Get a list of all the borders that surround this cell point.

        Returns
        -------
        edges: list(HalfEdge) or None
            The list of borders, or None if not all borders are present (when the voronoi diagram is under construction)
        """

        if self.first_edge is None:
            return []
        edge = self.first_edge
        edges = [edge]
        while edge.next != self.first_edge:
            if edge.next is None:
                return edges
            edge = edge.next
            edges.append(edge)
        return edges

    def vertices(self):
        """
        Get a list of all the vertices that surround this cell point.

        Returns
        -------
        vertices: list(Vertex) or None
            The list of vertices, or None if not all borders are present (when the voronoi diagram is under
            construction)
        """
        borders = self.borders()
        if borders is None:
            return None
        return [border.origin for border in borders if isinstance(border.origin, Vertex)]

    def _get_xy(self):
        coordinates = self.vertices()
        if coordinates is None:
            return [], []
        x = [coordinate.x for coordinate in coordinates]
        y = [coordinate.y for coordinate in coordinates]
        return x, y

    def __sub__(self, other):
        return Point(x=self.xd - other.xd, y=self.yd - other.yd)

    @staticmethod
    def _shoelace(x, y):
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
