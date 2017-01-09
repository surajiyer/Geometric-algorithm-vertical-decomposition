import copy
import math
from Point import Point
from LineSegment import LineSegment
from Trapezoid import Trapezoid
from GraphObject import GraphObject

class DAGNode:
    """
        Class representing a Node in the DAG search structure
    """
    def __init__(self, graphObject):
        assert isinstance(graphObject, GraphObject)
        self.graphObject = graphObject

    def setLeftChild(self, leftChild):
        assert isinstance(leftChild, DAGNode)
        self.leftChild = leftChild

    def setRightChild(self, rightChild):
        assert isinstance(rightChild, DAGNode)
        self.rightChild = rightChild


    def getQueryResult(self, queryPoint, lineSegment, queryPointExisted):
        """
            queryPoint: one of the endpoints of lineSegment
            lineSegment: lineSegment currently being inserted
        """

        assert isinstance(queryPoint, Point)
        assert isinstance(lineSegment, LineSegment)

        # we are an X-Node
        if isinstance(self.graphObject, Point):
            #if the querypoint is the same as this node
            if queryPoint == self.graphObject:       

                #we do not want to change the querypoint itself
                newQueryPoint = copy.deepcopy(queryPoint)
                queryPointExisted = True

                #the querypoint is the left point of the line segment
                if queryPoint == lineSegment.p:
                    xDiff = (lineSegment.q.x - queryPoint.x)
                    yDiff = (lineSegment.q.y - queryPoint.y)
                elif queryPoint == lineSegment.q: #the querypoint is the right point of the line segment
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
                    return self.leftChild.getQueryResult(queryPoint, lineSegment, queryPointExisted)
                elif queryPoint.x > self.graphObject.x:
                    return self.rightChild.getQueryResult(queryPoint, lineSegment, queryPointExisted)
                else:
                    return self.rightChild.getQueryResult(queryPoint, lineSegment, queryPointExisted)
                    #TODO: handle points with same x

        elif isinstance(self.graphObject, LineSegment):
            #we are a Y-Node
            if self.graphObject.aboveLine(queryPoint):
                return self.rightChild.getQueryResult(queryPoint, lineSegment, queryPointExisted)
            else:
                return self.leftChild.getQueryResult(queryPoint, lineSegment, queryPointExisted)
        elif isinstance(self.graphObject, Trapezoid):
            #we are a leaf
            return self, queryPointExisted
        else:
            raise ValueError('invalid DAG node!')