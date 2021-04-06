from foronoi.graph.point import Point
from foronoi.graph.vertex import Vertex


class HalfEdge:
    def __init__(self, incident_point, twin=None, origin=None):
        """
        Edges are normally treated as undirected and shared between faces. However, for some tasks (such as simplifying
        or cleaning geometry) it is useful to view faces as each having their own edges.
        You can think of this as splitting each shared undirected edge along its length into two half edges.
        (Boundary edges of course will only have one "half-edge".)
        Each half-edge is directed (it has a start vertex and an end vertex).

        The half-edge properties let you quickly find a half-edge’s source and destination vertex, the next half-edge,
        get the other half-edge from the same edge, find all half-edges sharing a given point, and other manipulations.

        Examples
        --------
        Get the half-edge's source

        >>> edge.origin

        Get the half-edge's destination

        >>> edge.target # or edge.twin.origin

        Get the previous and next half-edge

        >>> edge.prev
        >>> edge.next

        Get the other half-edge from the same edge

        >>> edge.twin

        Find all half-edges sharing a given point

        >>> edge.origin.connected_edges

        Parameters
        ----------
        incident_point: Point
            The cell point of which this edge is the border
        twin: HalfEdge
            The other half-edge from the same edge
        origin: Breakpoint or Vertex
            The origin of the half edge. Can be a Breakpoint or a Vertex during construction, and only Vertex when
            the diagram is finished.

        Attributes
        ----------
        origin: :class:`Breakpoint` or :class:`Vertex`
            Pointer to the origin. Can be breakpoint or vertex.
        next: :class:`HalfEdge`
            Pointer to the next edge
        prev: :class:`HalfEdge`
            Pointer to the previous edge
        """

        # Pointer to the origin. Can be breakpoint or vertex.
        self.origin = origin

        # The point of which this edge is the border
        self.incident_point = incident_point

        # the twin of this edge
        self._twin = None
        self.twin = twin

        # Next and previous
        self.next = None
        self.prev = None

        self.removed = False

    def __repr__(self):
        return f"{self.incident_point}/{self.twin.incident_point or '-'}"

    def set_next(self, next):
        """
        Update the `next`-property for this edge and set the `prev`-property on the `next`-edge to the current edge.

        Parameters
        ----------
        next: HalfEdge
            The next edge
        """
        if next:
            next.prev = self
        self.next = next

    def get_origin(self, y=None, max_y=None):
        """
        Get the coordinates of the edge's origin.
        During construction of the Voronoi diagram, the origin can be a vertex, which has a fixed location, or a
        breakpoint, which is a breakpoint between two moving arcs. In the latter case, we need to calculate the
        position based on the `y`-coordinate of the sweep line.

        Parameters
        ----------
        y: Decimal
            The y-coordinate of the sweep line.
        max_y:
            Bounding box top for clipping infinitely highly positioned breakpoints.

        Returns
        -------
        origin: Coordinate
        """
        if isinstance(self.origin, Vertex):
            if self.origin.xd is None or self.origin.yd is None:
                return None
            return self.origin

        if y is not None:
            return self.origin.get_intersection(y, max_y=max_y)

        return None

    @property
    def twin(self):
        """
        Get the other half-edge from the same edge

        Returns
        -------
        twin: HalfEdge
        """
        return self._twin

    @twin.setter
    def twin(self, twin):
        if twin is not None:
            twin._twin = self

        self._twin = twin

    @property
    def target(self):
        """
        The twin's origin.

        Returns
        -------
        vertex: Vertex
        """
        if self.twin is None:
            return None
        return self.twin.origin

    def delete(self):
        """
        Delete this half edge by pointing the previous edge to the next, and removing it from the origin's
        connected edges list.
        """

        # Remove the edge from the vertex' connected edges list
        if isinstance(self.origin, Vertex):
            self.origin.connected_edges.remove(self)

        # Link previous edge to next edge
        if self.prev is not None:
            self.prev.set_next(self.next)

        # If the incident point had a pointer to this edge, we need to point it to a new one
        if self.incident_point is not None and self.incident_point.first_edge == self:

            # Incident points should remain the same
            assert (
                    self.next is None or self.next.incident_point == self.incident_point
            ), f"Incident points {self.next.incident_point} and {self.incident_point} do not match"

            # Set the new "first edge" pointer
            self.incident_point.first_edge = self.next