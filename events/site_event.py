from events.event import Event
from graph.point import Point


class SiteEvent(Event):
    def __init__(self, point: Point):
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
        return f"SiteEvent(x={self.point.x}, y={self.point.y}, pl={self.point.player})"