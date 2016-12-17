from Point import Point
from LineSegment import LineSegment

class Trapezoid:
    """
    Class representing a trapezoid with top, bottom, leftp and rightp
    (2 line segments and 2 endpoints respectively)
    """
    def __init__(self, leftp, rightp, top, bottom, neighbors):
        assert isinstance(leftp, Point) and isinstance(rightp, Point),'leftp and/or rightp is not a point'
        self.leftp = leftp
        self.rightp = rightp

        assert isinstance(top, LineSegment) and isinstance(bottom, LineSegment),'top and/or bottom is not a line segment'
        self.top = top
        self.bottom = bottom

        assert isinstance(neighbors, list) and all(isinstance(n, Trapezoid) for n in neighbors)
        assert len(neighbors) <= 4, 'Maximum number of neighbors for a trapezoid is 4'
        self.neighbors = neighbors

        print("<Trapezoid leftp:%s rightp:%s top:%s bottom:%s neighbors:%s>" % (
        str(self.leftp), str(self.rightp), str(self.top), str(self.bottom), str(self.neighbors)))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return '<Trapezoid leftp:%s rightp:%s top:%s bottom:%s Neighbors:%s>' % (str(self.leftp), str(self.rightp),
                                                                                 str(self.top), str(self.bottom),
                                                                                 str(self.neighbors))