from Polygon import Polygon, Point, LineSegment
from TrapezoidMap import TrapezoidMap, Trapezoid
from DAG import DAG, DAGNode


class RandomizedIncrementalConstruction:
    def __init__(self, polygon):
        assert isinstance(polygon, Polygon)
        self.polygon = polygon
        self.T = TrapezoidMap([])
        self.computeDecomposition()

    def getTrapezoidalMap(self) -> TrapezoidMap:
        return self.T

    def computeDecomposition(self):
        """
        Create a vertical decomposition of a simple polygon
        """
        self.computeBoundingBox()

        # TODO: Add randomization
        for lineSegment in self.polygon.E:
            self.insertLinesegment(lineSegment)

    def insertLinesegment(self, lineSegment):
        # Special case for vertical line segments: just ignore them
        if lineSegment.p.x == lineSegment.q.x:
            return

        # find the trapezoid in which p and q lie
        pNode, pExisted = self.DAG.root.getQueryResult(lineSegment.p, lineSegment, False)
        qNode, qExisted = self.DAG.root.getQueryResult(lineSegment.q, lineSegment, False)

        # p and q lie in the same trapezoid
        if pNode.graphObject == qNode.graphObject:
            containingTrapezoid = pNode.graphObject

            # we always need to split the trapezoid
            newTopTrapezoid = Trapezoid(lineSegment.p, lineSegment.q, containingTrapezoid.top, lineSegment)
            newBottomTrapezoid = Trapezoid(lineSegment.p, lineSegment.q, lineSegment, containingTrapezoid.bottom)

            # make a DAG y-node for these trapezoids with the line segment
            yNode = DAGNode(lineSegment)
            yNode.leftchild = DAGNode(newBottomTrapezoid)
            yNode.rightchild = DAGNode(newTopTrapezoid)

            # the trapezoid will be removed from the trapezoidal map
            self.T.deleteTrapezoidFromMap(containingTrapezoid)

            # and add the new ones
            self.T.addTrapezoid(newTopTrapezoid)
            self.T.addTrapezoid(newBottomTrapezoid)

            # TODO: fix correct neighbor initialization

            # then we might need to make a trapezoid right of q
            if not qExisted:
                if lineSegment.q.x == containingTrapezoid.rightp.x \
                        and any(len(neighbor.leftneighbors) >= 2 for neighbor in containingTrapezoid.rightneighbors):
                    rightTrapezoid = Trapezoid(lineSegment.q,
                                               lineSegment.q,
                                               containingTrapezoid.top,
                                               containingTrapezoid.bottom)
                else:
                    rightTrapezoid = Trapezoid(lineSegment.q,
                                               containingTrapezoid.rightp,
                                               containingTrapezoid.top,
                                               containingTrapezoid.bottom)
                rightTrapezoid.setLeftNeighbors([newBottomTrapezoid, newTopTrapezoid])
                rightTrapezoid.setRightNeighbors(containingTrapezoid.rightneighbors)

                # update right neighbors of containingTrapezoid
                for neighbor in rightTrapezoid.rightneighbors:
                    neighbor.setLeftNeighbors([rightTrapezoid])
                    neighbor.leftneighbors.remove(containingTrapezoid)

                # add the new trapezoid as a neighbor
                for neighbor in rightTrapezoid.leftneighbors:
                    neighbor.setRightNeighbors([rightTrapezoid])

                self.T.addTrapezoid(rightTrapezoid)
                qXnode = DAGNode(lineSegment.q, yNode, DAGNode(rightTrapezoid))

                # change the pNode to the new qXnode
                pNode.modify(qXnode)
            else:
                newBottomTrapezoid.setRightNeighbors(containingTrapezoid.rightneighbors)
                for neighbor in newBottomTrapezoid.rightneighbors:
                    neighbor.setLeftNeighbors([newBottomTrapezoid])
                    neighbor.leftneighbors.remove(containingTrapezoid)

                newTopTrapezoid.setRightNeighbors(containingTrapezoid.rightneighbors)
                for neighbor in newTopTrapezoid.rightneighbors:
                    neighbor.setLeftNeighbors([newTopTrapezoid])
                    neighbor.leftneighbors.remove(containingTrapezoid)

            # then we need to make a trapezoid le ft of p
            if not pExisted:
                # first initialize the new trapezoid
                if lineSegment.p.x == containingTrapezoid.leftp.x \
                        and any(len(neighbor.rightneighbors) >= 2 for neighbor in containingTrapezoid.leftneighbors):
                    leftTrapezoid = Trapezoid(lineSegment.p,
                                              lineSegment.p,
                                              containingTrapezoid.top,
                                              containingTrapezoid.bottom)
                else:
                    leftTrapezoid = Trapezoid(containingTrapezoid.leftp,
                                              lineSegment.p,
                                              containingTrapezoid.top,
                                              containingTrapezoid.bottom)

                leftTrapezoid.setLeftNeighbors(containingTrapezoid.leftneighbors)
                leftTrapezoid.setRightNeighbors([newBottomTrapezoid, newTopTrapezoid])

                # update left neighbors of containingTrapezoid
                for neighbor in leftTrapezoid.leftneighbors:
                    neighbor.setRightNeighbors([leftTrapezoid])
                    neighbor.rightneighbors.remove(containingTrapezoid)

                # add the new trapezoid as a neighbor
                for neighbor in leftTrapezoid.rightneighbors:
                    neighbor.setLeftNeighbors([leftTrapezoid])

                self.T.addTrapezoid(leftTrapezoid)

                pXnode = DAGNode(lineSegment.p,
                                 DAGNode(leftTrapezoid),
                                 qXnode if not qExisted else yNode)
                pNode.modify(pXnode)
            else:
                newBottomTrapezoid.setLeftNeighbors(containingTrapezoid.leftneighbors)
                for neighbor in newBottomTrapezoid.leftneighbors:
                    neighbor.setRightNeighbors([newBottomTrapezoid])
                    neighbor.rightneighbors.remove(containingTrapezoid)

                newTopTrapezoid.setLeftNeighbors(containingTrapezoid.leftneighbors)
                for neighbor in newTopTrapezoid.leftneighbors:
                    neighbor.setRightNeighbors([newTopTrapezoid])
                    neighbor.rightneighbors.remove(containingTrapezoid)

            if qExisted and pExisted:
                pNode.modify(yNode)

        else:
            # the trapezoids will be removed from the trapezoidal map
            print(lineSegment)
            print(pNode)
            print(qNode)
            self.T.deleteTrapezoidFromMap(pNode.graphObject)
            self.T.deleteTrapezoidFromMap(qNode.graphObject)

            # TODO: fix intersecting trapezoids case

    def computeBoundingBox(self):
        # find  top right point to create a bounding box (bottom left is [0, 0])
        topRight = Point(0, 0)
        bottomLeft = Point(float("inf"), float("inf"))

        for point in self.polygon.V:
            # find top right
            if point.get_x() >= topRight.get_x():
                topRight.set_x(point.get_x() + 1)
            if point.get_y() >= topRight.get_y():
                topRight.set_y(point.get_y() + 1)

            # find left bottom
            if point.get_x() <= bottomLeft.get_x():
                bottomLeft.set_x(point.get_x() - 1)
            if point.get_y() <= bottomLeft.get_y():
                bottomLeft.set_y(point.get_y() - 1)

        # Now add the bounding box as a trapezoid
        B = Trapezoid(bottomLeft, topRight,
                      LineSegment(Point(bottomLeft.x, topRight.y), topRight),
                      LineSegment(bottomLeft, Point(topRight.x, bottomLeft.y)))
        self.T.addTrapezoid(B)
        self.DAG = DAG(DAGNode(B))
