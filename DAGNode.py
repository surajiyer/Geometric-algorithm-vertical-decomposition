import copy
import Text

from GraphObject import GraphObject
from Point import Point
from LineSegment import LineSegment
import Trapezoid


class DAGNode:
    """
    Class representing a Node in the DAG search structure
    """

    def __init__(self, graph_object, left_child=None, right_child=None):
        assert isinstance(graph_object, GraphObject)
        self.graph_object = graph_object
        self.left_child = left_child
        self.right_child = right_child

    @property
    def left_child(self):
        return self._left_child

    @left_child.setter
    def left_child(self, left_child):
        assert isinstance(left_child, DAGNode) or left_child is None, 'left_child should be a DAGNode!'
        self._left_child = left_child

    @property
    def right_child(self):
        return self._right_child

    @right_child.setter
    def right_child(self, right_child):
        assert isinstance(right_child, DAGNode) or right_child is None, 'right_child should be a DAGNode!'
        self._right_child = right_child

    def get_offset_point(self, query_point, line_seg) -> Point:
        assert isinstance(query_point, Point)
        assert isinstance(line_seg, LineSegment)

        new_query_point = copy.copy(query_point)
        if query_point == line_seg.p:
            # the query point is the left point of the line segment
            x_diff = (line_seg.q.x - query_point.x)
            y_diff = (line_seg.q.y - query_point.y)
        elif query_point == line_seg.q:
            # the query point is the right point of the line segment
            x_diff = (line_seg.p.x - query_point.x)
            y_diff = (line_seg.p.y - query_point.y)
        else:
            raise ValueError('Invalid query point!')

        # (p2.x - p1.x) * t --> xDiff * t
        new_query_point.x = query_point.x + x_diff * (0.1 / line_seg.len)

        # (p2.y - p1.y) * t --> yDiff * t
        new_query_point.y = query_point.y + y_diff * (0.1 / line_seg.len)

        return new_query_point

    def getQueryResult(self, query_point, line_seg, query_point_existed=False):
        """
        queryPoint: one of the endpoints of lineSegment
        lineSegment: lineSegment currently being inserted
        """
        assert isinstance(query_point, Point)
        assert isinstance(line_seg, LineSegment)
        # print("query point", query_point, "|", self.graphObject)

        # we are an X-Node
        if isinstance(self.graph_object, Point):
            # if the query point is the same as this node
            if query_point.x < self.graph_object.x:
                return self.left_child.getQueryResult(query_point, line_seg, query_point_existed)
            elif query_point.x > self.graph_object.x:
                return self.right_child.getQueryResult(query_point, line_seg, query_point_existed)
            else:
                new_query_point = self.get_offset_point(query_point, line_seg)
                return self.getQueryResult(new_query_point, line_seg, query_point == self.graph_object)

        # we are a Y-Node
        elif isinstance(self.graph_object, LineSegment):
            if self.graph_object.aboveLine(query_point):
                return self.right_child.getQueryResult(query_point, line_seg, query_point_existed)
            else:
                return self.left_child.getQueryResult(query_point, line_seg, query_point_existed)

        # we are a leaf node
        elif isinstance(self.graph_object, Trapezoid.Trapezoid):
            return self, query_point_existed

        # we have no idea what we are doing
        else:
            raise ValueError('invalid DAG node!')

    def modify(self, new_node):
        assert isinstance(new_node, DAGNode)
        self.graph_object = new_node.graph_object
        self.left_child = new_node.left_child
        self.right_child = new_node.right_child

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        # return hash(tuple(sorted(self.__dict__.items())))
        return hash(str(self))

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.graph_object == other.graph_object \
                   and self.left_child is other.left_child \
                   and self.right_child is other.right_child
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self == other
        return NotImplemented

    def __repr__(self):
        return '<Node left_child: %s, right_child: %s, graph_object: %s>' % (
            self.left_child.graph_object if self.left_child else 'NO',
            self.right_child.graph_object if self.right_child else 'NO', self.graph_object)
