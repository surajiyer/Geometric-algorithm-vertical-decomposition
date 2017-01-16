from Polygon import Polygon, Point, LineSegment
from RandomizedIncrementalConstruction import RandomizedIncrementalConstruction
from LineSweep import LineSweep
import matplotlib.pyplot as plt


def load_input(file_name):
    """
    Loads input, parses input and returns graph data structure
    :param file_name:
    :return:
    """
    with open(file_name, 'r') as file:
        n = int(file.readline())
        V = []

        # Create a polygon
        for i in range(n):
            line = file.readline()
            line = [int(l) for l in line.split()]
            # We add 1 to every value such that we can always make a bounding
            # box around the coordinates s.t. the bounding box does not intersect
            # with for example a point (0, 0)
            V.append(Point(line[0] + 1, line[1] + 1))
        P = Polygon(V)

        return P


def visualize(P, MAP):
    """
    Visualize the given trapezoidal map with matplotlib
    :param MAP:
    :return:
    """
    for trapezoid in MAP.trapezoids:
        y_s = []
        # now we need to project a vertical line on the bottom edge
        if trapezoid.left_p == trapezoid.top.p:
            l = trapezoid.bottom
            y = l.getSlope() * trapezoid.left_p.x + l.getIntercept()
            y_s.extend([y, trapezoid.left_p.y])
        elif trapezoid.left_p == trapezoid.bottom.p:
            l = trapezoid.top
            y = l.getSlope() * trapezoid.left_p.x + l.getIntercept()
            y_s.extend([trapezoid.left_p.y, y])
        else:
            l = trapezoid.bottom
            y = l.getSlope() * trapezoid.left_p.x + l.getIntercept()
            y_s.append(y)
            l = trapezoid.top
            y = l.getSlope() * trapezoid.left_p.x + l.getIntercept()
            y_s.append(y)

        if trapezoid.right_p == trapezoid.top.p:
            l = trapezoid.bottom
            y = l.getSlope() * trapezoid.right_p.x + l.getIntercept()
            y_s.extend([trapezoid.right_p.y, y])
        elif trapezoid.right_p == trapezoid.bottom.p:
            l = trapezoid.top
            y = l.getSlope() * trapezoid.right_p.x + l.getIntercept()
            y_s.extend([y, trapezoid.right_p.y])
        else:
            l = trapezoid.top
            y = l.getSlope() * trapezoid.right_p.x + l.getIntercept()
            y_s.append(y)
            l = trapezoid.bottom
            y = l.getSlope() * trapezoid.right_p.x + l.getIntercept()
            y_s.append(y)

        y_s.append(y_s[0])
        x_s = [trapezoid.left_p.x, trapezoid.left_p.x, trapezoid.right_p.x, trapezoid.right_p.x, trapezoid.left_p.x]
        plt.plot(x_s, y_s, 'k')

    x_s = [p.x for p in P.V]
    y_s = [p.y for p in P.V]
    plt.fill(x_s, y_s, 'b')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    # make polygon based on input
    # P = load_input('Data/test_2.txt')
    # # Initialize algorithm (also computes the map already)
    # R = RandomizedIncrementalConstruction(P)
    # T = R.getTrapezoidalMap()
    # for trap in T.trapezoids:
    #     print(trap)
    #     print(trap.left_neighbors)
    #     print(trap.right_neighbors)
    # visualize(P, T)

    P = load_input('Data/test_0.txt')
    # Initialize algorithm (also computes the map already)
    R = LineSweep(P)
    print(LineSegment(Point(3, 3), Point(7, 3)) > LineSegment(Point(4, 4), Point(5, 7)))
    T = R.getTrapezoidalMap()
    visualize(P, T)

    # # testing aboveLine method
    # P = Point(1, 0)
    # L = LineSegment(Point(5, 5), Point(1, 1))
    # L.aboveLine(P)
    #
    # # testing trapezoid initialization
    # T = Trapezoid(Point(2, 3), Point(3, 2), LineSegment(Point(4, 3), Point(3, 3)),
    #               LineSegment(Point(1, 5), Point(6, 7)))
    # print(T)
    #
    # trapezoidal_map = decompose(P)
    # visualize(trapezoidal_map)
