from voronoi.events.event import Event
from voronoi.graph.coordinate import Coordinate


class SiteEvent(Event):
    circle_event = False

    def __init__(self, point: Coordinate):
        """
        Site event
        :param point:
        """
        self.point = point

    @property
    def x(self):
        return self.point.x

    @property
    def y(self):
        return self.point.y

    def __repr__(self):
        return f"SiteEvent(x={self.point.x}, y={self.point.y})"
