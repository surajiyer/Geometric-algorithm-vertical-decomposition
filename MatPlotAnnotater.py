import math
import matplotlib.pyplot as plt
from matplotlib.text import Annotation


class MatPlotAnnotater(object):
    """callback for matplotlib to display an annotation when points are
    clicked on.  The point which is closest to the click and within
    xtol and ytol is identified.

    Register this function like this:

    scatter(xdata, ydata)
    af = AnnoteFinder(xdata, ydata, annotes)
    connect('button_press_event', af)
    """

    def __init__(self, xdata, ydata, annotes, e_type, ax=None, xtol=None, ytol=None):
        self.data = list(zip(xdata, ydata, annotes))
        self.e_type = e_type
        if xtol is None:
            xtol = ((max(xdata) - min(xdata)) / float(len(xdata))) / 2
        if ytol is None:
            ytol = ((max(ydata) - min(ydata)) / float(len(ydata))) / 2
        self.xtol = xtol
        self.ytol = ytol
        if ax is None:
            self.ax = plt.gca()
        else:
            self.ax = ax
        if self.e_type == 'motion_notify_event':
            self.data = [(x, y, self.ax.annotate(a, xy=(x, y), xycoords='data',
                                                 xytext=(x, y+0.1), textcoords='data', wrap=True,
                                                 horizontalalignment="center",
                                                 arrowprops=dict(arrowstyle="simple", connectionstyle="arc3,rad=-0.2"),
                                                 bbox=dict(boxstyle="round", facecolor="w", edgecolor="0.5", alpha=0.9))
                          ) for (x, y, a) in self.data]
            for x, y, a in self.data:
                a.set_visible(False)
        self.drawnAnnotations = {}
        self.links = []

    def distance(self, x1, x2, y1, y2):
        """
        return the distance between two points
        """
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def __call__(self, event):
        if self.e_type == 'motion_notify_event':
            self.drawOnMove(event)
        else:
            if event.inaxes:
                clickX = event.xdata
                clickY = event.ydata
                if (self.ax is None) or (self.ax is event.inaxes):
                    annotes = []
                    for x, y, a in self.data:
                        # print(x, y, a)
                        if ((clickX - self.xtol < x < clickX + self.xtol) and
                                (clickY - self.ytol < y < clickY + self.ytol)):
                            annotes.append(
                                (self.distance(x, clickX, y, clickY), x, y, a))
                    if annotes:
                        annotes.sort()
                        distance, x, y, annote = annotes[0]
                        self.drawAnnote(event.inaxes, x, y, annote)
                        for l in self.links:
                            l.drawSpecificAnnote(annote)

    def drawAnnote(self, ax, x, y, annote):
        """
        Draw the annotation on the plot
        """
        if (x, y) in self.drawnAnnotations:
            markers = self.drawnAnnotations[(x, y)]
            for m in markers:
                m.set_visible(not m.get_visible())
            self.ax.figure.canvas.draw_idle()
        else:
            t = ax.text(x, y, " - %s" % annote, )
            m = ax.scatter([x], [y], marker='d', c='r', zorder=100)
            self.drawnAnnotations[(x, y)] = (t, m)
            self.ax.figure.canvas.draw_idle()

    def drawSpecificAnnote(self, annote):
        annotesToDraw = [(x, y, a) for x, y, a in self.data if a == annote]
        for x, y, a in annotesToDraw:
            self.drawAnnote(self.ax, x, y, a)

    def drawOnMove(self, event):
        visibility_changed = False
        if (self.ax is None) or (self.ax is event.inaxes):
            clickX = event.xdata
            clickY = event.ydata
            for x, y, annotation in self.data:
                should_be_visible = (clickX - self.xtol < x < clickX + self.xtol) \
                                    and (clickY - self.ytol < y < clickY + self.ytol)
                if should_be_visible and isinstance(annotation, str):
                    self.drawAnnote(event.inaxes, x, y, annotation)
                elif isinstance(annotation, Annotation) and should_be_visible != annotation.get_visible():
                    visibility_changed = True
                    annotation.set_visible(should_be_visible)
        if visibility_changed:
            plt.draw()
