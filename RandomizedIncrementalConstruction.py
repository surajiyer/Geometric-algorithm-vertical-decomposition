from Polygon import Polygon, Point, LineSegment
from TrapezoidMap import TrapezoidMap, Trapezoid
from DAG import DAG, DAGNode
from itertools import groupby
import random


class RandomizedIncrementalConstruction:
    def __init__(self, polygon):
        assert isinstance(polygon, Polygon)
        self.polygon = polygon
        self.T = TrapezoidMap(set())
        self.computeDecomposition()

    def getTrapezoidalMap(self) -> TrapezoidMap:
        return self.T

    def computeDecomposition(self):
        """
        Create a vertical decomposition of a simple polygon
        """
        self.computeBoundingBox()
        # self.polygon.E = [self.polygon.E[i] for i in [1, 7, 3, 5]] \
        #                  + [self.polygon.E[i] for i in range(len(self.polygon.E)) if i not in [1, 7, 3, 5]]
        random.shuffle(self.polygon.E)
        for lineSegment in self.polygon.E:
            self.insertLinesegment(lineSegment)
            # self.T.visualize()
            # self.T.visualize_graph()

    def getIntersectingTrapezoids(self, line_seg):
        """
        Function to get a list of trapezoids intersected by a given a line segment.
        :param line_seg:
        :return: list of trapezoids
        """
        assert isinstance(line_seg, LineSegment)
        p = self.T.G.root.getQueryResult(line_seg.p, line_seg)
        q = self.T.G.root.getQueryResult(line_seg.q, line_seg)
        current_trapezoid = p[0].graph_object
        intersecting_trapezoids = [current_trapezoid]
        print('Line Segment |', line_seg)

        while current_trapezoid != q[0].graph_object:
            # print('Inside loop')
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
                        bottom_y = l.slope * n.left_p.x + l.intercept
                        l = n.top
                        top_y = l.slope * n.left_p.x + l.intercept
                        l = LineSegment(Point(n.left_p.x, bottom_y), Point(n.left_p.x, top_y))

                if l.intersects(line_seg):
                    intersecting_trapezoids.append(n)
                    current_trapezoid = n
                    break

        return intersecting_trapezoids, p, q

    def insertLinesegment(self, line_seg):
        assert isinstance(line_seg, LineSegment)

        # Special case for vertical line segments: just ignore them
        if line_seg.isVertical:
            return

        # find the trapezoid in which p and q lie
        intersectingTrapezoids, (pNode, p_exists), (qNode, q_exists) = self.getIntersectingTrapezoids(line_seg)
        pTrapezoid, qTrapezoid = pNode.graph_object, qNode.graph_object

        # p and q lie in the same trapezoid
        if len(intersectingTrapezoids) == 1:
            # we always need to split the trapezoid
            newTopTrapezoid = Trapezoid(line_seg.p, line_seg.q, pTrapezoid.top, line_seg)
            newBottomTrapezoid = Trapezoid(line_seg.p, line_seg.q, line_seg, pTrapezoid.bottom)

            # make a DAG y-node for these trapezoids with the line segment
            yNode = DAGNode(line_seg, newBottomTrapezoid.node, newTopTrapezoid.node)

            if q_exists:
                newBottomTrapezoid.setRightNeighbors(pTrapezoid.right_neighbors)
                # for neighbor in newBottomTrapezoid.right_neighbors:
                #     neighbor.left_neighbors.discard(pTrapezoid)

                newTopTrapezoid.setRightNeighbors(pTrapezoid.right_neighbors)
                # for neighbor in newTopTrapezoid.right_neighbors:
                #     neighbor.left_neighbors.discard(pTrapezoid)
            else:
                # make a trapezoid right of q
                if line_seg.q.x == pTrapezoid.right_p.x \
                        and any(len(neighbor.left_neighbors) >= 2 for neighbor in pTrapezoid.right_neighbors):
                    rightTrapezoid = Trapezoid(Point(line_seg.q.x, pTrapezoid.top.q.y),
                                               Point(line_seg.q.x, pTrapezoid.bottom.q.y),
                                               pTrapezoid.top, pTrapezoid.bottom)
                else:
                    rightTrapezoid = Trapezoid(line_seg.q, pTrapezoid.right_p, pTrapezoid.top, pTrapezoid.bottom)
                rightTrapezoid.setLeftNeighbors({newBottomTrapezoid, newTopTrapezoid})
                rightTrapezoid.setRightNeighbors(pTrapezoid.right_neighbors)

                # update right neighbors of containing trapezoid
                # for neighbor in rightTrapezoid.right_neighbors:
                #     neighbor.left_neighbors.discard(pTrapezoid)

                self.T.addTrapezoid({rightTrapezoid})
                qXnode = DAGNode(line_seg.q, yNode, rightTrapezoid.node)
                # change the pNode to the new qXnode
                if p_exists:
                    pNode.modify(qXnode)

            if p_exists:
                newBottomTrapezoid.setLeftNeighbors(pTrapezoid.left_neighbors)
                # for neighbor in newBottomTrapezoid.left_neighbors:
                #     neighbor.right_neighbors.discard(pTrapezoid)

                newTopTrapezoid.setLeftNeighbors(pTrapezoid.left_neighbors)
                # for neighbor in newTopTrapezoid.left_neighbors:
                #     neighbor.right_neighbors.discard(pTrapezoid)
            else:
                # make a trapezoid left of p
                if line_seg.p.x == pTrapezoid.left_p.x \
                        and any(len(neighbor.right_neighbors) >= 2 for neighbor in pTrapezoid.left_neighbors):
                    leftTrapezoid = Trapezoid(Point(line_seg.p.x, pTrapezoid.top.p.y),
                                              Point(line_seg.p.x, pTrapezoid.bottom.p.y),
                                              pTrapezoid.top, pTrapezoid.bottom)
                else:
                    leftTrapezoid = Trapezoid(pTrapezoid.left_p, line_seg.p, pTrapezoid.top, pTrapezoid.bottom)
                leftTrapezoid.setLeftNeighbors(pTrapezoid.left_neighbors)
                leftTrapezoid.setRightNeighbors({newBottomTrapezoid, newTopTrapezoid})

                # update left neighbors of containing trapezoid
                # for neighbor in leftTrapezoid.left_neighbors:
                #     neighbor.right_neighbors.discard(pTrapezoid)

                self.T.addTrapezoid({leftTrapezoid})
                pXnode = DAGNode(line_seg.p,
                                 leftTrapezoid.node,
                                 qXnode if not q_exists else yNode)
                pNode.modify(pXnode)

            if q_exists and p_exists:
                pNode.modify(yNode)

            # Update the trapezoidal map
            self.T.deleteTrapezoidFromMap({pTrapezoid})
            self.T.addTrapezoid({newTopTrapezoid, newBottomTrapezoid})

        elif len(intersectingTrapezoids) > 1:
            """ https://isotropic.org/papers/point-location.pdf """
            # Handle the trapezoid containing lineSegment.p
            # newLeftBottomTrapezoid = Trapezoid(lineSegment.p, lineSegment.get_Y(pTrapezoid.right_p.x),
            #                                    lineSegment, pTrapezoid.bottom)
            newLeftBottomTrapezoid = Trapezoid(line_seg.p, pTrapezoid.right_p, line_seg, pTrapezoid.bottom)
            newLeftBottomTrapezoid.setRightNeighbors(
                {n for n in pTrapezoid.right_neighbors if not line_seg.aboveLine(n.top.q)})

            # newLeftTopTrapezoid = Trapezoid(lineSegment.p, lineSegment.get_Y(pTrapezoid.right_p.x),
            #                                 pTrapezoid.top, lineSegment)
            newLeftTopTrapezoid = Trapezoid(line_seg.p, pTrapezoid.right_p, pTrapezoid.top, line_seg)
            newLeftTopTrapezoid.setRightNeighbors(
                {n for n in pTrapezoid.right_neighbors if line_seg.aboveLine(n.bottom.q)})

            if not p_exists:
                newLeftTrapezoid = Trapezoid(pTrapezoid.left_p, line_seg.p, pTrapezoid.top, pTrapezoid.bottom)
                newLeftTrapezoid.setLeftNeighbors(pTrapezoid.left_neighbors)
                newLeftTrapezoid.setRightNeighbors({newLeftTopTrapezoid, newLeftBottomTrapezoid})
            else:
                newLeftTopTrapezoid.setLeftNeighbors(pTrapezoid.left_neighbors)
                newLeftBottomTrapezoid.setLeftNeighbors(pTrapezoid.left_neighbors)

            # Handle the trapezoid containing lineSegment.q
            # newRightBottomTrapezoid = Trapezoid(lineSegment.get_Y(qTrapezoid.left_p.x), lineSegment.q,
            #                                     lineSegment, qTrapezoid.bottom)
            newRightBottomTrapezoid = Trapezoid(qTrapezoid.left_p, line_seg.q, line_seg, qTrapezoid.bottom)

            newRightBottomTrapezoid.setLeftNeighbors(
                {n for n in qTrapezoid.left_neighbors if not line_seg.aboveLine(n.top.q)})
            # newRightTopTrapezoid = Trapezoid(lineSegment.get_Y(qTrapezoid.left_p.x), lineSegment.q,
            #                                  qTrapezoid.top, lineSegment)
            newRightTopTrapezoid = Trapezoid(qTrapezoid.left_p, line_seg.q, qTrapezoid.top, line_seg)
            newRightTopTrapezoid.setLeftNeighbors(
                {n for n in qTrapezoid.left_neighbors if line_seg.aboveLine(n.bottom.q)})

            if not q_exists:
                newRightTrapezoid = Trapezoid(line_seg.q, qTrapezoid.right_p, qTrapezoid.top, qTrapezoid.bottom)
                newRightTrapezoid.setLeftNeighbors({newRightTopTrapezoid, newRightBottomTrapezoid})
                newRightTrapezoid.setRightNeighbors(qTrapezoid.right_neighbors)
            else:
                newRightTopTrapezoid.setRightNeighbors(qTrapezoid.right_neighbors)
                newRightBottomTrapezoid.setRightNeighbors(qTrapezoid.right_neighbors)

            # Walk to the right along the new segment and split
            # each trapezoid into upper and lower ones
            newTopTrapezoids, newBottomTrapezoids = [newLeftTopTrapezoid], [newLeftBottomTrapezoid]
            trap_dict = dict()
            trap_dict[pTrapezoid] = (newLeftTopTrapezoid, newLeftBottomTrapezoid)
            for t in intersectingTrapezoids[1:-1]:
                # create new top and bottom trapezoids
                # new_top = Trapezoid(lineSegment.get_Y(t.left_p.x), lineSegment.get_Y(t.right_p.x),
                #                     t.top, lineSegment)
                # new_bottom = Trapezoid(lineSegment.get_Y(t.left_p.x), lineSegment.get_Y(t.right_p.x),
                #                        lineSegment, t.bottom)
                new_top = Trapezoid(t.left_p, t.right_p, t.top, line_seg)
                new_bottom = Trapezoid(t.left_p, t.right_p, line_seg, t.bottom)

                # Update neighbors of the new top and bottom
                for n in t.left_neighbors:
                    if line_seg.aboveLine(n.bottom.q):
                        new_top.setLeftNeighbors({n})
                    if not line_seg.aboveLine(n.top.q):
                        new_bottom.setLeftNeighbors({n})
                new_top.setLeftNeighbors({newTopTrapezoids[-1]})
                new_bottom.setLeftNeighbors({newBottomTrapezoids[-1]})

                # Add it to the list and dict
                newTopTrapezoids.append(new_top)
                newBottomTrapezoids.append(new_bottom)
                trap_dict[t] = (new_top, new_bottom)

            newRightTopTrapezoid.setLeftNeighbors({newTopTrapezoids[-1]})
            newRightBottomTrapezoid.setLeftNeighbors({newBottomTrapezoids[-1]})
            newTopTrapezoids.append(newRightTopTrapezoid)
            newBottomTrapezoids.append(newRightBottomTrapezoid)
            trap_dict[qTrapezoid] = (newRightTopTrapezoid, newRightBottomTrapezoid)

            # Merge trapezoids with the same top and bottom line segments
            for k, g in groupby(newTopTrapezoids, lambda x: x.top):
                g = list(g)
                if len(g) > 1:
                    # create new merged trapezoid
                    t = Trapezoid(g[0].left_p, g[-1].right_p, k, g[0].bottom)
                    for n in g[0].left_neighbors:
                        n.right_neighbors.discard(g[0])
                    for n in g[-1].right_neighbors:
                        n.left_neighbors.discard(g[-1])
                    t.setLeftNeighbors(g[0].left_neighbors)
                    t.setRightNeighbors(g[-1].right_neighbors)

                    # Update list and dictionary
                    for k, v in trap_dict.items():
                        if v[0] in g:
                            trap_dict[k] = (t, v[1])

            for k, g in groupby(newBottomTrapezoids, lambda x: x.bottom):
                g = list(g)
                if len(g) > 1:
                    # create new merged trapezoid
                    t = Trapezoid(g[0].left_p, g[-1].right_p, g[0].top, k)
                    for n in g[0].left_neighbors:
                        n.right_neighbors.discard(g[0])
                    for n in g[-1].right_neighbors:
                        n.left_neighbors.discard(g[-1])
                    t.setLeftNeighbors(g[0].left_neighbors)
                    t.setRightNeighbors(g[-1].right_neighbors)

                    # Update list and dictionary
                    for k, v in trap_dict.items():
                        if v[1] in g:
                            trap_dict[k] = (v[0], t)

            # Updating the DAG and the Trapezoidal map
            if not p_exists:
                pTrapezoid.node = DAGNode(line_seg.p,
                                          left_child=newLeftTrapezoid.node,
                                          right_child=DAGNode(line_seg, trap_dict[pTrapezoid][1].node,
                                                              trap_dict[pTrapezoid][0].node))
                self.T.deleteTrapezoidFromMap({pTrapezoid})
                self.T.addTrapezoid({newLeftTrapezoid})
            if not q_exists:
                qTrapezoid.node = DAGNode(line_seg.q,
                                          left_child=DAGNode(line_seg, trap_dict[qTrapezoid][1].node,
                                                             trap_dict[qTrapezoid][0].node),
                                          right_child=newRightTrapezoid.node)
                self.T.deleteTrapezoidFromMap({qTrapezoid})
                self.T.addTrapezoid({newRightTrapezoid})
            for t in intersectingTrapezoids[0 if p_exists else 1: len(intersectingTrapezoids) if q_exists else -1]:
                t.node = DAGNode(line_seg, left_child=trap_dict[t][1].node, right_child=trap_dict[t][0].node)
            self.T.deleteTrapezoidFromMap(set(intersectingTrapezoids))
            self.T.addTrapezoid({v[0] for v in trap_dict.values()})
            self.T.addTrapezoid({v[1] for v in trap_dict.values()})

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
        self.T.addTrapezoid({B})
        self.T.G = DAG(DAGNode(B))
