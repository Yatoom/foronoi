from voronoi.events.event import Event
from voronoi.graph.coordinate import DecimalCoordinate
from voronoi.observers.subject import Subject


class SiteEvent(Event, Subject):
    circle_event = False

    def __init__(self, point: DecimalCoordinate):
        """
        Site event
        :param point:
        """
        super().__init__()
        self.point = point

    @property
    def x(self):
        return self.point.x

    @property
    def y(self):
        return self.point.y

    def __repr__(self):
        return f"SiteEvent(x={self.point.x}, y={self.point.y})"
