from algorithm import Algorithm
from nodes.bounding_box import BoundingBox
from nodes.point import Point


def test_grid():
    # Testing square grid
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
    # Testing diamond
    points = [
        Point(5, 7.5),
        Point(2.5, 5),
        Point(7.5, 5),
        Point(6, 3),
    ]
    v = Algorithm(BoundingBox(0, 10, 0, 10))
    v.create_diagram(points=points, visualize_steps=False, visualize_result=False, verbose=False)
    sizes = [26.01, 202.48, 15.87, 95.95, 12.32, 108.89, 14.05, 57.78, 31.34, 12.08, 31.21, 17.03]
    calculated = [p.cell_size(2) for p in v.points]
    assert (sizes == calculated)


def test_martijn():
    points = [
        Point(2.241, 3.594),
        Point(3.568, 3.968),
        Point(6.401, 16.214),
        Point(2.925, 18.298),
    ]

    v = Algorithm(BoundingBox(-1, 26, -1, 26))
    v.create_diagram(points=points, visualize_steps=False, verbose=False, visualize_result=False)
    sizes = [42.9, 209.3, 380.84, 95.97]
    calculated = [p.cell_size(2) for p in v.points]
    assert (sizes == calculated)


def test_desmos():
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
