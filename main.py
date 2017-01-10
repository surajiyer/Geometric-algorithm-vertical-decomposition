import matplotlib
from Polygon import Polygon, Point
from LineSegment import LineSegment
from RandomizedIncrementalConstruction import RandomizedIncrementalConstruction
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
        # TODO: compute corner coordinates
        # now we need to project a vertical line on the bottom edge
        if trapezoid.leftp == trapezoid.top.p:
            l = trapezoid.bottom
            y = l.getSlope() * trapezoid.leftp.x + l.getIntercept()
            y_s.extend([y, trapezoid.leftp.y])
        elif trapezoid.leftp == trapezoid.bottom.p:
            l = trapezoid.top
            y = l.getSlope() * trapezoid.leftp.x + l.getIntercept()
            y_s.extend([trapezoid.leftp.y, y])
        else:
            l = trapezoid.bottom
            y = l.getSlope() * trapezoid.leftp.x + l.getIntercept()
            y_s.append(y)
            l = trapezoid.top
            y = l.getSlope() * trapezoid.leftp.x + l.getIntercept()
            y_s.append(y)

        if trapezoid.rightp == trapezoid.top.p:
            l = trapezoid.bottom
            y = l.getSlope() * trapezoid.rightp.x + l.getIntercept()
            y_s.extend([trapezoid.rightp.y, y])
        elif trapezoid.rightp == trapezoid.bottom.p:
            l = trapezoid.top
            y = l.getSlope() * trapezoid.rightp.x + l.getIntercept()
            y_s.extend([y, trapezoid.rightp.y])
        else:
            l = trapezoid.top
            y = l.getSlope() * trapezoid.rightp.x + l.getIntercept()
            y_s.append(y)
            l = trapezoid.bottom
            y = l.getSlope() * trapezoid.rightp.x + l.getIntercept()
            y_s.append(y)

        y_s.append(y_s[0])
        x_s = [trapezoid.leftp.x, trapezoid.leftp.x, trapezoid.rightp.x, trapezoid.rightp.x, trapezoid.leftp.x]
        plt.plot(x_s, y_s, 'k')

    x_s = [p.x for p in P.V]
    y_s = [p.y for p in P.V]
    plt.fill(x_s, y_s, 'b')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    # make polygon based on input
    P = load_input('Data/test_1.txt')
    # Initialize algorithm (also computes the map already)
    R = RandomizedIncrementalConstruction(P)
    T = R.getTrapezoidalMap()
    print(T)
    visualize(P, T)

    """
    #testing aboveLine method
    P = Point(1,0)
    L = LineSegment(Point(5,5), Point(1,1))
    L.aboveLine(P)

    #testing trapezoid initialization
    T = Trapezoid(Point(2, 3), Point(3, 2), LineSegment(Point(4, 3), Point(3, 3)),
                  LineSegment(Point(1, 5), Point(6, 7)), [])
    print (T)

    trapezoidal_map = decompose(P)
    visualize(trapezoidal_map)
    """
