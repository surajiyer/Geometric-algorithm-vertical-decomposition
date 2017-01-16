from Trapezoid import Trapezoid


class TrapezoidMap:
    """
    Class representing a trapezoidal map with a set of trapezoids
    """

    def __init__(self, trapezoids):
        assert isinstance(trapezoids, list) and all(isinstance(n, Trapezoid) for n in trapezoids)
        self.trapezoids = trapezoids

    def addTrapezoid(self, trapezoids):
        assert isinstance(trapezoids, list) and all(isinstance(t, Trapezoid) for t in trapezoids)
        self.trapezoids.extend(trapezoids)

    def deleteTrapezoidFromMap(self, trapezoids):
        self.trapezoids = [t for t in self.trapezoids if t not in trapezoids]
        # self.trapezoids.remove(trapezoid)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return '<Trapezoidal map -> Trapezoids: %s>' % (str(self.trapezoids))
