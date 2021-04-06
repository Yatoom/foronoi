from decimal import Decimal

from foronoi.graph.coordinate import Coordinate


class Arc:
    def __init__(self, origin: Coordinate, circle_event=None):
        """
        Each leaf of beach line, representing an arc `α`, stores one pointer to a node in the event queue, namely, the
        node that represents the circle event in which `α` will disappear. This pointer is None if no circle event
        exists where `α` will disappear, or this circle event has not been detected yet.

        Parameters
        ----------
        origin: Point
            The point that caused the arc
        circle_event: CircleEvent
            The pointer to the circle event in which the arc will disappear

        Attributes
        ----------
        origin: Point
            The point that caused the arc
        circle_event: CircleEvent
            The pointer to the circle event in which the arc will disappear
        """

        self.origin = origin
        self.circle_event = circle_event

    def __repr__(self):
        return f"Arc({self.origin.name})"

    def get_plot(self, x, sweep_line):
        """
        Computes all `y`-coordinates for given `x`-coordinates and the sweep line's `y`-coordinate.

        Parameters
        ----------
        x: np.array
            The input x-coordinates
        sweep_line: Decimal, float
            The y-coordinate of the sweep line
        Returns
        -------
        y: number, array-like
            A list of y-values
        """
        sweep_line = float(sweep_line)
        i = self.origin

        if i.y - sweep_line == 0:
            return None

        # Calculate the y value for each element of the x vector

        u = 2 * (i.y - sweep_line)
        v = (x ** 2 - 2 * i.x * x + i.x ** 2 + i.y ** 2 - sweep_line ** 2)
        y = v/u

        return y
