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
    Point(59, 93),
    Point(41, 88),
    Point(14, 97),
    Point(31, 64),
    Point(70, 62),
    Point(94, 99),
    Point(40, 38),
    Point(56, 39),
    Point(50, 18),
    Point(87, 92),
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