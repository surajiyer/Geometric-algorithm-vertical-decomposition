from Point import Point
from LineSegment import LineSegment
from GraphObject import GraphObject
import sys


class Trapezoid(GraphObject):
    """
    Class representing a trapezoid with top, bottom, leftp and rightp
    (2 line segments and 2 endpoints respectively)
    """

    def __init__(self, leftp, rightp, top, bottom):
        super().__init__()
        assert isinstance(leftp, Point) and isinstance(rightp, Point), 'leftp and/or rightp is not a point'
        self.leftp = leftp
        self.rightp = rightp

        assert isinstance(top, LineSegment) and isinstance(bottom,
                                                           LineSegment), 'top and/or bottom is not a line segment'
        self.top = top
        self.bottom = bottom
        self.leftneighbors = []
        self.rightneighbors = []

    def setLeftNeighbors(self, neighborarray):
        assert isinstance(neighborarray, list) and all(isinstance(n, Trapezoid) for n in neighborarray)

        # there are no left neighbors
        if self.top.p == self.bottom.p:
            return

        if self.leftp == self.top.p:
            l = self.bottom
            y_high = self.leftp.y
            y_low = l.getSlope() * self.leftp.x + l.getIntercept()
        elif self.leftp == self.bottom.p:
            l = self.top
            y_high = l.getSlope() * self.leftp.x + l.getIntercept()
            y_low = self.leftp.y
        else:
            l = self.bottom
            y_low = l.getSlope() * self.leftp.x + l.getIntercept()
            l = self.top
            y_high = l.getSlope() * self.leftp.x + l.getIntercept()

        for n in neighborarray:
            if self.leftp.x == n.rightp.x:
                print("setLeft", self)
                if n.rightp == n.top.q:
                    l = n.bottom
                    ny_high = n.rightp.y
                    ny_low = l.getSlope() * n.rightp.x + l.getIntercept()
                elif n.rightp == n.bottom.q:
                    l = n.top
                    ny_high = l.getSlope() * n.rightp.x + l.getIntercept()
                    ny_low = n.rightp.y
                else:
                    l = n.bottom
                    ny_low = l.getSlope() * n.rightp.x + l.getIntercept()
                    l = n.top
                    ny_high = l.getSlope() * n.rightp.x + l.getIntercept()

                # sides overlap
                if ny_low < y_high < ny_high or ny_low < y_low < ny_high or y_low < ny_low < y_high or y_low < ny_high < y_high:
                    print("ylow", y_low, "yhigh", y_high, "nylow", ny_low, "nyhigh", ny_high)
                    print(self, n)
                    sys.stdout.flush()
                    self.leftneighbors.append(n)

    def setRightNeighbors(self, neighborarray):
        assert isinstance(neighborarray, list) and all(isinstance(n, Trapezoid) for n in neighborarray)

        # there are no right neighbors
        if self.top.q == self.bottom.q:
            return

        if self.rightp == self.top.q:
            l = self.bottom
            y_high = self.rightp.y
            y_low = l.getSlope() * self.rightp.x + l.getIntercept()
        elif self.rightp == self.bottom.q:
            l = self.top
            y_high = l.getSlope() * self.rightp.x + l.getIntercept()
            y_low = self.rightp.y
        else:
            l = self.bottom
            y_low = l.getSlope() * self.rightp.x + l.getIntercept()
            l = self.top
            y_high = l.getSlope() * self.rightp.x + l.getIntercept()

        for n in neighborarray:
            if self.rightp.x == n.leftp.x:

                if n.leftp == n.top.p:
                    l = n.bottom
                    ny_high = n.leftp.y
                    ny_low = l.getSlope() * n.leftp.x + l.getIntercept()
                elif n.leftp == n.bottom.p:
                    l = n.top
                    ny_high = l.getSlope() * n.leftp.x + l.getIntercept()
                    ny_low = n.leftp.y
                else:
                    l = n.bottom
                    ny_low = l.getSlope() * n.leftp.x + l.getIntercept()
                    l = n.top
                    ny_high = l.getSlope() * n.leftp.x + l.getIntercept()

                # sides overlap
                if ny_low < y_high < ny_high or ny_low < y_low < ny_high or y_low < ny_low < y_high or y_low < ny_high < y_high:
                    self.rightneighbors.append(n)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return '<Trapezoid leftp:%s rightp:%s top:%s bottom:%s >' % (str(self.leftp), str(self.rightp),
                                                                     str(self.top), str(self.bottom))
