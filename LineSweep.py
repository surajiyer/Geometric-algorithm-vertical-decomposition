from Polygon import Polygon, Point, LineSegment
from TrapezoidMap import TrapezoidMap, Trapezoid
from bintrees import AVLTree


class LineSweep:
    def __init__(self, polygon):
        assert isinstance(polygon, Polygon)
        self.polygon = polygon
        # the event structure
        self.Q = []
        # the status structure
        self.S = AVLTree()
        self.lineSweep()


    def getTrapezoidalMap(self) -> TrapezoidMap:
        return self.T

    """
    Run the line sweep
    """

    def lineSweep(self):
        self.T = TrapezoidMap([])
        # first initialize the event structure
        self.initEventStructure()
        # now compute the bounding box
        self.computeBoundingBox()
        # now loop over the event points
        for event in self.Q:
            self.handleEventPoint(event)

    def handleEventPoint(self, event):
        # first we check which "kind" of point we have for each edge
        # the event point is the startpoint of this edge
        for j in range(2, len(event)) :
            if event[0] == event[j].p:
                self.handleStartPoint(event[0], event[j], event[1])
            elif event[0] == event[j].q:
                self.handleEndPoint(event[0], event[j], event[1])

    def handleStartPoint(self, point, linesegment, case = None):
        assert isinstance(point, Point)
        assert isinstance(linesegment, LineSegment)
        # TODO: handle start event point
        print("point", point, " is the startpoint of linesegment", linesegment)
        # insert the segment into the status
        self.S.insert(linesegment, None)
        print("inserted:", self.S)
        try:
            pred = self.S.prev_key(linesegment)
        except KeyError:
            pred = None

        try:
            succ = self.S.succ_key(linesegment)
        except KeyError:
            succ = None

        if case == "A":
            pass
        elif case == "B":
            pass
        elif case == "C":
            pass
        elif case == "D":
            pass
        elif case == "E":
            pass
        elif case == "F":
            pass
        else:
            # the event point is on the bounding box
            pass


    def handleEndPoint(self, point, linesegment, case):
        assert isinstance(point, Point)
        assert isinstance(linesegment, LineSegment)
        # TODO: handle end event point
        print("point", point, " is the endpoint of linesegment", linesegment)

        try:
            pred = self.S.prev_key(linesegment)
        except KeyError:
            print(linesegment, "had no predecessor")
            pred = None

        try:
            succ = self.S.succ_key(linesegment)
        except KeyError:
            succ = None

        if case == "A":
            # make a trapezoid with the current linesegment
            if pred.p.x <= linesegment.p.x:
                self.T.addTrapezoid(Trapezoid(linesegment.p, linesegment.q, linesegment, pred))
            elif pred.p.x > linesegment.p.x and pred.p.x < linesegment.q.x:
                self.T.addTrapezoid(Trapezoid(pred.p, linesegment.q, linesegment, pred))
            else:
                # in this case we do not know bottom so do nothing
                pass
        elif case == "B":
            pass
        elif case == "C":
            pass
        elif case == "D":
            pass
        elif case == "E":
            pass
        elif case == "F":
            pass
        else:
            # the event point is on the bounding box
            pass

        # remove the linesegment from the status
        self.S.remove(linesegment)
        print("removed:", self.S)

    def initEventStructure(self):
        #the edge between the first and last point
        lastEdge = LineSegment(self.polygon.V[0], self.polygon.V[-1])

        # if points have the same x, the point with lowest y goes first
        for i in range(len(self.polygon.V)):
            eventPoint = []
            eventPoint.append(self.polygon.V[i])
            #the current point is not the first or last one
            if i != 0:
                # the edge between the current point and the previous one
                eventPoint.append(LineSegment(self.polygon.V[i], self.polygon.V[i - 1]))
            else:
                eventPoint.append(lastEdge)
            if i != (len(self.polygon.V) - 1):
                # the edge between the current point and the next one
                eventPoint.append(LineSegment(self.polygon.V[i], self.polygon.V[i + 1]))
            else:
                eventPoint.append(lastEdge)

            # now also "sort" the edges of an event such that the edge where the point is the endpoint is done first
            # if the point equals the endpoint (q) of the first edge, we are fine
            if eventPoint[1].q == eventPoint[0]:
                pass
            elif eventPoint[2].q == eventPoint[0]:
                # in this case we must swap eventPoint[1] and eventPoint[2]
                eventPoint[1], eventPoint[2] = eventPoint[2], eventPoint[1]

            # now we wish to determine the "case" we have here
            eventPoint.insert(1, self.determineCase(eventPoint[0], eventPoint[1], eventPoint[2]))

            self.Q.append(eventPoint)

        self.Q.sort(key=lambda event: (event[0].x, event[0].y))

    # given a point and two lines connected to this point, determine the configuration they are in
    def determineCase(self, point, l1, l2):
        assert(isinstance(point, Point))
        assert (isinstance(l1, LineSegment))
        assert (isinstance(l2, LineSegment))

        if l1.isVertical and not l2.isVertical:
            if l2.p == l1.p or l2.p == l1.q:
                return "D"
            elif l2.q == l1.p or l2.q == l1.q:
                return "E"
        elif l2.isVertical and not l1.isVertical:
            if l1.p == l2.p or l1.p == l2.q:
                return "D"
            elif l1.q == l2.p or l1.q == l2.q:
                return "E"
        elif l1.isVertical and l2.isVertical:
            return "F"
        elif point == l1.p and point == l2.p:
            return "B"
        elif point == l1.q and point == l2.q:
            return "C"
        elif point == l1.q and point == l2.p:
            return "A"
        else:
            raise ValueError("Case not defined")

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

        #define bounding box edges
        topEdge = LineSegment(Point(bottomLeft.x, topRight.y), Point(topRight.x, topRight.y))
        bottomEdge = LineSegment(Point(bottomLeft.x, bottomLeft.y), Point(topRight.x, bottomLeft.y))

        # based on the bounding box dimensions we add events to Q
        # first insert the top left point of the bounding box since it should be the second event
        self.Q.insert(0, [topEdge.p, "G", topEdge])
        # then insert the bottom left point of the bounding box since it should be the first event
        self.Q.insert(0, [bottomEdge.p, "G", bottomEdge])
        # then append the bottom right point as it should be the second to last event
        self.Q.append([bottomEdge.q, "G", bottomEdge])
        # and finally append the top right point
        self.Q.append([topEdge.q, "G", topEdge])

        print("Event Structure: ", self.Q)

