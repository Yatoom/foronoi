from data_structures.dcel import Point


def polygon_area(points: list[Point]) -> float:
    """
    Given the corners of a simple polygon, computes and returns the area of the polygon.
    The area is calculated using the shoelace formula
    """
    area = 0.0
    for i in range(len(points)):
        area += points[i].x * points[(i + 1) % len(points)].y
        area -= points[(i + 1) % len(points)].x * points[i].y
    return abs(area) / 2.0
