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
        for lineSegment in self.polygon.E:
            self.insertLinesegment(lineSegment)

    def getIntersectingTrapezoids(self, lineSegment):
        """
        Function to get a list of trapezoids intersected by a given a line segment.
        :param lineSegment:
        :return: list of trapezoids
        """
        assert isinstance(lineSegment, LineSegment)

        pNode, pExisted = self.DAG.root.getQueryResult(lineSegment.p, lineSegment)
        qNode, qExisted = self.DAG.root.getQueryResult(lineSegment.q, lineSegment)
        current_trapezoid = pNode.graphObject
        intersecting_trapezoids = [current_trapezoid]

        while current_trapezoid != qNode.graphObject:
            for n in current_trapezoid.right_neighbors:
                if current_trapezoid.right_p != n.left_p:
                    l = LineSegment(current_trapezoid.right_p, n.left_p)
                else:
                    if n.left_p == n.bottom.p:
                        l = n.top
                        y = l.getSlope() * n.left_p.x + l.getIntercept()
                        l = LineSegment(n.left_p, Point(n.left_p.x, y))
                    elif n.left_p == n.top.p:
                        l = n.bottom
                        y = l.getSlope() * n.left_p.x + l.getIntercept()
                        l = LineSegment(Point(n.left_p.x, y), n.left_p)
                    else:
                        l = n.bottom
                        by = l.getSlope() * n.left_p.x + l.getIntercept()
                        l = n.top
                        ty = l.getSlope() * n.left_p.x + l.getIntercept()
                        l = LineSegment(Point(n.left_p.x, by), Point(n.left_p.x, ty))

                        # elif currentTrapezoid.right_p == currentTrapezoid.top.q:
                        #     l = n.bottom
                        #     y = l.getSlope() * n.left_p.x + l.getIntercept()
                        #     l = LineSegment(Point(n.bottom.p.x, y), n.left_p)

                if l.intersects(lineSegment):
                    intersecting_trapezoids.append(current_trapezoid)
                    current_trapezoid = n
                    break

        return intersecting_trapezoids

    def insertLinesegment(self, lineSegment):
        assert isinstance(lineSegment, LineSegment)

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
            newBottomTrapezoid = Trapezoid(lineSegment.p, lineSegment.q, lineSegment, pTrapezoid.bottom)

            # make a DAG y-node for these trapezoids with the line segment
            yNode = DAGNode(lineSegment)
            yNode.left_child = newBottomTrapezoid.node
            yNode.right_child = newTopTrapezoid.node

            # the trapezoid will be removed from the trapezoidal map
            self.T.deleteTrapezoidFromMap([pTrapezoid])

            # and add the new ones
            self.T.addTrapezoid([newTopTrapezoid, newBottomTrapezoid])

            if not qExisted:
                # then we might need to make a trapezoid right of q
                if lineSegment.q.x == pTrapezoid.right_p.x \
                        and any(len(neighbor.left_neighbors) >= 2 for neighbor in pTrapezoid.right_neighbors):
                    rightTrapezoid = Trapezoid(lineSegment.q,
                                               lineSegment.q,
                                               pTrapezoid.top,
                                               pTrapezoid.bottom)
                else:
                    rightTrapezoid = Trapezoid(lineSegment.q,
                                               pTrapezoid.right_p,
                                               pTrapezoid.top,
                                               pTrapezoid.bottom)
                rightTrapezoid.setLeftNeighbors([newBottomTrapezoid, newTopTrapezoid])
                rightTrapezoid.setRightNeighbors(pTrapezoid.right_neighbors)

                # update right neighbors of containingTrapezoid
                for neighbor in rightTrapezoid.right_neighbors:
                    neighbor.setLeftNeighbors([rightTrapezoid])
                    neighbor.left_neighbors.remove(pTrapezoid)

                # add the new trapezoid as a neighbor
                for neighbor in rightTrapezoid.left_neighbors:
                    neighbor.setRightNeighbors([rightTrapezoid])

                self.T.addTrapezoid([rightTrapezoid])
                qXnode = DAGNode(lineSegment.q, yNode, rightTrapezoid.node)

                # change the pNode to the new qXnode
                pNode.modify(qXnode)
            else:
                newBottomTrapezoid.setRightNeighbors(pTrapezoid.right_neighbors)
                for neighbor in newBottomTrapezoid.right_neighbors:
                    neighbor.setleft_neighbors([newBottomTrapezoid])
                    neighbor.left_neighbors.remove(pTrapezoid)

                newTopTrapezoid.setRightNeighbors(pTrapezoid.right_neighbors)
                for neighbor in newTopTrapezoid.right_neighbors:
                    neighbor.setleft_neighbors([newTopTrapezoid])
                    neighbor.left_neighbors.remove(pTrapezoid)

            # then we need to make a trapezoid le ft of p
            if not pExisted:
                # first initialize the new trapezoid
                if lineSegment.p.x == pTrapezoid.left_p.x \
                        and any(len(neighbor.right_neighbors) >= 2 for neighbor in pTrapezoid.left_neighbors):
                    leftTrapezoid = Trapezoid(lineSegment.p,
                                              lineSegment.p,
                                              pTrapezoid.top,
                                              pTrapezoid.bottom)
                else:
                    leftTrapezoid = Trapezoid(pTrapezoid.left_p,
                                              lineSegment.p,
                                              pTrapezoid.top,
                                              pTrapezoid.bottom)
                leftTrapezoid.setLeftNeighbors(pTrapezoid.left_neighbors)
                leftTrapezoid.setRightNeighbors([newBottomTrapezoid, newTopTrapezoid])

                # update left neighbors of containingTrapezoid
                for neighbor in leftTrapezoid.left_neighbors:
                    neighbor.setRightNeighbors([leftTrapezoid])
                    neighbor.right_neighbors.remove(pTrapezoid)

                # add the new trapezoid as a neighbor
                for neighbor in leftTrapezoid.right_neighbors:
                    neighbor.setLeftNeighbors([leftTrapezoid])

                self.T.addTrapezoid([leftTrapezoid])

                pXnode = DAGNode(lineSegment.p,
                                 leftTrapezoid.node,
                                 qXnode if not qExisted else yNode)
                pNode.modify(pXnode)
            else:
                newBottomTrapezoid.setLeftNeighbors(pTrapezoid.left_neighbors)
                for neighbor in newBottomTrapezoid.left_neighbors:
                    neighbor.setRightNeighbors([newBottomTrapezoid])
                    neighbor.right_neighbors.remove(pTrapezoid)

                newTopTrapezoid.setLeftNeighbors(pTrapezoid.left_neighbors)
                for neighbor in newTopTrapezoid.left_neighbors:
                    neighbor.setRightNeighbors([newTopTrapezoid])
                    neighbor.right_neighbors.remove(pTrapezoid)

            if qExisted and pExisted:
                pNode.modify(yNode)

        elif len(intersectingTrapezoids) > 1:
            """ https://isotropic.org/papers/point-location.pdf """
            # Handle the trapezoid containing lineSegment.p
            newLeftTrapezoid = Trapezoid(pTrapezoid.left_p, lineSegment.p, pTrapezoid.top,
                                         pTrapezoid.bottom)
            newLeftBottomTrapezoid = Trapezoid(lineSegment.p, lineSegment.getY(pTrapezoid.right_p.x),
                                               lineSegment, pTrapezoid.bottom)
            newLeftTopTrapezoid = Trapezoid(lineSegment.p, lineSegment.getY(pTrapezoid.right_p.x),
                                            pTrapezoid.top, lineSegment)

            # Handle the trapezoid containing lineSegment.q
            newRightTrapezoid = Trapezoid(lineSegment.q, pTrapezoid.right_p, pTrapezoid.top,
                                          pTrapezoid.bottom)
            newRightBottomTrapezoid = Trapezoid(lineSegment.getY(pTrapezoid.left_p.x), lineSegment.q,
                                                lineSegment, pTrapezoid.bottom)
            newRightTopTrapezoid = Trapezoid(lineSegment.getY(pTrapezoid.left_p.x), lineSegment.q,
                                             pTrapezoid.top, lineSegment)

            # Walk to the right along the new segment and split
            # each trapezoid into upper and lower ones
            newTopTrapezoids, newBottomTrapezoids = [newLeftTopTrapezoid], [newLeftBottomTrapezoid]
            for t in intersectingTrapezoids[1:-1]:
                new_top = Trapezoid(lineSegment.getY(t.left_p.x), lineSegment.getY(t.right_p.x),
                                    t.top, lineSegment)
                new_bottom = Trapezoid(lineSegment.getY(t.left_p.x), lineSegment.getY(t.right_p.x),
                                       lineSegment, t.bottom)
                for n in t.left_neighbors:
                    if lineSegment.aboveLine(n.bottom.q):
                        new_top.setLeftNeighbors([n])
                        n.setRightNeighbors([new_top])
                    if not lineSegment.aboveLine(n.top.q):
                        new_bottom.setLeftNeighbors([n])
                        n.setRightNeighbors([new_bottom])
                new_top.setLeftNeighbors([newTopTrapezoids[-1]])
                newTopTrapezoids[-1].setRightNeighbors([new_top])
                new_bottom.setLeftNeighbors([newBottomTrapezoids[-1]])
                newBottomTrapezoids[-1].setRightNeighbors([new_bottom])
                newTopTrapezoids.append(new_top)
                newBottomTrapezoids.append(new_bottom)
            newTopTrapezoids.append(newRightTopTrapezoid)
            newBottomTrapezoids.append(newRightBottomTrapezoid)

            # Merge trapezoids with the same top and bottom line segments
            newTopTrapezoidsTemp, newBottomTrapezoidsTemp = [], []
            for k, g in groupby(newTopTrapezoids, lambda x: x.top):
                t = Trapezoid(g[0].left_p, g[-1].right_p, k, g[0].bottom)
                t.setLeftNeighbors(g[0].left_neighbors)
                t.setRightNeighbors(g[-1].right_neighbors)
                newTopTrapezoidsTemp.append((k, t))
            for k, g in groupby(newBottomTrapezoids, lambda x: x.bottom):
                t = Trapezoid(g[0].left_p, g[-1].right_p, g[0].top, k)
                t.setLeftNeighbors(g[0].left_neighbors)
                t.setRightNeighbors(g[-1].right_neighbors)
                newBottomTrapezoidsTemp.append((k, t))
            newTopTrapezoids, newBottomTrapezoids = newTopTrapezoidsTemp, newBottomTrapezoidsTemp

            # newTopTrapezoids = [(k, Trapezoid(g[0].left_p, g[-1].right_p, k, g[0].bottom))
            #                     for k, g in groupby(newTopTrapezoids, lambda x: x.top)]
            # newBottomTrapezoids = [(k, Trapezoid(g[0].left_p, g[-1].right_p, g[0].top, k))
            #                        for k, g in groupby(newBottomTrapezoids, lambda x: x.bottom)]

            # Calculating neighbors
            # newLeftTrapezoid.setLeftNeighbors(pTrapezoid.left_neighbors)
            # newLeftTrapezoid.setRightNeighbors([newLeftBottomTrapezoid, newLeftTopTrapezoid])
            # newRightTrapezoid.setLeftNeighbors([newRightBottomTrapezoid, newRightTopTrapezoid])
            # newRightTrapezoid.setRightNeighbors(pTrapezoid.right_neighbors)
            # for i in range(len(newBottomTrapezoids)):
            #     if i == 0:
            #         newBottomTrapezoids[i][1].setLeftNeighbors([newLeftTrapezoid])
            #     elif i == len(newBottomTrapezoids) - 1:
            #         newBottomTrapezoids[i][1].setRightNeighbors([newRightTrapezoid])
            #     else:
            #         newBottomTrapezoids[i][1].setLeftNeighbors()

            # newLeftBottomTrapezoid.setLeftNeighbors([newLeftTrapezoid])
            # newLeftBottomTrapezoid.setRightNeighbors(newTopTrapezoids[0])
            # newLeftTopTrapezoid.setLeftNeighbors([newLeftTrapezoid])
            # newLeftTopTrapezoid.setRightNeighbors(list(trapezoids[0]))

            # newRightBottomTrapezoid.setLeftNeighbors(list(trapezoids[-1]))
            # newRightBottomTrapezoid.setRightNeighbors([newRightTrapezoid])
            # newRightTopTrapezoid.setLeftNeighbors(list(trapezoids[-1]))
            # newRightTopTrapezoid.setRightNeighbors([newRightTrapezoid])

            # Updating the DAG
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
            self.T.deleteTrapezoidFromMap(intersectingTrapezoids)
            self.T.addTrapezoid([k[1] for k in newTopTrapezoidsTemp+newBottomTrapezoidsTemp])

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
        self.T.addTrapezoid([B])
        self.DAG = DAG(DAGNode(B))
