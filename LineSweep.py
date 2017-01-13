from Polygon import Polygon, Point, LineSegment
from TrapezoidMap import TrapezoidMap, Trapezoid


class LineSweep:
    def __init__(self, polygon):
        assert isinstance(polygon, Polygon)
        self.polygon = polygon
        # the event structure
        self.Q = []
        # the status structure
        self.S = []
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
        for point in self.Q:
            self.handleEventPoint(point)

    def handleEventPoint(self, point):
        # TODO: handle event point

    def initEventStructure(self):
        # TODO: sort the points based on x coordinate from low to high
        # if points have the same x, the point with lowest y goes first
        for point in self.polygon.V:
            self.Q.append(point)

        self.Q.sort()

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

        # TODO: we might need a different point class here, discuss with group
        # based on the bounding box dimensions we add events to Q
        # first insert the top left point of the bounding box since it should be the second event
        self.Q.insert(Point(bottomLeft.x, topRight.y), 0)
        # then insert the bottom left point of the bounding box since it should be the first event
        self.Q.insert(Point(bottomLeft.x, bottomLeft.y), 0)
        # then append the bottom right point as it should be the second last event
        self.Q.append(Point(topRight.x, bottomLeft.y))
        # and finally append the top right point
        self.Q.append(Point(topRight.x, topRight.y))

