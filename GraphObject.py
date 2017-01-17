class GraphObject:
    def __init__(self):
        pass

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        # return hash(tuple(sorted(self.__dict__.items())))
        return hash(str(self))
