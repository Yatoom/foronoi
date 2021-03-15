from voronoi import Voronoi, Polygon

# Define a set of points
from voronoi.observers.debug_observer import DebugObserver
from voronoi.observers.tree_observer import TreeObserver
from voronoi.observers.voronoi_observer import VoronoiObserver

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
v.attach_observer(VoronoiObserver(visualize_result=True, visualize_before_clipping=True, visualize_steps=True))
v.attach_observer(DebugObserver())
v.attach_observer(TreeObserver())

# Create the diagram
v.create_diagram(
    points=points,
)

# Get properties
edges = v.edges
vertices = v.vertices
arcs = v.arcs
points = v.points

# Calculate the sell size for each  point
for point in v.points:
    print(f"{(point.x, point.y)} \t {point.cell_size()}")

# for point in v.points:
#     print([(round(p.x, 2), round(p.y, 2)) for p in point.get_coordinates()])

print(v.points[0].get_coordinates())