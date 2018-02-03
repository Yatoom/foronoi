class Vertex:
    def __init__(self, incident_points=None, point=None):
        self.incident_points = incident_points
        self.point = point

    @property
    def position(self):
        return self.point


class HalfEdge:
    def __init__(self, incident_point, twin=None):

        # Pointer to the breakpoint it is attached to
        self.breakpoint = None

        # Pointer to the vertex it is attached to
        self.vertex = None

        # The point of which this edge is the border
        self.incident_point = incident_point

        # the twin of this edge
        self._twin = None
        self.twin = twin

        self.removed = False

    def __repr__(self):
        return f"HalfEdge({self.incident_point})"

    def get_origin(self, y):
        if self.vertex is None:
            return self.breakpoint.get_intersection(y)
        return self.vertex.point

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
