class Vertex:
    def __init__(self, connected_edges=None, coordinate=None):
        if connected_edges is None:
            connected_edges = []

        self.connected_edges = connected_edges

        self.coordinate = coordinate

    def __repr__(self):
        return f"Vertex({self.coordinate})"

    @property
    def position(self):
        return self.coordinate