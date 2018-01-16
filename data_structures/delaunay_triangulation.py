from random import shuffle


class Point:
    def __init__(self, x: float = None, y: float = None, player: int = None):
        self.x = x
        self.y = y
        self.player = player


class Edge:
    def __init__(self, p1: Point = None, p2: Point = None):
        self.p1 = p1
        self.p2 = p2


class DelaunayTriangulation:
    d_points: list = []
    d_edges: list = []

    def __init__(self):
        # Initialize T as a large triangle delta(p_0, p_1, p_2) containing all points
        self.d_points.append(Point(-1000, -1000, 0))
        self.d_points.append(Point(0, 1000, 0))
        self.d_points.append(Point(1000, -1000, 0))
        self.d_edges.append(Edge(self.d_points[0], self.d_points[1]))
        self.d_edges.append(Edge(self.d_points[0], self.d_points[2]))
        self.d_edges.append(Edge(self.d_points[1], self.d_points[2]))

    def legalize_edge(self, point: Point, edge: Edge):
        # If edge is illegal
        if True: # TODO check if edge is illegal
            # Find adjacent triangle edge.p1,edge.p2,ph
            ph = None
            # Replace edge by new edge point,ph
            # TODO this hard thing :(
            pass

    def insert(self, point: Point):
        # Find triangle containing point
        # TODO find triangle containing the point
        pi = None
        pj = None
        pk = None

        # If point lies withing triangle then
        if True: # TODO add check for point inside triangle
            # Add edges from point to pi, pj, pk
            self.d_edges.append(Edge(point, pi))
            self.d_edges.append(Edge(point, pj))
            self.d_edges.append(Edge(point, pk))
            # Legalize the edges of the triangle pi,pj,pk
            self.legalize_edge(point, Edge(pi, pj))
            self.legalize_edge(point, Edge(pj, pk))
            self.legalize_edge(point, Edge(pk, pi))

        # Else (point lies on an edge)
        else: # TODO complete else part
            pass

    def compute_triangulation(self, points: list):
        # Randomize input list
        shuffle(points)

        # Insert the random order point set
        for point in points:
            self.insert(point)

        # Discard the points p_0, p_1, p_2 and all incident edges
        self.d_edges = list(filter(lambda e: e.p1.player > 0 and e.p2.player > 0, self.d_edges))
        self.d_points = list(filter(lambda p: p.player > 0, self.d_points))

        # Return the result, points are implicit
        return self.d_edges
