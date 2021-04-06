from foronoi.graph.point import Point
from foronoi.events.event import Event
from foronoi.observers.subject import Subject


class SiteEvent(Event, Subject):
    circle_event = False

    def __init__(self, point: Point):
        """
        Site event
        :param point:
        """
        super().__init__()
        self.point = point

    @property
    def xd(self):
        return self.point.xd

    @property
    def yd(self):
        return self.point.yd

    def __repr__(self):
        return f"SiteEvent(x={self.point.xd}, y={self.point.yd})"
