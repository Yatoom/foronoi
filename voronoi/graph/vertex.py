class Vertex:
    def __init__(self, connected_edges=None, point=None):
        if connected_edges is None:
            connected_edges = []

        self.connected_edges = connected_edges

        self.point = point

    def __repr__(self):
        return f"Vertex({self.point})"

    @property
    def position(self):
        return self.point