class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_x(self, x):
        assert isinstance(x, int) and x >= 0, \
            'Points must have positive integer x-coordinate: %d' % x
        self._x = x

    def set_y(self, y):
        assert isinstance(y, int) and y >= 0, \
            'Points must have positive integer y-coordinate: %d' % y
        self._y = y

    x = property(get_x, set_x)
    y = property(get_y, set_y)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return '(%d, %d)' % (self.x, self.y)
