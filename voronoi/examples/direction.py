from voronoi import Voronoi, Polygon
import matplotlib.pyplot as plt

# Define a set of points
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
v.create_diagram(
    points=points
)

# Get properties
# edges = v.edges
vertices = v.vertices
# arcs = v.arcs
# points = v.points

fig, ax = plt.subplots(figsize=(17, 17))

for vertex in vertices:
    for edge in vertex.connected_edges:
        Visualization.plot_edge(ax, edge, None, polygon, zorder=0)

for vertex in vertices:
    for edge in vertex.connected_edges:
        Visualization.plot_edge_direction(ax, edge, None, polygon, scale=0.5, zorder=5)

Visualization.plot_vertices(ax, vertices, zorder=10)

plt.show()
print()