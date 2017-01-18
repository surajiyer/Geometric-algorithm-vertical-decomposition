from Polygon import Polygon, Point, LineSegment
from TrapezoidMap import TrapezoidMap, Trapezoid
from DAG import DAG, DAGNode
from itertools import groupby
import random


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
        random.shuffle(self.polygon.E)
        # self.polygon.E = [self.polygon.E[i] for i in [3, 0, 1, 4, 2]]
        import pprint as pp
        for lineSegment in self.polygon.E:
            self.insertLinesegment(lineSegment)
            # pp.pprint(self.T.G)
            # self.T.visualize_graph()

    def getIntersectingTrapezoids(self, lineSegment):
        """
        Function to get a list of trapezoids intersected by a given a line segment.
        :param lineSegment:
        :return: list of trapezoids
        """
        assert isinstance(lineSegment, LineSegment)
        print('----------------------------------------')
        print("LineSegment |", lineSegment)
        print("Finding p")
        p = self.T.G.root.getQueryResult(lineSegment.p, lineSegment)
        print("Finding q")
        q = self.T.G.root.getQueryResult(lineSegment.q, lineSegment)
        current_trapezoid = p[0].graph_object
        intersecting_trapezoids = [current_trapezoid]

        print('Before Loop')
        while current_trapezoid != q[0].graph_object:
            print('Inside loop')
            for n in current_trapezoid.right_neighbors:
                if current_trapezoid.right_p != n.left_p:
                    l = LineSegment(current_trapezoid.right_p, n.left_p)
                else:
                    if n.left_p == n.bottom.p:
                        l = n.top
                        y = l.slope * n.left_p.x + l.intercept
                        l = LineSegment(n.left_p, Point(n.left_p.x, y))
                    elif n.left_p == n.top.p:
                        l = n.bottom
                        y = l.slope * n.left_p.x + l.intercept
                        l = LineSegment(Point(n.left_p.x, y), n.left_p)
                    else:
                        l = n.bottom
                        by = l.slope * n.left_p.x + l.intercept
                        l = n.top
                        ty = l.slope * n.left_p.x + l.intercept
                        l = LineSegment(Point(n.left_p.x, by), Point(n.left_p.x, ty))

                if l.intersects(lineSegment):
                    intersecting_trapezoids.append(n)
                    current_trapezoid = n
                    break

        return intersecting_trapezoids, p, q

    def insertLinesegment(self, lineSegment):
        assert isinstance(lineSegment, LineSegment)

        # Special case for vertical line segments: just ignore them
        if lineSegment.p.x == lineSegment.q.x:
            return

        # find the trapezoid in which p and q lie
        intersectingTrapezoids, (pNode, pExisted), (qNode, qExisted) = self.getIntersectingTrapezoids(lineSegment)
        pTrapezoid, qTrapezoid = pNode.graph_object, qNode.graph_object

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

            # Update the trapezoidal map
            self.T.deleteTrapezoidFromMap([pTrapezoid])
            self.T.addTrapezoid([newTopTrapezoid, newBottomTrapezoid])

            if not qExisted:
                # then we might need to make a trapezoid right of q
                if lineSegment.q.x == pTrapezoid.right_p.x \
                        and any(len(neighbor.left_neighbors) >= 2 for neighbor in pTrapezoid.right_neighbors):
                    rightTrapezoid = Trapezoid(Point(lineSegment.q.x, pTrapezoid.top.q.y),
                                               Point(lineSegment.q.x, pTrapezoid.bottom.q.y),
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
                    neighbor.left_neighbors.remove(pTrapezoid)

                self.T.addTrapezoid([rightTrapezoid])
                qXnode = DAGNode(lineSegment.q, yNode, rightTrapezoid.node)

                # change the pNode to the new qXnode
                if pExisted:
                    pNode.modify(qXnode)
            else:
                newBottomTrapezoid.setRightNeighbors(pTrapezoid.right_neighbors)
                for neighbor in newBottomTrapezoid.right_neighbors:
                    neighbor.left_neighbors.remove(pTrapezoid)

                newTopTrapezoid.setRightNeighbors(pTrapezoid.right_neighbors)
                for neighbor in newTopTrapezoid.right_neighbors:
                    neighbor.left_neighbors.remove(pTrapezoid)

            # then we need to make a trapezoid left of p
            if not pExisted:
                # first initialize the new trapezoid
                if lineSegment.p.x == pTrapezoid.left_p.x \
                        and any(len(neighbor.right_neighbors) >= 2 for neighbor in pTrapezoid.left_neighbors):
                    leftTrapezoid = Trapezoid(Point(lineSegment.p.x, pTrapezoid.top.p.y),
                                              Point(lineSegment.p.x, pTrapezoid.bottom.p.y),
                                              pTrapezoid.top,
                                              pTrapezoid.bottom)
                else:
                    leftTrapezoid = Trapezoid(pTrapezoid.left_p,
                                              lineSegment.p,
                                              pTrapezoid.top,
                                              pTrapezoid.bottom)
                leftTrapezoid.setLeftNeighbors(pTrapezoid.left_neighbors)
                leftTrapezoid.setRightNeighbors([newBottomTrapezoid, newTopTrapezoid])

                # update left neighbors of pTrapezoid
                for neighbor in leftTrapezoid.left_neighbors:
                    neighbor.right_neighbors.remove(pTrapezoid)

                self.T.addTrapezoid([leftTrapezoid])

                pXnode = DAGNode(lineSegment.p,
                                 leftTrapezoid.node,
                                 qXnode if not qExisted else yNode)
                pNode.modify(pXnode)
            else:
                newBottomTrapezoid.setLeftNeighbors(pTrapezoid.left_neighbors)
                for neighbor in newBottomTrapezoid.left_neighbors:
                    neighbor.right_neighbors.remove(pTrapezoid)

                newTopTrapezoid.setLeftNeighbors(pTrapezoid.left_neighbors)
                for neighbor in newTopTrapezoid.left_neighbors:
                    neighbor.right_neighbors.remove(pTrapezoid)

            if qExisted and pExisted:
                pNode.modify(yNode)

        elif len(intersectingTrapezoids) > 1:
            """ https://isotropic.org/papers/point-location.pdf """
            # Handle the trapezoid containing lineSegment.p
            # TODO: handle pexisted and qexisted case
            newLeftBottomTrapezoid = Trapezoid(lineSegment.p, lineSegment.get_Y(pTrapezoid.right_p.x),
                                               lineSegment, pTrapezoid.bottom)
            newLeftTopTrapezoid = Trapezoid(lineSegment.p, lineSegment.get_Y(pTrapezoid.right_p.x),
                                            pTrapezoid.top, lineSegment)
            if not pExisted:
                newLeftTrapezoid = Trapezoid(pTrapezoid.left_p, lineSegment.p, pTrapezoid.top,
                                             pTrapezoid.bottom)
                newLeftTrapezoid.setLeftNeighbors(pTrapezoid.left_neighbors)
                newLeftTrapezoid.setRightNeighbors([newLeftTopTrapezoid, newLeftBottomTrapezoid])
            else:
                newLeftTopTrapezoid.setLeftNeighbors(pTrapezoid.left_neighbors)
                newLeftBottomTrapezoid.setLeftNeighbors(pTrapezoid.left_neighbors)

            # Handle the trapezoid containing lineSegment.q
            newRightBottomTrapezoid = Trapezoid(lineSegment.get_Y(qTrapezoid.left_p.x), lineSegment.q,
                                                lineSegment, qTrapezoid.bottom)
            newRightTopTrapezoid = Trapezoid(lineSegment.get_Y(qTrapezoid.left_p.x), lineSegment.q,
                                             qTrapezoid.top, lineSegment)
            if not qExisted:
                newRightTrapezoid = Trapezoid(lineSegment.q, qTrapezoid.right_p, qTrapezoid.top,
                                              qTrapezoid.bottom)
                newRightTrapezoid.setLeftNeighbors([newRightTopTrapezoid, newRightBottomTrapezoid])
                newRightTrapezoid.setRightNeighbors(qTrapezoid.right_neighbors)
            else:
                newRightTopTrapezoid.setRightNeighbors(qTrapezoid.right_neighbors)
                newRightBottomTrapezoid.setRightNeighbors(qTrapezoid.right_neighbors)

            # TODO: fix removal of old neighbors
            # Walk to the right along the new segment and split
            # each trapezoid into upper and lower ones
            newTopTrapezoids, newBottomTrapezoids = [newLeftTopTrapezoid], [newLeftBottomTrapezoid]
            for t in intersectingTrapezoids[1:-1]:
                new_top = Trapezoid(lineSegment.get_Y(t.left_p.x), lineSegment.get_Y(t.right_p.x),
                                    t.top, lineSegment)
                new_bottom = Trapezoid(lineSegment.get_Y(t.left_p.x), lineSegment.get_Y(t.right_p.x),
                                       lineSegment, t.bottom)
                for n in t.left_neighbors:
                    if lineSegment.aboveLine(n.bottom.q):
                        new_top.setLeftNeighbors([n])
                    if not lineSegment.aboveLine(n.top.q):
                        new_bottom.setLeftNeighbors([n])
                new_top.setLeftNeighbors([newTopTrapezoids[-1]])
                new_bottom.setLeftNeighbors([newBottomTrapezoids[-1]])
                newTopTrapezoids.append(new_top)
                newBottomTrapezoids.append(new_bottom)
            newRightTopTrapezoid.setLeftNeighbors([newTopTrapezoids[-1]])
            newRightBottomTrapezoid.setLeftNeighbors([newBottomTrapezoids[-1]])
            newTopTrapezoids.append(newRightTopTrapezoid)
            newBottomTrapezoids.append(newRightBottomTrapezoid)

            # Merge trapezoids with the same top and bottom line segments
            newTopTrapezoidsTemp, newBottomTrapezoidsTemp = [], []
            for k, g in groupby(newTopTrapezoids, lambda x: x.top):
                g = list(g)
                if len(g) > 1:
                    t = Trapezoid(g[0].left_p, g[-1].right_p, k, g[0].bottom)
                    t.setLeftNeighbors(g[0].left_neighbors)
                    t.setRightNeighbors(g[-1].right_neighbors)
                    newTopTrapezoidsTemp.append((k, t))
                else:
                    newTopTrapezoidsTemp.append((k, g[0]))
            for k, g in groupby(newBottomTrapezoids, lambda x: x.bottom):
                g = list(g)
                if len(g) > 1:
                    t = Trapezoid(g[0].left_p, g[-1].right_p, g[0].top, k)
                    t.setLeftNeighbors(g[0].left_neighbors)
                    t.setRightNeighbors(g[-1].right_neighbors)
                    newBottomTrapezoidsTemp.append((k, t))
                else:
                    newBottomTrapezoidsTemp.append((k, g[0]))
            newTopTrapezoids, newBottomTrapezoids = newTopTrapezoidsTemp, newBottomTrapezoidsTemp

            # Updating the DAG and the Trapezoidal map
            newTopTrapezoids = dict(newTopTrapezoids)
            newBottomTrapezoids = dict(newBottomTrapezoids)
            if not pExisted:
                pTrapezoid.node = DAGNode(lineSegment.p,
                                          left_child=newLeftTrapezoid.node,
                                          right_child=DAGNode(lineSegment, newBottomTrapezoids[pTrapezoid.bottom].node,
                                                              newTopTrapezoids[pTrapezoid.top].node))
                self.T.deleteTrapezoidFromMap([pTrapezoid])
            if not qExisted:
                qTrapezoid.node = DAGNode(lineSegment.q,
                                          left_child=DAGNode(lineSegment, newBottomTrapezoids[qTrapezoid.bottom].node,
                                                             newTopTrapezoids[qTrapezoid.top].node),
                                          right_child=newRightTrapezoid.node)
                self.T.deleteTrapezoidFromMap([qTrapezoid])
            for t in intersectingTrapezoids[0 if pExisted else 1: len(intersectingTrapezoids) if qExisted else -1]:
                t.node = DAGNode(lineSegment, left_child=newBottomTrapezoids[t.bottom].node,
                                 right_child=newTopTrapezoids[t.top].node)
            self.T.deleteTrapezoidFromMap(intersectingTrapezoids)
            self.T.addTrapezoid([k[1] for k in newTopTrapezoidsTemp + newBottomTrapezoidsTemp])

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
        self.T.G = DAG(DAGNode(B))
