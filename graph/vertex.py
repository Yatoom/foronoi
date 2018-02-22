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