from Polygon import Polygon, Point, LineSegment
from TrapezoidMap import TrapezoidMap, Trapezoid
from operator import itemgetter
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
        self.Test = []
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
        for j in range(1, len(event)) :
            if event[0] == event[j].p:
                self.handleStartPoint(event[0], event[j])
            elif event[0] == event[j].q:
                self.handleEndPoint(event[0], event[j])

    def handleStartPoint(self, point, linesegment):
        assert isinstance(point, Point)
        assert isinstance(linesegment, LineSegment)
        # TODO: handle start event point
        # print("point", point, " is the startpoint of linesegment", linesegment)
        self.Test.append([linesegment, None])
        self.S.insert(linesegment, None)
        print(self.S)


    def handleEndPoint(self, point, linesegment):
        assert isinstance(point, Point)
        assert isinstance(linesegment, LineSegment)
        # TODO: handle end event point
        # print("point", point, " is the endpoint of linesegment", linesegment)

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

            self.Q.append(eventPoint)

        self.Q.sort(key=lambda event: (event[0].x, event[0].y))

    def computeBoundingBox(self):
        # find  top right point to create a bounding box (bottom left is [0, 0])
        # TODO: we might need a different point class here, discuss with group
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
        self.Q.insert(0, [topEdge.p, topEdge])
        # then insert the bottom left point of the bounding box since it should be the first event
        self.Q.insert(0, [bottomEdge.p, bottomEdge])
        # then append the bottom right point as it should be the second to last event
        self.Q.append([bottomEdge.q, bottomEdge])
        # and finally append the top right point
        self.Q.append([topEdge.q, topEdge])

        print("Event Structure: ", self.Q)

