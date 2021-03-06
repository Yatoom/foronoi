from decimal import Decimal


class Coordinate:
    def __init__(self, x=None, y=None):
        """
        A point in 2D space.
        :param x: (float) The x-coordinate
        :param y: (float) The y-coordinate
        """
        self._x: Decimal = Decimal(str(x)) if x is not None else Decimal()
        self._y: Decimal = Decimal(str(y)) if y is not None else Decimal()

    def __repr__(self):
        return f"({round(self.x, 3)}, {round(self.y, 3)})"

    def __sub__(self, other):
        return Coordinate(x=self.x - other.x, y=self.y - other.y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: float):
        self._x = Decimal(str(value))

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: float):
        self._y = Decimal(str(value))


    def as_floats(self):
        return FloatCoordinate(self.x, self.y)


class FloatCoordinate:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
