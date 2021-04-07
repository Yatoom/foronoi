from foronoi.graph import Polygon, Coordinate


class BoundingBox(Polygon):

    def __init__(self, left_x, right_x, bottom_y, top_y):
        """
        Convenience method to create a bounding box. Extends :class:`foronoi.graph.Polygon`.

        Parameters
        ----------
        left_x: float
            The x-coordinate of the left border
        right_x: float
            The x-coordinate of the right border
        bottom_y: float
            The y-coordinate of the bottom border
        top_y: float
            The y-coordinate of the top border
        """
        points = [
            (left_x, top_y),
            (right_x, top_y),
            (right_x, bottom_y),
            (left_x, bottom_y)
        ]

        super().__init__(points)
