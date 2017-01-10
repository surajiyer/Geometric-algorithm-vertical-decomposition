from Point import Point
from LineSegment import LineSegment
from GraphObject import GraphObject


class Trapezoid(GraphObject):
    """
    Class representing a trapezoid with top, bottom, leftp and rightp
    (2 line segments and 2 endpoints respectively)
    """

    def __init__(self, leftp, rightp, top, bottom, leftneighbors, rightneighbors):
        super().__init__()
        assert isinstance(leftp, Point) and isinstance(rightp, Point), 'leftp and/or rightp is not a point'
        self.leftp = leftp
        self.rightp = rightp

        assert isinstance(top, LineSegment) and isinstance(bottom,
                                                           LineSegment), 'top and/or bottom is not a line segment'
        self.top = top
        self.bottom = bottom

        assert isinstance(leftneighbors, list) and all(isinstance(n, Trapezoid) for n in leftneighbors)
        assert isinstance(rightneighbors, list) and all(isinstance(n, Trapezoid) for n in rightneighbors)
        self.leftneighbors = leftneighbors
        self.rightneighbors = rightneighbors

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return '<Trapezoid leftp:%s rightp:%s top:%s bottom:%s >' % (str(self.leftp), str(self.rightp),
                                                                     str(self.top), str(self.bottom))
