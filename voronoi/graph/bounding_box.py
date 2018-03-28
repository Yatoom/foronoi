from voronoi.graph import Polygon, Coordinate


class BoundingBox(Polygon):

    def __init__(self, left_x, right_x, bottom_y, top_y):
        points = [
            Coordinate(left_x, top_y),
            Coordinate(right_x, top_y),
            Coordinate(right_x, bottom_y),
            Coordinate(left_x, bottom_y)
        ]

        super().__init__(points)
