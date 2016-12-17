import matplotlib
from Polygon import Polygon, Point
from Trapezoid import Trapezoid
from LineSegment import LineSegment
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
            V.append(Point(line[0], line[1]))
        P = Polygon(V)

        return P


def decompose(P):
    """
    Create a vertical decomposition of a simple polygon
    :param P: A simple polygon
    :return: Trapezoid map
    """
    print(P.V)
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
    #testing trapezoid initialization
    T = Trapezoid(Point(2, 3), Point(3, 2), LineSegment(Point(4, 3), Point(3, 3)),
                  LineSegment(Point(1, 5), Point(6, 7)), [])
    """P = load_input('test_0.txt')
    trapezoidal_map = decompose(P)
    visualize(trapezoidal_map)"""

