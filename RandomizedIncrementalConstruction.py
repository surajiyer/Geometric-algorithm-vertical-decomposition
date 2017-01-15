from Polygon import Polygon, Point, LineSegment
from TrapezoidMap import TrapezoidMap, Trapezoid
from DAG import DAG, DAGNode
from itertools import groupby


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

    def getIntersectingTrapezoids(self, lineSegment):
        pNode = self.DAG.root.getQueryResult(lineSegment.p, lineSegment)
        qNode = self.DAG.root.getQueryResult(lineSegment.q, lineSegment)
        currentTrapezoid = pNode.graphObject
        intersectingTraps = [currentTrapezoid]

        while currentTrapezoid != qNode.graphObject:
            for n in currentTrapezoid.rightneighbors:
                if currentTrapezoid.rightp != n.leftp:
                    l = LineSegment(currentTrapezoid.rightp, n.leftp)
                else:
                    if n.leftp == n.bottom.p:
                        l = n.top
                        y = l.getSlope() * n.leftp.x + l.getIntercept()
                        l = LineSegment(n.leftp, Point(n.leftp.x, y))
                    elif n.leftp == n.top.p:
                        l = n.bottom
                        y = l.getSlope() * n.leftp.x + l.getIntercept()
                        l = LineSegment(Point(n.leftp.x, y), n.leftp)
                    else:
                        l = n.bottom
                        by = l.getSlope() * n.leftp.x + l.getIntercept()
                        l = n.top
                        ty = l.getSlope() * n.leftp.x + l.getIntercept()
                        l = LineSegment(Point(n.leftp.x, by), Point(n.leftp.x, ty))

                        # elif currentTrapezoid.rightp == currentTrapezoid.top.q:
                        #     l = n.bottom
                        #     y = l.getSlope() * n.leftp.x + l.getIntercept()
                        #     l = LineSegment(Point(n.bottom.p.x, y), n.leftp)

                if l.intersects(lineSegment):
                    intersectingTraps.append(currentTrapezoid)
                    currentTrapezoid = n
                    break

        return intersectingTraps

    def insertLinesegment(self, lineSegment):
        # Special case for vertical line segments: just ignore them
        if lineSegment.p.x == lineSegment.q.x:
            return

        # find the trapezoid in which p and q lie
        pNode, pExisted = self.DAG.root.getQueryResult(lineSegment.p, lineSegment)
        qNode, qExisted = self.DAG.root.getQueryResult(lineSegment.q, lineSegment)
        intersectingTrapezoids = self.getIntersectingTrapezoids(lineSegment)
        pTrapezoid, qTrapezoid = pNode.graphObject, qNode.graphObject

        # p and q lie in the same trapezoid
        # if pTrapezoid == qTrapezoid:
        if len(intersectingTrapezoids) == 1:
            # we always need to split the trapezoid
            newTopTrapezoid = Trapezoid(lineSegment.p, lineSegment.q, pTrapezoid.top, lineSegment)
            newTopTrapezoid.node = DAGNode(newTopTrapezoid)
            newBottomTrapezoid = Trapezoid(lineSegment.p, lineSegment.q, lineSegment, pTrapezoid.bottom)
            newBottomTrapezoid.node = DAGNode(newBottomTrapezoid)

            # make a DAG y-node for these trapezoids with the line segment
            yNode = DAGNode(lineSegment)
            yNode.left_child = newBottomTrapezoid.node
            yNode.right_child = newTopTrapezoid.node

            # the trapezoid will be removed from the trapezoidal map
            self.T.deleteTrapezoidFromMap(pTrapezoid)

            # and add the new ones
            self.T.addTrapezoid(newTopTrapezoid)
            self.T.addTrapezoid(newBottomTrapezoid)

            # TODO: fix correct neighbor initialization

            # then we might need to make a trapezoid right of q
            if not qExisted:
                if lineSegment.q.x == pTrapezoid.rightp.x \
                        and any(len(neighbor.leftneighbors) >= 2 for neighbor in pTrapezoid.rightneighbors):
                    rightTrapezoid = Trapezoid(lineSegment.q,
                                               lineSegment.q,
                                               pTrapezoid.top,
                                               pTrapezoid.bottom)
                else:
                    rightTrapezoid = Trapezoid(lineSegment.q,
                                               pTrapezoid.rightp,
                                               pTrapezoid.top,
                                               pTrapezoid.bottom)

                rightTrapezoid.node = DAGNode(rightTrapezoid)
                rightTrapezoid.setLeftNeighbors([newBottomTrapezoid, newTopTrapezoid])
                rightTrapezoid.setRightNeighbors(pTrapezoid.rightneighbors)

                # update right neighbors of containingTrapezoid
                for neighbor in rightTrapezoid.rightneighbors:
                    neighbor.setLeftNeighbors([rightTrapezoid])
                    neighbor.leftneighbors.remove(pTrapezoid)

                # add the new trapezoid as a neighbor
                for neighbor in rightTrapezoid.leftneighbors:
                    neighbor.setRightNeighbors([rightTrapezoid])

                self.T.addTrapezoid(rightTrapezoid)
                qXnode = DAGNode(lineSegment.q, yNode, rightTrapezoid.node)

                # change the pNode to the new qXnode
                pNode.modify(qXnode)
            else:
                newBottomTrapezoid.setRightNeighbors(pTrapezoid.rightneighbors)
                for neighbor in newBottomTrapezoid.rightneighbors:
                    neighbor.setLeftNeighbors([newBottomTrapezoid])
                    neighbor.leftneighbors.remove(pTrapezoid)

                newTopTrapezoid.setRightNeighbors(pTrapezoid.rightneighbors)
                for neighbor in newTopTrapezoid.rightneighbors:
                    neighbor.setLeftNeighbors([newTopTrapezoid])
                    neighbor.leftneighbors.remove(pTrapezoid)

            # then we need to make a trapezoid le ft of p
            if not pExisted:
                # first initialize the new trapezoid
                if lineSegment.p.x == pTrapezoid.leftp.x \
                        and any(len(neighbor.rightneighbors) >= 2 for neighbor in pTrapezoid.leftneighbors):
                    leftTrapezoid = Trapezoid(lineSegment.p,
                                              lineSegment.p,
                                              pTrapezoid.top,
                                              pTrapezoid.bottom)
                else:
                    leftTrapezoid = Trapezoid(pTrapezoid.leftp,
                                              lineSegment.p,
                                              pTrapezoid.top,
                                              pTrapezoid.bottom)

                leftTrapezoid.node = DAGNode(leftTrapezoid)
                leftTrapezoid.setLeftNeighbors(pTrapezoid.leftneighbors)
                leftTrapezoid.setRightNeighbors([newBottomTrapezoid, newTopTrapezoid])

                # update left neighbors of containingTrapezoid
                for neighbor in leftTrapezoid.leftneighbors:
                    neighbor.setRightNeighbors([leftTrapezoid])
                    neighbor.rightneighbors.remove(pTrapezoid)

                # add the new trapezoid as a neighbor
                for neighbor in leftTrapezoid.rightneighbors:
                    neighbor.setLeftNeighbors([leftTrapezoid])

                self.T.addTrapezoid(leftTrapezoid)

                pXnode = DAGNode(lineSegment.p,
                                 leftTrapezoid.node,
                                 qXnode if not qExisted else yNode)
                pNode.modify(pXnode)
            else:
                newBottomTrapezoid.setLeftNeighbors(pTrapezoid.leftneighbors)
                for neighbor in newBottomTrapezoid.leftneighbors:
                    neighbor.setRightNeighbors([newBottomTrapezoid])
                    neighbor.rightneighbors.remove(pTrapezoid)

                newTopTrapezoid.setLeftNeighbors(pTrapezoid.leftneighbors)
                for neighbor in newTopTrapezoid.leftneighbors:
                    neighbor.setRightNeighbors([newTopTrapezoid])
                    neighbor.rightneighbors.remove(pTrapezoid)

            if qExisted and pExisted:
                pNode.modify(yNode)

        elif len(intersectingTrapezoids) > 1:
            """ https://isotropic.org/papers/point-location.pdf """
            # Handle the trapezoid containing lineSegment.p
            newLeftTrapezoid = Trapezoid(pTrapezoid.leftp, lineSegment.p, pTrapezoid.top,
                                         pTrapezoid.bottom)
            newLeftTrapezoid.node = DAGNode(newLeftTrapezoid)
            newLeftBottomTrapezoid = Trapezoid(lineSegment.p, lineSegment.getY(pTrapezoid.rightp.x),
                                               lineSegment, pTrapezoid.bottom)
            newLeftBottomTrapezoid.node = DAGNode(newLeftBottomTrapezoid)
            newLeftTopTrapezoid = Trapezoid(lineSegment.p, lineSegment.getY(pTrapezoid.rightp.x),
                                            pTrapezoid.top, lineSegment)
            newLeftTopTrapezoid.node = DAGNode(newLeftTopTrapezoid)

            # Handle the trapezoid containing lineSegment.q
            newRightTrapezoid = Trapezoid(lineSegment.q, pTrapezoid.rightp, pTrapezoid.top,
                                          pTrapezoid.bottom)
            newRightTrapezoid.node = DAGNode(newRightTrapezoid)
            newRightBottomTrapezoid = Trapezoid(lineSegment.getY(pTrapezoid.leftp.x), lineSegment.q,
                                                lineSegment, pTrapezoid.bottom)
            newRightBottomTrapezoid.node = DAGNode(newRightBottomTrapezoid)
            newRightTopTrapezoid = Trapezoid(lineSegment.getY(pTrapezoid.leftp.x), lineSegment.q,
                                             pTrapezoid.top, lineSegment)
            newRightTopTrapezoid.node = DAGNode(newRightTopTrapezoid)

            # Walk to the right along the new segment and split
            # each trapezoid into upper and lower ones
            newTopTrapezoids, newBottomTrapezoids = [newLeftTopTrapezoid], [newLeftBottomTrapezoid]
            for t in intersectingTrapezoids[1:-1]:
                new_top = Trapezoid(lineSegment.getY(t.leftp.x), lineSegment.getY(t.rightp.x),
                                    t.top, lineSegment)
                new_bottom = Trapezoid(lineSegment.getY(t.leftp.x), lineSegment.getY(t.rightp.x),
                                       lineSegment, t.bottom)
                newTopTrapezoids.append(new_top)
                newBottomTrapezoids.append(new_bottom)
            newTopTrapezoids.append(newRightTopTrapezoid)
            newBottomTrapezoids.append(newRightBottomTrapezoid)

            # Merge trapezoids with the same top and bottom line segments
            newTopTrapezoids = [(k, Trapezoid(g[0].leftp, g[-1].rightp, k, g[0].bottom)
                                 for k, g in groupby(newTopTrapezoids, lambda x: x.top))]
            newBottomTrapezoids = [(k, Trapezoid(g[0].leftp, g[-1].rightp, g[0].top, k)
                                    for k, g in groupby(newBottomTrapezoids, lambda x: x.bottom))]
            for (k, t) in newTopTrapezoids + newBottomTrapezoids:
                t.node = DAGNode(t)

            # Handling neighbor calculation
            # TODO: fix the neighbors of the new trapezoids
            newLeftTrapezoid.setLeftNeighbors(pTrapezoid.leftneighbors)
            newLeftTrapezoid.setRightNeighbors([newLeftBottomTrapezoid, newLeftTopTrapezoid])
            newLeftBottomTrapezoid.setLeftNeighbors([newLeftTrapezoid])
            newLeftBottomTrapezoid.setRightNeighbors(list(trapezoids[0]))
            newLeftTopTrapezoid.setLeftNeighbors([newLeftTrapezoid])
            newLeftTopTrapezoid.setRightNeighbors(list(trapezoids[0]))

            newRightTrapezoid.setLeftNeighbors([newRightBottomTrapezoid, newRightTopTrapezoid])
            newRightTrapezoid.setRightNeighbors(pTrapezoid.rightneighbors)
            newRightBottomTrapezoid.setLeftNeighbors(list(trapezoids[-1]))
            newRightBottomTrapezoid.setRightNeighbors([newRightTrapezoid])
            newRightTopTrapezoid.setLeftNeighbors(list(trapezoids[-1]))
            newRightTopTrapezoid.setRightNeighbors([newRightTrapezoid])

            # Update the DAG
            pTrapezoid.node = DAGNode(lineSegment.p, left_child=newLeftTrapezoid.node,
                                      right_child=DAGNode(lineSegment))
            qTrapezoid.node = DAGNode(lineSegment.q, left_child=DAGNode(lineSegment),
                                      right_child=newRightTrapezoid.node)

            newTopTrapezoids = dict(newTopTrapezoids)
            newBottomTrapezoids = dict(newBottomTrapezoids)
            for t in intersectingTrapezoids[1:-1]:
                t.node = DAGNode(lineSegment, left_child=newBottomTrapezoids[t.bottom].node,
                                 right_child=newTopTrapezoids[t.top].node)

            # the trapezoids will be removed from the trapezoidal map
            # TODO: delete intersecting trapezoids from map + add new ones to map

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
