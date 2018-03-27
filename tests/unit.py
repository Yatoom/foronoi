from algorithm import Algorithm
from graph import Polygon
from graph.bounding_box import BoundingBox
from graph.point import Point


# -----------------
# Helper functions
# -----------------

def _triangle(x, y):
    return Polygon([
        Point(0, y),
        Point(x, y),
        Point(x / 2, 0)
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
        Point(50, 50),
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
            points.append(Point(j, i))

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
        Point(5, 7.5),
        Point(2.5, 5),
        Point(7.5, 5),
        Point(5, 2.5),
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
        Point(2.241, 3.594),
        Point(3.568, 3.968),
        Point(6.401, 16.214),
        Point(2.925, 18.298),
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
        Point(8.333, 8.333),
        Point(8.333, 26),
        Point(16.667, 8.333),
        Point(26, 17.667)
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
        Point(4.6, 11.44),
        Point(10, 15.44),
        Point(10, 3),
        Point(12.7, 10.6),
        Point(8.7, 7.7),
        Point(13.9, 6.76),
        Point(7.1, 4.24),
        Point(2.3, 12),
        Point(12, 1.20),
        Point(5.3, 2),
        Point(3.4, 2.9),
        Point(7.8, 8.4),
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
        Point(10, 3),
        Point(13.9, 6.76),
        Point(12, 1.20),
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
        Point(0, 10),
        Point(10, 0),
        Point(0, 0),
        Point(10, 10),
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
        Point(2, 2.5),
        Point(4, 2.5),
        Point(6, 2.5),
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
        Point(3.125, 3.125),
        Point(9.375, 3.125),
        Point(15.625, 3.125),
        Point(21.875, 3.125),
        Point(3.125, 9.375),
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
        Point(3.125, 3.125),
        Point(9.375, 3.125),
        Point(15.625, 3.125),
        Point(21.875, 3.125),
        Point(3.125, 9.375),
        Point(9.375, 9.375),
        Point(15.625, 9.375),
        Point(21.875, 9.375),
        Point(3.125, 15.625),
        Point(9.375, 15.625),
        Point(15.625, 15.625),
        Point(21.875, 15.625),
        Point(3.125, 21.875),
        Point(9.375, 21.875),
        Point(15.625, 21.875),
        Point(21.875, 21.875),
        Point(6.25, 18.75),
        Point(12.5, 18.75),
        Point(18.75, 18.75),
        Point(6.25, 12.5),
        Point(12.5, 12.5),
        Point(18.75, 12.5),
        Point(6.25, 6.25),
        Point(12.5, 6.25),
        Point(18.75, 6.25),
        Point(0.0, 12.5),
        Point(0.0, 18.75),
        Point(6.25, 25.0),
        Point(12.5, 25.0),
        Point(18.75, 25.0),
        Point(25.0, 18.75)
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
    points = [Point(13, 93), Point(20, 89), Point(33, 69)]

    # Expected sizes
    sizes = [218.59, 629.68, 4151.73]

    # Execute test
    _execute(polygon, points, sizes)


def test_triangle_from_right():
    # Polygon
    polygon = _triangle(100, 100)

    # Points
    points = [Point(100 - 13, 93), Point(100 - 20, 89), Point(100 - 33, 69)]

    # Expected sizes
    sizes = [218.59, 629.68, 4151.73]

    # Execute test
    _execute(polygon, points, sizes)


def test_lines_outside_triangle():
    # Polygon
    polygon = _triangle(100, 100)

    # Points
    points = [
        Point(57, 75),
        Point(35, 85),
        Point(92, 98),
        Point(81, 87),
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
        Point(54, 90),
        Point(5, 95),
        Point(16, 85),
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
        Point(45, 13),
        Point(57, 71),
        Point(39, 82),
        Point(61, 81),
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
        Point(45, 13),
        Point(43, 85),
        Point(39, 82),
        Point(22, 95),
        Point(27, 90),
    ]

    # Expected sizes
    sizes = [1161.4, 1958.77, 1128.36, 341.33, 410.13]

    # Execute test
    _execute(polygon, points, sizes)