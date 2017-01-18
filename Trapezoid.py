from Point import Point
from LineSegment import LineSegment
from GraphObject import GraphObject
import DAGNode as dag
# from llist import dllistnode


class Trapezoid(GraphObject):
    """
    Class representing a trapezoid with top, bottom, left_p and right_p
    (2 line segments and 2 endpoints respectively)
    """

    def __init__(self, left_p, right_p, top, bottom):
        super().__init__()
        assert isinstance(left_p, Point) and isinstance(right_p, Point), 'left_p and/or right_p is not a point'
        assert isinstance(top, LineSegment) and isinstance(bottom,
                                                           LineSegment), 'top and/or bottom is not a line segment'
        self.left_p = left_p
        self.right_p = right_p
        self.top = top
        self.bottom = bottom
        self.left_neighbors = set()
        self.right_neighbors = set()
        self._node = dag.DAGNode(self)
        # self._dllistnode = dllistnode(self)

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, node):
        self._node.modify(node)

    def setLeftNeighbors(self, neighbors, auto=False):
        assert isinstance(neighbors, set) and all(isinstance(n, Trapezoid) for n in neighbors)

        if not neighbors:
            return

        # there are no left neighbors
        if self.top.p == self.bottom.p:
            return

        if self.left_p.x == self.right_p.x:
            """ zero-width trapezoid """
            y_high = self.left_p.y
            y_low = self.right_p.y
        elif self.left_p == self.top.p:
            l = self.bottom
            y_high = self.left_p.y
            y_low = l.slope * self.left_p.x + l.intercept
        elif self.left_p == self.bottom.p:
            l = self.top
            y_high = l.slope * self.left_p.x + l.intercept
            y_low = self.left_p.y
        else:
            l = self.bottom
            y_low = l.slope * self.left_p.x + l.intercept
            l = self.top
            y_high = l.slope * self.left_p.x + l.intercept

        for n in neighbors:
            if n in self.left_neighbors:
                continue
            if self.left_p.x == n.right_p.x:
                if n.left_p.x == n.right_p.x:
                    """ zero-width trapezoid """
                    ny_high = n.left_p.y
                    ny_low = n.right_p.y
                elif n.right_p == n.top.q:
                    l = n.bottom
                    ny_high = n.right_p.y
                    ny_low = l.slope * n.right_p.x + l.intercept
                elif n.right_p == n.bottom.q:
                    l = n.top
                    ny_high = l.slope * n.right_p.x + l.intercept
                    ny_low = n.right_p.y
                else:
                    l = n.bottom
                    ny_low = l.slope * n.right_p.x + l.intercept
                    l = n.top
                    ny_high = l.slope * n.right_p.x + l.intercept

                # sides overlap
                if ny_low < y_high < ny_high or ny_low < y_low < ny_high \
                        or y_low < ny_low < y_high or y_low < ny_high < y_high \
                        or (y_low == ny_low and y_high == ny_high):
                    self.left_neighbors.add(n)
                    if not auto:
                        n.setRightNeighbors({self}, auto=True)

    def setRightNeighbors(self, neighbors, auto=False):
        assert isinstance(neighbors, set) and all(isinstance(n, Trapezoid) for n in neighbors)

        if not neighbors:
            return

        # there are no right neighbors
        if self.top.q == self.bottom.q:
            return

        if self.left_p.x == self.right_p.x:
            y_high = self.left_p.y
            y_low = self.right_p.y
        elif self.right_p == self.top.q:
            l = self.bottom
            y_high = self.right_p.y
            y_low = l.slope * self.right_p.x + l.intercept
        elif self.right_p == self.bottom.q:
            l = self.top
            y_high = l.slope * self.right_p.x + l.intercept
            y_low = self.right_p.y
        else:
            l = self.bottom
            y_low = l.slope * self.right_p.x + l.intercept
            l = self.top
            y_high = l.slope * self.right_p.x + l.intercept

        for n in neighbors:
            if n in self.right_neighbors:
                continue
            if self.right_p.x == n.left_p.x:
                if n.left_p.x == n.right_p.x:
                    """ zero-width trapezoid """
                    ny_high = n.left_p.y
                    ny_low = n.right_p.y
                elif n.left_p == n.top.p:
                    l = n.bottom
                    ny_high = n.left_p.y
                    ny_low = l.slope * n.left_p.x + l.intercept
                elif n.left_p == n.bottom.p:
                    l = n.top
                    ny_high = l.slope * n.left_p.x + l.intercept
                    ny_low = n.left_p.y
                else:
                    l = n.bottom
                    ny_low = l.slope * n.left_p.x + l.intercept
                    l = n.top
                    ny_high = l.slope * n.left_p.x + l.intercept

                # sides overlap
                if ny_low < y_high < ny_high or ny_low < y_low < ny_high \
                        or y_low < ny_low < y_high or y_low < ny_high < y_high \
                        or (y_low == ny_low and y_high == ny_high):
                    self.right_neighbors.add(n)
                    if not auto:
                        n.setLeftNeighbors({self})

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            # x, y = copy.copy(self.__dict__), copy.copy(other.__dict__)
            # x.pop("_node", None)
            # y.pop("_node", None)
            # return x == y
            # return self.__dict__ == other.__dict__
            return self.left_p == other.left_p and self.right_p == other.right_p \
                   and self.top == other.top and self.bottom == other.bottom
        return super().__eq__(other)

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self == other
        return NotImplemented

    def __repr__(self):
        return '<Trapezoid left_p:%s right_p:%s top:%s bottom:%s>' % (str(self.left_p), str(self.right_p),
                                                                      str(self.top), str(self.bottom))
