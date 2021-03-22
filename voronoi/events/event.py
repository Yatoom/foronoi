class Event:
    circle_event = False

    @property
    def xd(self):
        return 0

    @property
    def yd(self):
        return 0

    def __lt__(self, other):
        if self.yd == other.yd and self.xd == other.xd:
            return self.circle_event and not other.circle_event

        if self.yd == other.yd:
            return self.xd < other.xd

        # Switch y axis
        return self.yd > other.yd

    def __eq__(self, other):
        if other is None:
            return None
        return self.yd == other.yd and self.xd == other.xd

    def __ne__(self, other):
        return not self.__eq__(other)
