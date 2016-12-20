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
            #We add 1 to every value such that we can always make a bounding
            #box around the coordinates s.t. the bounding box does not intersect
            #with for example a point (0, 0)
            V.append(Point(line[0] + 1, line[1] + 1))
        P = Polygon(V)

        return P

def visualize(P):
    """
    Visualize the given trapezoidal map with matplotlib
    :param G:
    :return:
    """
    print(P.E)
    x = [p.x for p in P.V]
    y = [p.y for p in P.V]
    plt.fill(x, y, 'b')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    #make polygon based on input
    P = load_input('test_0.txt')
    #Initialize algorithm (also computes the map already)
    R = RandomizedIncrementalConstruction(P)
    T = R.getTrapezoidalMap()
    print(T)
    #visualize(T)

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

