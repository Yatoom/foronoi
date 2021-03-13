from pprint import pprint

from voronoi import Voronoi, Polygon
import matplotlib.pyplot as plt

# Define a set of points
from voronoi.graph.coordinate import FloatCoordinate
from voronoi.visualization import Visualization

points = [
    (2.5, 2.5),
    (4, 7.5),
    (7.5, 2.5),
    (6, 7.5),
    (4, 4),
    (3, 3),
    (6, 3),
]

# Define a bounding box
polygon = Polygon([
    (2.5, 10),
    (5, 10),
    (10, 5),
    (10, 2.5),
    (5, 0),
    (2.5, 0),
    (0, 2.5),
    (0, 5),
])

# Initialize the algorithm
v = Voronoi(polygon)

# Create the diagram
v.create_diagram(points)

vertices = v.vertices


def sort_vertices(vertex):
    return vertex.point.y, vertex.point.x


def sort_edges(edge):
    return edge.get_origin().y, edge.get_origin().x


r = [
    [
        [edge.get_origin(), edge.twin.get_origin()]
        for edge in sorted(vertex.connected_edges, key=sort_edges)
    ]
    for vertex in sorted(vertices, key=sort_vertices)
]
pprint(r)
#
# for vertex in vertices:
#     for edge in vertex.connected_edges:
#         print(diff(edge.get_origin(), edge.twin.get_origin()))
