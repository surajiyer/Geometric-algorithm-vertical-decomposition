from Point import Point


class LineSegment:
    """
    Class to represent a line segment with 2 endpoints
    """
    def __init__(self, p, q):
        assert isinstance(p, Point) and isinstance(q, Point)
        self.p = p
        self.q = q

    @staticmethod
    def on_segment(p, q, r):
        """
        Given three colinear points p, q, r, the function checks if point q lies on line segment 'pr'
        :param p: Vertex
        :param q: Vertex
        :param r: Vertex
        :return:
        """
        assert isinstance(p, Point) and isinstance(q, Point) and isinstance(r, Point)
        return min(p.x, r.x) <= q.x <= max(p.x, r.x) and min(p.y, r.y) <= q.y <= max(p.y, r.y)

    @staticmethod
    def ccw(p, q, r) -> int:
        """
        Check if three points are listed in counter-clockwise order
        :param p:
        :param q:
        :param r:
        :return:
        """
        assert isinstance(p, Point) and isinstance(q, Point) and isinstance(r, Point)
        val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)

        # collinear
        if val == 0:
            return 0

        # -1 for clockwise, 1 for counter-clockwise
        return -1 if val > 0 else 1

    def intersects(self, other) -> bool:
        """
        Return true if line segments 'self' and 'other' intersect.
        http://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
        :param other:
        :return:
        """
        assert isinstance(other, LineSegment)

        # check if they share an endpoint
        if self.p == other.p or self.q == other.q\
                or self.p == other.q or self.q == other.p:
            return False

        o1 = self.ccw(self.p, self.q, other.p)
        o2 = self.ccw(self.p, self.q, other.q)
        o3 = self.ccw(other.p, other.q, self.p)
        o4 = self.ccw(other.p, other.q, self.q)

        if (self.p == Point(1, 1) and self.q == Point(2, 2)
            and other.p == Point(2, 2) and other.q == Point(3, 1)):
            print(o1, o2, o3, o4)

        # General case
        if o1 != o2 and o3 != o4:
            return True

        # Special cases
        # A, B and C are colinear and C lies on segment AB
        if o1 == 0 and self.on_segment(self.p, other.p, self.q): return True

        # A, B and C are colinear and D lies on segment AB
        if o2 == 0 and self.on_segment(self.p, other.q, self.q): return True

        # C, D and A are colinear and A lies on segment CD
        if o3 == 0 and self.on_segment(other.p, self.p, other.q): return True

        # C, D and B are colinear and B lies on segment CD
        if o4 == 0 and self.on_segment(other.p, self.q, other.q): return True

        return False

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return '<Segment p:%s q:%s>' % (str(self.p), str(self.q))