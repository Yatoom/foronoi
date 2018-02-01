from nodes.point import Point


class SiteEvent:
    def __init__(self, point: Point):
        """
        Site event
        :param point:
        """
        self.point = point

    @property
    def y(self):
        return self.point.y

    @property
    def priority(self):
        return calc_priority(self.point.x, self.point.y)

    def __repr__(self):
        return f"SiteEvent(x={self.point.x}, y={self.point.y}, pl={self.point.player})"


class CircleEvent:
    def __init__(self, center: Point, radius: float, arc_node: "Node", triple=None):
        """
        Circle event.

        :param y: Lowest point on the circle
        :param arc_node: Pointer to the node in the beach line tree that holds the arc that will disappear
        :param triple: The tuple of points that caused the event
        """
        self.center = center
        self.radius = radius
        self.arc_pointer = arc_node
        self.is_valid = True
        self.triple = triple

    def __repr__(self):
        return f"CircleEvent({self.center}, {round(self.radius, 3)})"

    @property
    def y(self):
        return self.center.y - self.radius

    @property
    def priority(self):
        return calc_priority(self.center.x, self.center.y)

    def get_triangle(self):
        return (
            (self.triple[0].x, self.triple[0].y),
            (self.triple[1].x, self.triple[1].y),
            (self.triple[2].x, self.triple[2].y),
        )

    def remove(self):
        print(f"Circle event for {self.y} removed.")
        self.is_valid = False


def calc_priority(x, y):
    y = round(y, 5) * 10 ** 5
    x = round(x, 5) * 10 ** 5
    yx = -int(y * 10 ** 5 - x)
    return yx
