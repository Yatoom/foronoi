from voronoi.graph.coordinate import Coordinate


class Arc:
    """
    Each leaf of beach line, representing an arc α, stores one pointer to a node in the event queue, namely, the node
    that represents the circle event in which α will disappear. This pointer is None if no circle event exists where α
    will disappear, or this circle event has not been detected yet.
    """

    def __init__(self, origin: Coordinate, circle_event=None):
        """
        :param origin: The point that caused the arc
        :param circle_event: The pointer to the circle event in which the arc will disappear
        """
        self.origin = origin
        self.circle_event = circle_event

    def __repr__(self):
        return f"Arc({self.origin.name})"

    def get_plot(self, x, sweep_line):
        """
        Method for plotting the arc.
        Will return the y-coordinates for all the x coordinates that are given as input.
        :param x: The input x-coordinates
        :param sweep_line: The y-coordinate of the sweep line
        :return: A list of y-values
        """
        sweep_line = sweep_line
        i = self.origin

        if i.y - sweep_line == 0:
            return None

        # Calculate the y value for each element of the x vector

        u = 2 * (i.y - sweep_line)
        v = (x ** 2 - 2 * i.x * x + i.x ** 2 + i.y ** 2 - sweep_line ** 2)
        y = v/u

        return y
