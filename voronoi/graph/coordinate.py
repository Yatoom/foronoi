from decimal import Decimal


class Coordinate:
    def __init__(self, x=None, y=None):
        """
        A point in 2D space.
        :param x: (float) The x-coordinate
        :param y: (float) The y-coordinate
        """
        self._xd: Decimal = Coordinate.to_dec(x)
        self._yd: Decimal = Coordinate.to_dec(y)

    def __sub__(self, other):
        return Coordinate(x=self.xd - other.xd, y=self.yd - other.yd)

    def __repr__(self):
        return f"Coord({self.xd:.2f}, {self.yd:.2f})"

    @staticmethod
    def to_dec(value):
        return Decimal(str(value)) if value is not None else None

    @property
    def x(self):
        return float(self._xd)

    @property
    def y(self):
        return float(self._yd)

    @x.setter
    def x(self, value):
        self._xd = Coordinate.to_dec(value)

    @y.setter
    def y(self, value):
        self._yd = Coordinate.to_dec(value)

    @property
    def xy(self):
        return self.x, self.y

    @property
    def xd(self):
        return self._xd

    @xd.setter
    def xd(self, value: float):
        self._xd = Coordinate.to_dec(value)

    @property
    def yd(self):
        return self._yd

    @yd.setter
    def yd(self, value: float):
        self._yd = Coordinate.to_dec(value)
