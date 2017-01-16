import copy
from Point import Point
from LineSegment import LineSegment
import Trapezoid
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

    def set_left_child(self, left_child):
        assert isinstance(left_child, DAGNode) or left_child is None, 'left_child should be a DAGNode!'
        self._left_child = left_child

    left_child = property(get_left_child, set_left_child)

    def get_right_child(self):
        return self._right_child

    def set_right_child(self, right_child):
        assert isinstance(right_child, DAGNode) or right_child is None, 'right_child should be a DAGNode!'
        self._right_child = right_child

    right_child = property(get_right_child, set_right_child)

    def getOffsetPoint(self, query_point, line_seg) -> Point:
        assert isinstance(query_point, Point)
        assert isinstance(line_seg, LineSegment)

        new_query_point = copy.deepcopy(query_point)
        # the query point is the left point of the line segment
        if query_point == line_seg.p:
            x_diff = (line_seg.q.x - query_point.x)
            y_diff = (line_seg.q.y - query_point.y)
        elif query_point == line_seg.q:
            # the query point is the right point of the line segment
            x_diff = (line_seg.p.x - query_point.x)
            y_diff = (line_seg.p.y - query_point.y)
        else:
            raise ValueError('Invalid query point!')

        # (p2.x - p1.x) * t --> xDiff * t
        new_query_point.x = query_point.x + x_diff * (0.1 / line_seg.getLength())

        # (p2.y - p1.y) * t --> yDiff * t
        new_query_point.y = query_point.y + y_diff * (0.1 / line_seg.getLength())

        return new_query_point

    def getQueryResult(self, query_point, line_seg, query_point_existed=False):
        """
        queryPoint: one of the endpoints of lineSegment
        lineSegment: lineSegment currently being inserted
        """
        assert isinstance(query_point, Point)
        assert isinstance(line_seg, LineSegment)

        # we are an X-Node
        if isinstance(self.graphObject, Point):
            # if the query point is the same as this node
            if query_point == self.graphObject:
                query_point_existed = True
                new_query_point = self.getOffsetPoint(query_point, line_seg)
                return self.getQueryResult(new_query_point, line_seg, query_point_existed)
            else:
                # if query point lies (completely) left of this point
                if query_point.x < self.graphObject.x:
                    return self.left_child.getQueryResult(query_point, line_seg, query_point_existed)
                elif query_point.x > self.graphObject.x:
                    return self.right_child.getQueryResult(query_point, line_seg, query_point_existed)
                else:
                    new_query_point = self.getOffsetPoint(query_point, line_seg)
                    return self.getQueryResult(new_query_point, line_seg, query_point_existed)
        elif isinstance(self.graphObject, LineSegment):
            # we are a Y-Node
            if self.graphObject.aboveLine(query_point):
                return self.right_child.getQueryResult(query_point, line_seg, query_point_existed)
            else:
                return self.left_child.getQueryResult(query_point, line_seg, query_point_existed)
        elif isinstance(self.graphObject, Trapezoid.Trapezoid):
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
