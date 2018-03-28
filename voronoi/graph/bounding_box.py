from voronoi.graph import Polygon, Point


class BoundingBox(Polygon):

    def __init__(self, left_x, right_x, bottom_y, top_y):
        points = [
            Point(left_x, top_y),
            Point(right_x, top_y),
            Point(right_x, bottom_y),
            Point(left_x, bottom_y)
        ]

        super().__init__(points)
