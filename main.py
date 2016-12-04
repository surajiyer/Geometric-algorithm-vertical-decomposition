import matplotlib
from Polygon import Polygon, Point


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


if __name__ == '__main__':
    P = load_input('test_0.txt')
    trapezoidal_map = decompose(P)
    visualize(trapezoidal_map)
