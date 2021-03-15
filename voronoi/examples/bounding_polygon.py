from voronoi import Voronoi, Polygon
from voronoi.observers.debug_observer import DebugObserver
from voronoi.observers.tree_observer import TreeObserver
from voronoi.observers.voronoi_observer import VoronoiObserver
from voronoi.visualization.visualizer import Visualizer
import matplotlib.pyplot as plt

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

v.attach(
    VoronoiObserver(visualize_steps=True, visualize_before_clipping=True)
)
v.attach(
    DebugObserver()
)
v.attach(
    TreeObserver()
)

# Create the diagram
v.create_diagram(
    points=points,
)

fig, ax = plt.subplots()
vis = Visualizer(polygon, 10)
vis.plot_edges(ax, v.edges)
vis.plot_vertices(ax, v.vertices)
vis.plot_sites(ax, v.points)
vis.plot_outgoing_edges(ax, v.vertices)
plt.show()