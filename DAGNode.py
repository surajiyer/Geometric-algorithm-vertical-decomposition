import copy
from Point import Point
from LineSegment import LineSegment
from Trapezoid import Trapezoid
from GraphObject import GraphObject


class DAGNode:
    """
        Class representing a Node in the DAG search structure
    """

    def __init__(self, graph_object, left_child=None, right_child=None):
        assert isinstance(graph_object, GraphObject)
        self.graphObject = graph_object
        self.left_child = left_child
        self.right_child = right_child

    def get_left_child(self):
        return self._left_child

    def set_left_child(self, leftchild):
        assert isinstance(leftchild, DAGNode) or leftchild is None, 'leftchild should be a DAGNode!!!!!!!'
        self._left_child = leftchild

    left_child = property(get_left_child, set_left_child)

    def get_right_child(self):
        return self._right_child

    def set_right_child(self, rightchild):
        assert isinstance(rightchild, DAGNode) or rightchild is None, 'rightchild should be a DAGNode!!!!!!!'
        self._right_child = rightchild

    right_child = property(get_right_child, set_right_child)

    def getOffsetPoint(self, query_point, line_seg) -> Point:
        assert isinstance(query_point, Point)
        assert isinstance(line_seg, LineSegment)

        new_query_point = copy.deepcopy(query_point)
        # the querypoint is the left point of the line segment
        if query_point == line_seg.p:
            xDiff = (line_seg.q.x - query_point.x)
            yDiff = (line_seg.q.y - query_point.y)
        elif query_point == line_seg.q:
            # the querypoint is the right point of the line segment
            xDiff = (line_seg.p.x - query_point.x)
            yDiff = (line_seg.p.y - query_point.y)
        else:
            raise ValueError('invalid querypoint!')

        # (p2.x - p1.x) * t --> xDiff * t
        new_query_point.x = query_point.x + xDiff * (0.1 / line_seg.getLength())

        # (p2.y - p1.y) * t --> yDiff * t
        new_query_point.y = query_point.y + yDiff * (0.1 / line_seg.getLength())

        return new_query_point

    def getQueryResult(self, queryPoint, lineSegment, query_point_existed=False):
        """
        queryPoint: one of the endpoints of lineSegment
        lineSegment: lineSegment currently being inserted
        """
        assert isinstance(queryPoint, Point)
        assert isinstance(lineSegment, LineSegment)

        # we are an X-Node
        if isinstance(self.graphObject, Point):
            # if the query point is the same as this node
            if queryPoint == self.graphObject:
                query_point_existed = True
                new_query_point = self.getOffsetPoint(queryPoint, lineSegment)
                return self.getQueryResult(new_query_point, lineSegment, query_point_existed)
            else:
                # if query point lies (completely) left of this point
                if queryPoint.x < self.graphObject.x:
                    return self.left_child.getQueryResult(queryPoint, lineSegment, query_point_existed)
                elif queryPoint.x > self.graphObject.x:
                    return self.right_child.getQueryResult(queryPoint, lineSegment, query_point_existed)
                else:
                    new_query_point = self.getOffsetPoint(queryPoint, lineSegment)
                    return self.getQueryResult(new_query_point, lineSegment, query_point_existed)
        elif isinstance(self.graphObject, LineSegment):
            # we are a Y-Node
            if self.graphObject.aboveLine(queryPoint):
                return self.right_child.getQueryResult(queryPoint, lineSegment, query_point_existed)
            else:
                return self.left_child.getQueryResult(queryPoint, lineSegment, query_point_existed)
        elif isinstance(self.graphObject, Trapezoid):
            # we are a leaf
            return self, query_point_existed
        else:
            raise ValueError('invalid DAG node!')

    def modify(self, new_node):
        assert isinstance(new_node, DAGNode)
        self.graphObject = new_node.graphObject
        self.left_child = new_node.left_child
        self.right_child = new_node.right_child

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return '(left_child: %s, right_child: %s, graphObject %s)' % (
            'YES' if self.left_child else 'NO', 'YES' if self.right_child else 'NO', self.graphObject)
