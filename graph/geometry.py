from graph import Point


# https://martin-thoma.com/how-to-check-if-two-line-segments-intersect/

class LineSegment:
    def __init__(self, a, b):
        self.first = a
        self.second = b

    def get_bounding_box(self):
        return [
            Point(min(self.first.x, self.second.x), min(self.first.y, self.second.y)),
            Point(max(self.first.x, self.second.x), max(self.first.y, self.second.y))
        ]


class Geometry(object):
    EPSILON = 0.000001

    @staticmethod
    def cross_product(a, b):
        return a.x * b.y - b.x * a.y

    @staticmethod
    def do_bounding_boxes_intersect(a, b):
        return a[0].x <= b[1].x and a[1].x >= b[0].x and a[0].y <= b[1].y and a[1].y >= b[0].y

    @staticmethod
    def is_point_on_line(a, b):
        # Move the image, so that a.first is on (0|0)
        aTmp = LineSegment(Point(0, 0), Point(a.second.x - a.first.x, a.second.y - a.first.y))
        bTmp = Point(b.x - a.first.x, b.y - a.first.y)
        r = Geometry.cross_product(aTmp.second, bTmp)
        return abs(r) < Geometry.EPSILON

    @staticmethod
    def is_point_right_of_line(a, b):
        # Move the image, so that a.first is on (0|0)
        aTmp = LineSegment(Point(0, 0), Point(a.second.x - a.first.x, a.second.y - a.first.y))
        bTmp = Point(b.x - a.first.x, b.y - a.first.y)
        return Geometry.cross_product(aTmp.second, bTmp) < 0

    @staticmethod
    def line_segment_touches_or_crosses_line(a, b):
        return Geometry.is_point_on_line(a, b.first) or Geometry.is_point_on_line(a, b.second) or (
            Geometry.is_point_right_of_line(a, b.first) and Geometry.is_point_right_of_line(a, b.second))

    @staticmethod
    def do_lines_intersect(a, b):
        box1 = a.get_bounding_box()
        box2 = b.get_bounding_box()
        Geometry.do_bounding_boxes_intersect(box1, box2) and Geometry.line_segment_touches_or_crosses_line(a, b) \
        and Geometry.line_segment_touches_or_crosses_line(b, a)
