from voronoi.graph.coordinate import Coordinate


class Vertex(Coordinate):
    def __init__(self, x, y, connected_edges=None):
        super().__init__(x, y)

        self.connected_edges = connected_edges or []

    def __repr__(self):
        return f"Vertex({self.xd:.2f}, {self.yd:.2f})"
