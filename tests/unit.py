from algorithm import Algorithm
from graph import Polygon
from graph.bounding_box import BoundingBox
from graph.point import Point


def test_grid():
    # Testing square grid
    print("Test grid.")

    points = []
    for i in range(25, 0, -5):
        for j in range(0, 25, 5):
            points.append(Point(j, i))
    v = Algorithm(BoundingBox(-5, 30, -5, 30))
    v.create_diagram(points=points, visualize_steps=False, visualize_result=False, verbose=False)
    sizes = [56.25, 37.5, 37.5, 37.5, 93.75, 37.5, 25.0, 25.0, 25.0, 62.5, 37.5, 25.0, 25.0, 25.0, 62.5, 37.5, 25.0,
             25.0, 25.0, 62.5, 93.75, 62.5, 62.5, 62.5, 156.25]
    calculated = [p.cell_size(2) for p in v.points]
    assert (sizes == calculated)


def test_diamond():
    print("Test diamond.")
    # Testing diamond
    points = [
        Point(5, 7.5),
        Point(2.5, 5),
        Point(7.5, 5),
        Point(5, 2.5),
    ]
    v = Algorithm(BoundingBox(0, 10, 0, 10))
    v.create_diagram(points=points, visualize_steps=False, visualize_result=False, verbose=False)
    sizes = [25.0, 25.0, 25.0, 25.0, ]
    calculated = [p.cell_size(2) for p in v.points]
    assert (sizes == calculated)


def test_martijn():
    print("Test Martijn.")
    points = [
        Point(2.241, 3.594),
        Point(3.568, 3.968),
        Point(6.401, 16.214),
        Point(2.925, 18.298),
    ]

    v = Algorithm(BoundingBox(-1, 26, -1, 26))
    v.create_diagram(points=points, visualize_steps=False, verbose=False, visualize_result=False)
    sizes = [42.86, 209.3, 380.84, 96.0]
    calculated = [p.cell_size(2) for p in v.points]
    assert (sizes == calculated)


def test_roel():
    print("Test Roel.")
    points = [
        Point(8.333, 8.333),
        Point(8.333, 26),
        Point(16.667, 8.333),
        Point(26, 17.667)
    ]

    v = Algorithm(BoundingBox(0, 30, 0, 30))
    v.create_diagram(points=points, visualize_steps=False, verbose=False, visualize_result=False)
    sizes = [214.58, 229.05, 221.56, 234.8]
    calculated = [p.cell_size(2) for p in v.points]
    assert (sizes == calculated)


def test_desmos():
    print("Test Desmos.")
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

    v = Algorithm(BoundingBox(0, 25, 0, 25))
    v.create_diagram(points=points, visualize_steps=False, verbose=False, visualize_result=False)
    sizes = [26.01, 202.48, 15.87, 95.95, 12.32, 108.89, 14.05, 57.78, 31.34, 12.08, 31.21, 17.03]
    calculated = [p.cell_size(2) for p in v.points]
    assert (sizes == calculated)


def test_rounding_errors():
    print("Test rounding errors.")
    points = [
        Point(10, 3),
        Point(13.9, 6.76),
        Point(12, 1.20),
    ]

    v = Algorithm(BoundingBox(0, 25, 0, 25))
    v.create_diagram(points=points, visualize_steps=False, verbose=False, visualize_result=False)
    sizes = [128.59, 465.07, 31.34]
    calculated = [p.cell_size(2) for p in v.points]
    assert (sizes == calculated)


def test_corners():
    points = [
        Point(0, 10),
        Point(10, 0),
        Point(0, 0),
        Point(10, 10),
    ]

    v = Algorithm(BoundingBox(0, 10, 0, 10))
    v.create_diagram(points=points, visualize_steps=False, verbose=False, visualize_result=False)
    sizes = [25.0, 25.0, 25.0, 25.0]
    calculated = [p.cell_size(2) for p in v.points]
    assert (sizes == calculated)


def test_horizontal():
    points = [
        Point(2, 2.5),
        Point(4, 2.5),
        Point(6, 2.5),
    ]

    v = Algorithm(BoundingBox(0, 8, 0, 10))
    v.create_diagram(points=points, visualize_steps=False, verbose=False, visualize_result=False)

    sizes = [30.0, 20.0, 30.0]
    calculated = [p.cell_size(2) for p in v.points]
    assert (sizes == calculated)


def test_left_arc():
    from algorithm import Algorithm
    from graph import Point, BoundingBox

    points = [
        Point(3.125, 3.125),
        Point(9.375, 3.125),
        Point(15.625, 3.125),
        Point(21.875, 3.125),
        Point(3.125, 9.375),
    ]

    v = Algorithm(BoundingBox(0, 25, 0, 25))
    v.create_diagram(points=points, visualize_steps=False, verbose=False, visualize_result=False)

    sizes = [39.06, 58.59, 117.19, 156.25, 253.91]
    calculated = [p.cell_size(2) for p in v.points]
    assert (sizes == calculated)


def test_multi_diamond():
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

    v = Algorithm(BoundingBox(-1, 26, -1, 26))
    v.create_diagram(points=points, visualize_steps=False, verbose=False, visualize_result=False)

    sizes = [47.68, 35.55, 35.55, 47.68, 27.04, 19.53, 19.53, 35.55, 19.53, 19.53, 19.53, 27.04, 30.66, 19.53, 19.53,
             30.66, 19.53, 19.53, 19.53, 19.53, 19.53, 19.53, 19.53, 19.53, 19.53, 16.52, 16.52, 16.52, 16.02, 16.52,
             17.02]

    calculated = [p.cell_size(2) for p in v.points]
    assert (sizes == calculated)


def test_triangle_from_left():
    x = 100
    y = 100

    polygon_points = [
        Point(0, y),
        Point(x, y),
        Point(x / 2, 0)
    ]

    polygon = Polygon(polygon_points)
    points = [Point(13, 93), Point(20, 89), Point(33, 69)]

    v = Algorithm(polygon)
    v.create_diagram(points=points, visualize_steps=False, verbose=False, visualize_result=False)

    sizes = [218.59, 629.68, 4151.73]

    calculated = [p.cell_size(2) for p in v.points]
    assert (sizes == calculated)


def test_triangle_from_right():
    x = 100
    y = 100

    polygon_points = [
        Point(0, y),
        Point(x, y),
        Point(x / 2, 0)
    ]

    polygon = Polygon(polygon_points)
    points = [Point(x - 13, 93), Point(x - 20, 89), Point(x - 33, 69)]

    v = Algorithm(polygon)
    v.create_diagram(points=points, visualize_steps=False, verbose=False, visualize_result=False)

    sizes = [218.59, 629.68, 4151.73]

    calculated = [p.cell_size(2) for p in v.points]
    assert (sizes == calculated)


def test_lines_outside_triangle():
    x = 100
    y = 100

    polygon_points = [
        Point(0, y),
        Point(x, y),
        Point(x / 2, 0)
    ]

    polygon = Polygon(polygon_points)
    points = [
        Point(57, 75),
        Point(35, 85),
        Point(92, 98),
        Point(81, 87),
    ]

    v = Algorithm(polygon)
    v.create_diagram(points=points, visualize_steps=False, verbose=False, visualize_result=False)

    sizes = [2590.11, 2590.11, 147.0, 673.12]

    calculated = [p.cell_size(2) for p in v.points]
    assert (sizes == calculated)


def test_another_line_outside_triangle():
    x = 100
    y = 100

    polygon_points = [
        Point(0, y),
        Point(x, y),
        Point(x / 2, 0)
    ]

    polygon = Polygon(polygon_points)
    points = [
        Point(54, 90),
        Point(5, 95),
        Point(16, 85),
    ]

    v = Algorithm(polygon)
    v.create_diagram(points=points, visualize_steps=False, verbose=False, visualize_result=False)

    sizes = [3490.08, 1373.73, 1373.73]

    calculated = [p.cell_size(2) for p in v.points]
    assert (sizes == calculated)
