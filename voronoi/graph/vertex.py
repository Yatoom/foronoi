from voronoi.graph.coordinate import DecimalCoordinate


class Vertex(DecimalCoordinate):
    def __init__(self, x, y, connected_edges=None):
        super().__init__(x, y)

        self.connected_edges = connected_edges or []

    def __repr__(self):
        return f"Vertex({self.x:.2f}, {self.y:.2f})"
