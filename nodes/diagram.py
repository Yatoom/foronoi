class BoundingBox:
    def __init__(self, left_x, right_x, bottom_y, top_y):
        self.left = left_x
        self.right = right_x
        self.bottom = bottom_y
        self.top = top_y


class Vertex:
    def __init__(self, incident_edges=None, point=None):

        if incident_edges is None:
            incident_edges = []

        self.incident_edges = incident_edges

        self.point = point

    def __repr__(self):
        return f"Vertex({self.point})"

    @property
    def position(self):
        return self.point
    #
    # def __lt__(self, other):
    #     if self.point.y == other.point.y:
    #         return self.point.x < other.point.x
    #
    #     # Switch y axis
    #     return self.point.y < other.point.y
    #
    # def __eq__(self, other):
    #     if other is None:
    #         return None
    #     return self.point.y == other.y and self.point.x == other.x
    #
    # def __ne__(self, other):
    #     return not self.__eq__(other)


class HalfEdge:
    def __init__(self, incident_point, twin=None, origin=None):

        # Pointer to the origin. Can be breakpoint or vertex.
        self.origin = origin

        # The point of which this edge is the border
        self.incident_point = incident_point

        # the twin of this edge
        self._twin = None
        self.twin = twin

        self.removed = False

    def __repr__(self):
        return f"HalfEdge({self.incident_point})"

    def get_origin(self, y=None):
        if isinstance(self.origin, Vertex):
            return self.origin.point

        if y is not None:
            return self.origin.get_intersection(y)

        return None

    def remove(self):
        self.removed = True

    @property
    def twin(self):
        return self._twin

    @twin.setter
    def twin(self, twin):

        if twin is not None:
            twin._twin = self

        self._twin = twin
