from voronoi.algorithm import Algorithm
from voronoi.graph import Polygon
from voronoi.graph.bounding_box import BoundingBox


# -----------------
# Helper functions
# -----------------

def _triangle(x, y):
    return Polygon([
        (0, y),
        (x, y),
        (x / 2, 0)
    ])


def _execute(polygon, points, sizes):
    v = Algorithm(polygon)
    v.create_diagram(points=points, vis_steps=False, verbose=False, vis_result=False)
    calculated = [p.cell_size(2) for p in v.points]
    assert (sizes == calculated)


# -----------
# Test cases
# -----------

def test_single_point_triangle():
    # Polygon
    polygon = _triangle(100, 100)

    # Points
    points = [
        (50, 50),
    ]

    # Expected sizes
    sizes = [5000]

    # Execute test
    _execute(polygon, points, sizes)


def test_grid():
    # Polygon
    polygon = BoundingBox(-5, 30, -5, 30)

    # Points
    points = []
    for i in range(25, 0, -5):
        for j in range(0, 25, 5):
            points.append((j, i))

    # Expected sizes
    sizes = [56.25, 37.5, 37.5, 37.5, 93.75, 37.5, 25.0, 25.0, 25.0, 62.5, 37.5, 25.0, 25.0, 25.0, 62.5, 37.5, 25.0,
             25.0, 25.0, 62.5, 93.75, 62.5, 62.5, 62.5, 156.25]

    # Execute test
    _execute(polygon, points, sizes)


def test_diamond():
    # Polygon
    polygon = BoundingBox(0, 10, 0, 10)

    # Points
    points = [
        (5, 7.5),
        (2.5, 5),
        (7.5, 5),
        (5, 2.5),
    ]

    # Expected sizes
    sizes = [25.0, 25.0, 25.0, 25.0, ]

    # Execute test
    _execute(polygon, points, sizes)


def test_martijn():
    # Polygon
    polygon = BoundingBox(-1, 26, -1, 26)

    # Points
    points = [
        (2.241, 3.594),
        (3.568, 3.968),
        (6.401, 16.214),
        (2.925, 18.298),
    ]

    # Expected sizes
    sizes = [42.86, 209.3, 380.84, 96.0]

    # Execute test
    _execute(polygon, points, sizes)


def test_roel():
    # Polygon
    polygon = BoundingBox(0, 30, 0, 30)

    # Points
    points = [
        (8.333, 8.333),
        (8.333, 26),
        (16.667, 8.333),
        (26, 17.667)
    ]

    # Expected sizes
    sizes = [214.58, 229.05, 221.56, 234.8]

    # Execute test
    _execute(polygon, points, sizes)


def test_desmos():
    # Polygon
    polygon = BoundingBox(0, 25, 0, 25)

    # Points
    points = [
        (4.6, 11.44),
        (10, 15.44),
        (10, 3),
        (12.7, 10.6),
        (8.7, 7.7),
        (13.9, 6.76),
        (7.1, 4.24),
        (2.3, 12),
        (12, 1.20),
        (5.3, 2),
        (3.4, 2.9),
        (7.8, 8.4),
    ]

    # Expected sizes
    sizes = [26.01, 202.48, 15.87, 95.95, 12.32, 108.89, 14.05, 57.78, 31.34, 12.08, 31.21, 17.03]

    # Execute test
    _execute(polygon, points, sizes)


def test_rounding_errors():
    # Polygon
    polygon = BoundingBox(0, 25, 0, 25)

    # Points
    points = [
        (10, 3),
        (13.9, 6.76),
        (12, 1.20),
    ]

    # Expected sizes
    sizes = [128.59, 465.07, 31.34]

    # Execute test
    _execute(polygon, points, sizes)


def test_corners():
    # Polygon
    polygon = BoundingBox(0, 10, 0, 10)

    # Points
    points = [
        (0, 10),
        (10, 0),
        (0, 0),
        (10, 10),
    ]

    # Expected sizes
    sizes = [25.0, 25.0, 25.0, 25.0]

    # Execute test
    _execute(polygon, points, sizes)


def test_horizontal():
    # Polygon
    polygon = BoundingBox(0, 8, 0, 10)

    # Points
    points = [
        (2, 2.5),
        (4, 2.5),
        (6, 2.5),
    ]

    # Expected sizes
    sizes = [30.0, 20.0, 30.0]

    # Execute test
    _execute(polygon, points, sizes)


def test_left_arc():
    # Polygon
    polygon = BoundingBox(0, 25, 0, 25)

    # Points
    points = [
        (3.125, 3.125),
        (9.375, 3.125),
        (15.625, 3.125),
        (21.875, 3.125),
        (3.125, 9.375),
    ]

    # Expected sizes
    sizes = [39.06, 58.59, 117.19, 156.25, 253.91]

    # Execute test
    _execute(polygon, points, sizes)


def test_multi_diamond():
    # Polygon
    polygon = BoundingBox(-1, 26, -1, 26)

    # Points
    points = [
        (3.125, 3.125),
        (9.375, 3.125),
        (15.625, 3.125),
        (21.875, 3.125),
        (3.125, 9.375),
        (9.375, 9.375),
        (15.625, 9.375),
        (21.875, 9.375),
        (3.125, 15.625),
        (9.375, 15.625),
        (15.625, 15.625),
        (21.875, 15.625),
        (3.125, 21.875),
        (9.375, 21.875),
        (15.625, 21.875),
        (21.875, 21.875),
        (6.25, 18.75),
        (12.5, 18.75),
        (18.75, 18.75),
        (6.25, 12.5),
        (12.5, 12.5),
        (18.75, 12.5),
        (6.25, 6.25),
        (12.5, 6.25),
        (18.75, 6.25),
        (0.0, 12.5),
        (0.0, 18.75),
        (6.25, 25.0),
        (12.5, 25.0),
        (18.75, 25.0),
        (25.0, 18.75)
    ]

    # Expected sizes
    sizes = [47.68, 35.55, 35.55, 47.68, 27.04, 19.53, 19.53, 35.55, 19.53, 19.53, 19.53, 27.04, 30.66, 19.53, 19.53,
             30.66, 19.53, 19.53, 19.53, 19.53, 19.53, 19.53, 19.53, 19.53, 19.53, 16.52, 16.52, 16.52, 16.02, 16.52,
             17.02]

    # Execute test
    _execute(polygon, points, sizes)


def test_triangle_from_left():
    # Polygon
    polygon = _triangle(100, 100)

    # Points
    points = [(13, 93), (20, 89), (33, 69)]

    # Expected sizes
    sizes = [218.59, 629.68, 4151.73]

    # Execute test
    _execute(polygon, points, sizes)


def test_triangle_from_right():
    # Polygon
    polygon = _triangle(100, 100)

    # Points
    points = [(100 - 13, 93), (100 - 20, 89), (100 - 33, 69)]

    # Expected sizes
    sizes = [218.59, 629.68, 4151.73]

    # Execute test
    _execute(polygon, points, sizes)


def test_lines_outside_triangle():
    # Polygon
    polygon = _triangle(100, 100)

    # Points
    points = [
        (57, 75),
        (35, 85),
        (92, 98),
        (81, 87),
    ]

    # Expected sizes
    sizes = [2590.11, 2590.11, 147.0, 673.12]

    # Execute test
    _execute(polygon, points, sizes)


def test_another_line_outside_triangle():
    # Polygon
    polygon = _triangle(100, 100)

    # Points
    points = [
        (54, 90),
        (5, 95),
        (16, 85),
    ]

    # Expected sizes
    sizes = [3490.08, 1373.73, 1373.73]

    # Execute test
    _execute(polygon, points, sizes)


def test_max_distance():
    # Polygon
    polygon = _triangle(100, 100)

    # Points
    points = [
        (45, 13),
        (57, 71),
        (39, 82),
        (61, 81),
    ]

    # Expected sizes
    sizes = [899.09, 1299.22, 1629.42, 1172.27]

    # Execute test
    _execute(polygon, points, sizes)


def test_calc_cell_sizes():
    # Polygon
    polygon = _triangle(100, 100)

    # Points
    points = [
        (45, 13),
        (43, 85),
        (39, 82),
        (22, 95),
        (27, 90),
    ]

    # Expected sizes
    sizes = [1161.4, 1958.77, 1128.36, 341.33, 410.13]

    # Execute test
    _execute(polygon, points, sizes)