from Polygon import Polygon, Point
from RandomizedIncrementalConstruction import RandomizedIncrementalConstruction
import time
import gc
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
            y = l.slope * trapezoid.left_p.x + l.intercept
            y_s.extend([y, trapezoid.left_p.y])
        elif trapezoid.left_p == trapezoid.bottom.p:
            l = trapezoid.top
            y = l.slope * trapezoid.left_p.x + l.intercept
            y_s.extend([trapezoid.left_p.y, y])
        else:
            l = trapezoid.bottom
            y = l.slope * trapezoid.left_p.x + l.intercept
            y_s.append(y)
            l = trapezoid.top
            y = l.slope * trapezoid.left_p.x + l.intercept
            y_s.append(y)

        if trapezoid.right_p == trapezoid.top.p:
            l = trapezoid.bottom
            y = l.slope * trapezoid.right_p.x + l.intercept
            y_s.extend([trapezoid.right_p.y, y])
        elif trapezoid.right_p == trapezoid.bottom.p:
            l = trapezoid.top
            y = l.slope * trapezoid.right_p.x + l.intercept
            y_s.extend([y, trapezoid.right_p.y])
        else:
            l = trapezoid.top
            y = l.slope * trapezoid.right_p.x + l.intercept
            y_s.append(y)
            l = trapezoid.bottom
            y = l.slope * trapezoid.right_p.x + l.intercept
            y_s.append(y)

        y_s.append(y_s[0])
        x_s = [trapezoid.left_p.x, trapezoid.left_p.x, trapezoid.right_p.x, trapezoid.right_p.x, trapezoid.left_p.x]
        plt.plot(x_s, y_s, 'k')

    x_s = [p.x for p in P.V]
    y_s = [p.y for p in P.V]
    plt.fill(x_s, y_s, 'b')
    plt.show()


if __name__ == '__main__':
    # make polygon based on input
    P = load_input('Data/gen_10000.txt')

    # Initialize algorithm (also computes the map already)
    times = []
    for i in range(0, 10):
        start = time.time()
        R = RandomizedIncrementalConstruction(P)
        end = time.time()
        print("Execution time:", (end-start)*1000)
        times.append((end-start)*1000)

        # Visualize the map
        T = R.getTrapezoidalMap()
        visualize(P, T)
        T.visualize_graph()

        # Garbage collection
        if (i != 9):
            R = None
            gc.collect()
