from voronoi.graph.point import Point
from voronoi.graph.vertex import Vertex


class HalfEdge:
    def __init__(self, incident_point, twin=None, origin=None):

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
        if next:
            next.prev = self
        self.next = next

    def get_origin(self, y=None, max_y=None):
        """
        Get the point of origin.

        :param y: Sweep line (only used when the Voronoi diagram is under construction and we need to calculate
                  where it currently is)
        :param max_y: Bounding box top for clipping infinite breakpoints
        :return: The point of origin, or None
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
        return self._twin

    @twin.setter
    def twin(self, twin):

        if twin is not None:
            twin._twin = self

        self._twin = twin

    @property
    def target(self):
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