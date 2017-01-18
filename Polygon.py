from Point import Point
from LineSegment import LineSegment


class Polygon:
    """
    Class representing a polygon with a set of points and edges between them.
    """
    def __init__(self, points):
        assert isinstance(points, list) and all(isinstance(p, Point) for p in points)
        self.V = points

        # check if points assume general position
        assert self.is_general_position, 'Input points must have distinct x-coordinates'

        # create edges and randomize
        self.E = []
        for i, p in enumerate(points):
            self.E.append(LineSegment(p, points[(i + 1) % len(points)]))

        # check if points represent a simple polygon
        assert self.is_simple_polygon, 'Input polygon must be simple'

    @property
    def is_general_position(self) -> bool:
        """
        Check if points assume general position by checking each
        vertex has distinct x-coordinate
        :return:
        """
        x_s = [p.x for p in self.V]
        print(sorted(x_s))
        return len(x_s) == len(set(x_s))

    @property
    def is_simple_polygon(self) -> bool:
        """
        Check if the given polygon is simple or complex.
        :return: True if simple. False otherwise.
        """
        for i, s1 in enumerate(self.E):
            for j, s2 in enumerate(self.E[i + 1:]):
                if s1.intersects(s2):
                    print('Segments %s and %s intersect' % (str(s1), str(s2)))
                    return False
        return True

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
