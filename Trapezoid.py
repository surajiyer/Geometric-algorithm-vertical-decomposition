class Trapezoid:
    """
    Class representing a trapezoid with top, bottom, leftp and rightp
    (2 line segments and 2 endpoints respectively)
    """
    def __init__(self, leftp, rightp, top, bottom):
        self.leftp = leftp
        self.rightp = rightp
        self.top = top
        self.bottom = bottom
