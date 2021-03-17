import random
from voronoi import Voronoi, Polygon, Point, VoronoiObserver

# Width and height of the triangle
width = 100
height = 100

# Number of points to generate
n_points = 10

# Print the randomly generated input points
print_input = True

# Create the triangle
triangle = Polygon([
    (0, height),
    (width, height),
    (width / 2, 0)
])

# Print the input points
points = [
    Point(72, 94),
    Point(59, 39),
    Point(88, 97),
    Point(37, 43),
    Point(42, 53),
    Point(48, 93),
    Point(52, 18),
    Point(16, 83),
    Point(85, 80),
    Point(43, 57),
]
# Initialize the algorithm
v = Voronoi(triangle)

# Attach observer that visualizes Voronoi diagram every step
v.attach_observer(
    VoronoiObserver(
        visualize_steps=True,

        # Settings to put into the visualizer
        settings=dict(polygon=True, edges=True, vertices=True, sites=True,
                      outgoing_edges=False, events=True, beachline=True, arcs=True, incident_pointers=False, scale=1,
                      show_edge_labels=False, show_point_labels=False, show_triangles=False),

        # Callback that saves the figure every step
        callback=lambda observer, figure: figure.savefig(f"output/{observer.n_messages}.png")
    )

)

# Start the procedure
v.create_diagram(
    points=[(p.x, p.y) for p in points],
)
