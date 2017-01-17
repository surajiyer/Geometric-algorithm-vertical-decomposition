from GraphObject import GraphObject


class Point(GraphObject):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_x(self, x):
        assert isinstance(float(x), float) and x >= 0.0, \
            'Points must have positive integer x-coordinate: %d' % x
        self._x = x

    def set_y(self, y):
        assert isinstance(float(y), float) and y >= 0.0, \
            'Points must have positive integer y-coordinate: %d' % y
        self._y = y

    x = property(get_x, set_x)
    y = property(get_y, set_y)

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self == other
        return NotImplemented

    def __repr__(self):
        return '(%.2f, %.2f)' % (self.x, self.y)
