from Polygon import Polygon, Point, LineSegment
from TrapezoidMap import TrapezoidMap, Trapezoid
from DAG import DAG, DAGNode


class RandomizedIncrementalConstruction:
    def __init__(self, polygon):
        assert isinstance(polygon, Polygon)
        self.polygon = polygon
        self.computeDecomposition()

    def getTrapezoidalMap(self) -> TrapezoidMap:
        return self.T

    """
    Create a vertical decomposition of a simple polygon
    """

    def computeDecomposition(self):
        self.T = TrapezoidMap([])
        self.computeBoundingBox()

        # TODO: Add randomization
        for lineSegment in self.polygon.E:
            print("Map before next insertion:", self.T)
            self.insertLinesegment(lineSegment)

    def insertLinesegment(self, lineSegment):
        # find the trapezoid in which p and q lie
        pNode, pExisted = self.DAG.root.getQueryResult(lineSegment.p, lineSegment, False)
        qNode, qExisted = self.DAG.root.getQueryResult(lineSegment.q, lineSegment, False)

        print("inserting", lineSegment)
        print("pNode", pNode.graphObject)

        # p and q lie in the same trapezoid
        if pNode.graphObject == qNode.graphObject:
            containingTrapezoid = pNode.graphObject
            # we always need to split the trapezoid
            # TODO: fix correct neighbor initialization
            newTopTrapezoid = Trapezoid(lineSegment.p, lineSegment.q, containingTrapezoid.top, lineSegment, [])
            newBottomTrapezoid = Trapezoid(lineSegment.p, lineSegment.q, lineSegment, containingTrapezoid.bottom, [])

            # make a DAG y-node for these trapezoids with the line segment
            yNode = DAGNode(lineSegment)
            yNode.leftchild = DAGNode(newBottomTrapezoid)
            yNode.rightchild = DAGNode(newTopTrapezoid)

            # the trapezoid will be removed from the trapezoidal map
            print("trying to delete:", containingTrapezoid)
            self.T.deleteTrapezoidFromMap(containingTrapezoid)

            # and add the new ones
            self.T.addTrapezoid(newTopTrapezoid)
            self.T.addTrapezoid(newBottomTrapezoid)

            # then we might need to make a trapezoid right of q
            if not qExisted:
                # TODO: fix neighbors
                rightTrapezoid = Trapezoid(lineSegment.q,
                                           containingTrapezoid.rightp,
                                           containingTrapezoid.top,
                                           containingTrapezoid.bottom, [])
                self.T.addTrapezoid(rightTrapezoid)
                qXnode = DAGNode(lineSegment.q, yNode, DAGNode(rightTrapezoid))

                # change the pNode to the new qXnode
                pNode.modify(qXnode)

            # then we need to make a trapezoid left of p
            if not pExisted:
                # first initialize the new trapezoid
                # TODO: fix neighbors
                leftTrapezoid = Trapezoid(containingTrapezoid.leftp,
                                          lineSegment.p,
                                          containingTrapezoid.top,
                                          containingTrapezoid.bottom, [])
                self.T.addTrapezoid(leftTrapezoid)

                pXnode = DAGNode(lineSegment.p,
                                 DAGNode(leftTrapezoid),
                                 qXnode if not qExisted else yNode)
                pNode.modify(pXnode)

            if qExisted and pExisted:
                pNode.modify(yNode)

            print("root of DAG after update:", pNode)

        else:
            # the trapezoids will be removed from the trapezoidal map
            self.T.deleteTrapezoidFromMap(pNode.graphObject)
            self.T.deleteTrapezoidFromMap(qNode.graphObject)

    def computeBoundingBox(self):
        # find  top right point to create a bounding box (bottom left is [0, 0])
        topRight = Point(0, 0)

        for point in self.polygon.V:
            if point.get_x() >= topRight.get_x():
                topRight.set_x(point.get_x() + 1)
            if point.get_y() >= topRight.get_y():
                topRight.set_y(point.get_y() + 1)

        # Now add the bounding box as a trapezoid
        B = Trapezoid(Point(0, 0), topRight,
                      LineSegment(Point(0, topRight.get_y()), topRight),
                      LineSegment(Point(0, 0), Point(topRight.get_x(), 0)), [])
        self.T.addTrapezoid(B)
        self.DAG = DAG(DAGNode(B))
