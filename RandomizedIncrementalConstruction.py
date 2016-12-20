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



    def computeBoundingBox(self):
        # find  top right point to create a bounding box (bottom left is [0, 0])
        topRight = Point(0, 0)

        for point in self.polygon.V:
            if point.get_x() >= topRight.get_x():
                topRight.set_x(point.get_x() + 1)
            if point.get_y() >= topRight.get_y():
                topRight.set_y(point.get_y() + 1)

        #Now add the bounding box as a trapezoid
        B = Trapezoid(Point(0, 0), topRight,
                                      LineSegment(Point(0, topRight.get_y()), topRight),
                                      LineSegment(Point(0, 0), Point(topRight.get_x(), 0)), [])
        self.T.addTrapezoid(B)
        self.DAG = DAG(DAGNode(B))