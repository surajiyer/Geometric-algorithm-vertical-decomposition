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
        # if the event contains a point on the bounding box
        if event[1] == "G":
            if event[0] == event[2].p:
                self.handleStartPoint(event[0], event[2], event[1])
            else:
                self.handleEndPoint(event[0], event[2], event[1])

        else:
            if event[0] == event[2].p:
                self.handleStartPoint(event[0], event[2], event[1], event[3])
            elif event[0] == event[2].q:
                self.handleEndPoint(event[0], event[2], event[1], event[3])
            else:
                raise ValueError("point is not part of the linesegment")

            if event[0] == event[3].p:
                self.handleStartPoint(event[0], event[3], event[1], event[2])
            elif event[0] == event[3].q:
                self.handleEndPoint(event[0], event[3], event[1], event[2])
            else:
                raise ValueError("point is not part of the linesegment")

    def handleStartPoint(self, point, linesegment, case = None, otherline = None):
        assert isinstance(point, Point)
        assert isinstance(linesegment, LineSegment)
        # TODO: handle start event point
        print("point", point, " is the startpoint of linesegment", linesegment)
        # insert the segment into the status
        self.S.insert(linesegment, linesegment)
        print("inserted:", linesegment)
        print(self.S)

        pred = self.getPred(linesegment)
        succ = self.getSucc(linesegment)

        if case == "A":
            pass
        elif case == "B":
            #make trapezoids with pred and/or succ
            if pred.p.x < succ.p.x:
                self.T.addTrapezoid([Trapezoid(succ.p, point, succ, pred)])
            else:
                self.T.addTrapezoid([Trapezoid(pred.p, point, succ, pred)])
        elif case == "C":
            raise ValueError ("This should not happen!")
        elif case == "D":
            pass
        elif case == "E":
            pass
        elif case == "F":
            # we simply ignore this case
            pass
        else:
            # the event point is on the bounding box
            pass


    def handleEndPoint(self, point, linesegment, case, otherline = None):
        assert isinstance(point, Point)
        assert isinstance(linesegment, LineSegment)
        # TODO: handle end event point
        print("point", point, " is the endpoint of linesegment", linesegment)

        pred = self.getPred(linesegment)
        succ = self.getSucc(linesegment)

        if case == "A":
            # make a trapezoid with the current linesegment
            if pred.p.x <= linesegment.p.x:
                self.T.addTrapezoid([Trapezoid(linesegment.p, linesegment.q, linesegment, pred)])
            elif pred.p.x > linesegment.p.x and pred.p.x < linesegment.q.x:
                self.T.addTrapezoid([Trapezoid(pred.p, linesegment.q, linesegment, pred)])
            else:
                # in this case we do not know bottom so do nothing
                pass

            #also consider successor
            if succ.p.x <= linesegment.p.x:
                self.T.addTrapezoid([Trapezoid(linesegment.p, linesegment.q, succ, linesegment)])
            elif pred.p.x > linesegment.p.x and pred.p.x < linesegment.q.x:
                self.T.addTrapezoid([Trapezoid(succ.p, linesegment.q, succ, linesegment)])
            else:
                # in this case we do not know bottom so do nothing
                pass
        elif case == "B":
            raise ValueError("this should not be possible!")
        elif case == "C":

            if(linesegment > otherline):
                # the current line is the top line
                #make a trapezoid to the left
                if succ.p.x < linesegment.p.x:
                    self.T.addTrapezoid([Trapezoid(linesegment.p, point, succ, linesegment)])
                else:
                    self.T.addTrapezoid([Trapezoid(succ.p, point, succ, linesegment)])

            if(linesegment < otherline):
                # the current line is the bottom one
                # make a trapezoid to the left
                if pred.p.x < linesegment.p.x:
                    self.T.addTrapezoid([Trapezoid(linesegment.p, point, linesegment, pred)])
                else:
                    self.T.addTrapezoid([Trapezoid(pred.p, point, linesegment, pred)])

            # first check the pred and succ of the current line
            if pred == otherline:
                # get a new predecessor
                pred = self.getPred(otherline)

            if succ == otherline:
                # get a new successor
                succ = self.getSucc(otherline)

            # make trapezoids with pred and/or succ to the right
            if pred.q.x < succ.q.x:
                self.T.addTrapezoid([Trapezoid(point, pred.q, succ, pred)])
            else:
                self.T.addTrapezoid([Trapezoid(point, succ.q, succ, pred)])

        elif case == "D":
            pass
        elif case == "E":
            pass
        elif case == "F":
            # we simply ignore this case
            pass
        else:
            # the event point is on the bounding box
            pass

        # remove the linesegment from the status
        self.S.remove(linesegment)
        print("removed:", linesegment)
        print(self.S)

    def getPred(self, linesegment) -> LineSegment:
        assert(isinstance(linesegment, LineSegment))
        try:
            return self.S.prev_key(linesegment)
        except KeyError:
            if(not self.S.__contains__(linesegment)):
                #linesegment not found in the tree!, inserting again and finding predecessor
                self.S.insert(linesegment, linesegment)
                return self.S.prev_key(linesegment)
            print("linesegment was there but there was no predecessor")
            return None

    def getSucc(self, linesegment) -> LineSegment:
        assert(isinstance(linesegment, LineSegment))
        try:
            return self.S.succ_key(linesegment)
        except KeyError:
            if (not self.S.__contains__(linesegment)):
                # linesegment not found in the tree!, inserting again and finding predecessor
                self.S.insert(linesegment, linesegment)
                return self.S.succ_key(linesegment)
            print("linesegment was there but there was no successor")
            return None

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

