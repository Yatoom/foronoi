from foronoi.graph.point import Point
from foronoi.events.event import Event
from foronoi.observers.subject import Subject


class SiteEvent(Event, Subject):
    circle_event = False

    def __init__(self, point: Point):
        """
        A site event.

        Parameters
        ----------
        point: Point
            The point that causes the site event.
        """
        super().__init__()
        self.point = point

    @property
    def xd(self):
        """
        The x-coordinate (in Decimal format) of the point, which functions as the secondary priority of this event.

        Returns
        -------
        x: Decimal
        """
        return self.point.xd

    @property
    def yd(self):
        """
        The y-coordinate (in Decimal format) of the point, which functions as the primary priority of this event.

        Returns
        -------
        y: Decimal
        """
        return self.point.yd

    def __repr__(self):
        return f"SiteEvent(x={self.point.xd}, y={self.point.yd})"
