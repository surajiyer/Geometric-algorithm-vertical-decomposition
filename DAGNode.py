import copy
from Point import Point
from LineSegment import LineSegment
from Trapezoid import Trapezoid
from GraphObject import GraphObject


class DAGNode:
    """
        Class representing a Node in the DAG search structure
    """
    def __init__(self, graphObject, leftchild=None, rightchild=None):
        assert isinstance(graphObject, GraphObject)
        self.graphObject = graphObject
        self.leftchild = leftchild
        self.rightchild = rightchild

    def get_leftchild(self):
        return self._leftchild

    def set_leftchild(self, leftchild):
        assert isinstance(leftchild, DAGNode) or leftchild is None, 'leftchild should be a DAGNode!!!!!!!'
        self._leftchild = leftchild

    leftchild = property(get_leftchild, set_leftchild)

    def get_rightchild(self):
        return self._rightchild

    def set_rightchild(self, rightchild):
        assert isinstance(rightchild, DAGNode) or rightchild is None, 'rightchild should be a DAGNode!!!!!!!'
        self._rightchild = rightchild

    rightchild = property(get_rightchild, set_rightchild)

    def getQueryResult(self, queryPoint, lineSegment, queryPointExisted):
        """
            queryPoint: one of the endpoints of lineSegment
            lineSegment: lineSegment currently being inserted
        """

        assert isinstance(queryPoint, Point)
        assert isinstance(lineSegment, LineSegment)

        # we are an X-Node
        if isinstance(self.graphObject, Point):
            # if the querypoint is the same as this node
            if queryPoint == self.graphObject:
                # we do not want to change the querypoint itself
                newQueryPoint = copy.deepcopy(queryPoint)
                queryPointExisted = True

                # the querypoint is the left point of the line segment
                if queryPoint == lineSegment.p:
                    xDiff = (lineSegment.q.x - queryPoint.x)
                    yDiff = (lineSegment.q.y - queryPoint.y)
                elif queryPoint == lineSegment.q:
                    # the querypoint is the right point of the line segment
                    xDiff = (lineSegment.p.x - queryPoint.x)
                    yDiff = (lineSegment.p.y - queryPoint.y)
                else:
                    raise ValueError('invalid querypoint!')

                # (p2.x - p1.x) * t --> xDiff * t
                newQueryPoint.x = queryPoint.x + xDiff * (0.1 / lineSegment.getLength())

                # (p2.y - p1.y) * t --> yDiff * t
                newQueryPoint.y = queryPoint.y + yDiff * (0.1 / lineSegment.getLength())

                return self.getQueryResult(newQueryPoint, lineSegment, queryPointExisted)
            else:
                # if querypoint lies (completely) left of this point
                if queryPoint.x < self.graphObject.x:
                    return self.leftchild.getQueryResult(queryPoint, lineSegment, queryPointExisted)
                elif queryPoint.x > self.graphObject.x:
                    return self.rightchild.getQueryResult(queryPoint, lineSegment, queryPointExisted)
                else:
                    if isinstance(self.leftchild.graphObject, LineSegment):
                        if self.leftchild.graphObject.aboveLine(queryPoint):
                            return self.rightchild.getQueryResult(queryPoint, lineSegment, queryPointExisted)
                        else:
                            return self.leftchild.getQueryResult(queryPoint, lineSegment, queryPointExisted)
                    return self.rightchild.getQueryResult(queryPoint, lineSegment, queryPointExisted)
                    # TODO: handle points with same x
        elif isinstance(self.graphObject, LineSegment):
            # we are a Y-Node
            if self.graphObject.aboveLine(queryPoint):
                return self.rightchild.getQueryResult(queryPoint, lineSegment, queryPointExisted)
            else:
                return self.leftchild.getQueryResult(queryPoint, lineSegment, queryPointExisted)
        elif isinstance(self.graphObject, Trapezoid):
            # we are a leaf
            return self, queryPointExisted
        else:
            raise ValueError('invalid DAG node!')

    def modify(self, newNode):
        assert isinstance(newNode, DAGNode)
        self.graphObject = newNode.graphObject
        self.leftchild = newNode.leftchild
        self.rightchild = newNode.rightchild

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return '(leftchild: %s, rightchild: %s, graphObject %s)' % (
            'YES' if self.leftchild else 'NO', 'YES' if self.rightchild else 'NO', self.graphObject)
