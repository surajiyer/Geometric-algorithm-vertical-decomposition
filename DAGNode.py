from Point import Point
from LineSegment import LineSegment
from Trapezoid import Trapezoid

class DAGNode:
    """
        Class representing a Node in the DAG search structure
    """
    def __init__(self, graphObject):
        assert isinstance(graphObject, Point)
        self.graphObject = graphObject

    def setLeftChild(self, leftChild):
        assert isinstance(leftChild, DAGNode)
        self.leftChild = leftChild

    def setRightChild(self, rightChild):
        assert isinstance(rightChild, DAGNode)
        self.rightChild = rightChild

    def getQueryResult(self, queryPoint):
        assert isinstance(queryPoint, Point)
        # we are an X-Node
        if isinstance(self.graphObject, Point):
            # if querypoint lies (completely) left of this point
            if queryPoint.get_x < self.graphObject.get_x:
                return self.leftChild.getQueryResult(queryPoint)
            else:
                return self.rightChild.getQueryResult(queryPoint)
        elif isinstance(self.graphObject, LineSegment):
            #we are a Y-Node
            if self.graphObject.aboveLine(queryPoint):
                return self.rightChild.getQueryResult(queryPoint)
            else:
                return self.leftChild.getQueryResult(queryPoint)
        elif isinstance(self.graphObject, Trapezoid):
            #we are a leaf
            return self.graphObject
