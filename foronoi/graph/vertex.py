from foronoi.graph.coordinate import Coordinate


class Vertex(Coordinate):
    def __init__(self, x, y, connected_edges=None):
        """
        A vertex is a fixed cross point between borders. Extends the :class:`Coordinate` class.

        Examples
        --------
        Vertex operations

        >>> connected_edges: List[HalfEdge] = vertex.connected_edges  # All connected edges
        >>> vertex_x: float = vertex.x                                # x-coordinate
        >>> vertex_xy: [float, float] = vertex.xy                     # (x, y)-coordinates

        Parameters
        ----------
        x: Decimal
            x-coordinate
        y: Decimal
            y-coordinate
        connected_edges: list(:class:`HalfEdge`)
            List of edges connected to this vertex.

        Attributes
        ----------
        connected_edges: list(:class:`HalfEdge`)
            List of edges connected to this vertex.
        """

        super().__init__(x, y)

        self.connected_edges = connected_edges or []

    def __repr__(self):
        return f"Vertex({self.xd:.2f}, {self.yd:.2f})"
