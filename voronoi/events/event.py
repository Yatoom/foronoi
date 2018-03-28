class Event:
    circle_event = False

    @property
    def x(self):
        return 0

    @property
    def y(self):
        return 0

    def __lt__(self, other):
        if self.y == other.y and self.x == other.x:
            return self.circle_event and not other.circle_event

        if self.y == other.y:
            return self.x < other.x

        # Switch y axis
        return self.y > other.y

    def __eq__(self, other):
        if other is None:
            return None
        return self.y == other.y and self.x == other.x

    def __ne__(self, other):
        return not self.__eq__(other)
