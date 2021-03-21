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

# Generate the points
points = []
while len(points) < n_points:
    p = Point(random.randint(0, width), random.randint(0, height))

    # Check if the point is inside the triangle
    if triangle.inside(p):
        points.append(p)

# Print the input points
if print_input:
    print("points = [")
    for point in points:
        print(f"    Point({point.xd}, {point.yd}),")
    print("]")

points = [
    Point(27, 89),
    Point(15, 95),
    Point(49, 8),
    Point(79, 63),
    Point(54, 12),
    Point(77, 92),
    Point(62, 82),
    Point(83, 71),
    Point(58, 33),
    Point(53, 59),
]

# Initialize the algorithm
v = Voronoi(triangle)

# Optional: attach observer that visualizes Voronoi diagram every step
v.attach_observer(
    VoronoiObserver(

        # Settings to put into the visualizer
        settings=dict(polygon=True, edges=True, vertices=True, sites=True,
                      outgoing_edges=False, border_to_site=False, scale=1,
                      edge_labels=False, site_labels=False, triangles=False, arcs=False),

        # Callback that saves the figure every step
        callback=lambda observer, figure: figure.savefig(f"output/{observer.n_messages:02d}.png")
    )
)

# Start the procedure
v.create_diagram(
    points=[(p.xd, p.yd) for p in points],
)


"""
Used for the example in the README:
points = [
    Point(57, 86),
    Point(14, 77),
    Point(44, 79),
    Point(62, 27),
    Point(49, 71),
    Point(22, 91),
    Point(49, 85),
    Point(79, 65),
    Point(64, 97),
    Point(50, 13),
]
"""