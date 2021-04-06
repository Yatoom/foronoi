from decimal import Decimal


class Coordinate:
    def __init__(self, x=None, y=None):
        """
        A point in 2D space

        Parameters
        ----------
        x: float
            The x-coordinate
        y: float
            The y-coordinate
        """
        self._xd: Decimal = Coordinate._to_dec(x)
        self._yd: Decimal = Coordinate._to_dec(y)

    def __sub__(self, other):
        return Coordinate(x=self.xd - other.xd, y=self.yd - other.yd)

    def __repr__(self):
        return f"Coord({self.xd:.2f}, {self.yd:.2f})"

    @staticmethod
    def _to_dec(value):
        return Decimal(str(value)) if value is not None else None

    @property
    def x(self):
        """
        Get the x-coordinate as float

        Returns
        -------
        x: float
            The x-coordinate
        """
        return float(self._xd)

    @property
    def y(self):
        """
        Get the y-coordinate as float

        Returns
        -------
        y: float
            The y-coordinate
        """
        return float(self._yd)

    @x.setter
    def x(self, value):
        """
        Stores the x-coordinate as Decimal

        Parameters
        ----------
        value: float
            The x-coordinate as float
        """
        self._xd = Coordinate._to_dec(value)

    @y.setter
    def y(self, value):
        """
        Stores the y-coordinate as Decimal

        Parameters
        ----------
        value: float
            The y-coordinate as float
        """
        self._yd = Coordinate._to_dec(value)

    @property
    def xy(self):
        """
        Get a (x, y) tuple

        Parameters
        ----------
        xy: (float, float)
            A tuple of the (x, y)-coordinate
        """
        return self.x, self.y

    @property
    def xd(self):
        """
        Get the x-coordinate as Decimal

        Returns
        -------
        x: Decimal
            The x-coordinate
        """
        return self._xd

    @xd.setter
    def xd(self, value: float):
        self._xd = Coordinate._to_dec(value)

    @property
    def yd(self):
        """
        Get the y-coordinate as Decimal

        Returns
        -------
        y: Decimal
            The y-coordinate
        """
        return self._yd

    @yd.setter
    def yd(self, value: float):
        self._yd = Coordinate._to_dec(value)
