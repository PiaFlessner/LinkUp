class resObject:
    def __init__(self, res_jewel):
        self.res_jewel = res_jewel

    # getter and setter methods for class properties
    @property
    def res_jewel(self):
        return self.res_jewel

    @res_jewel.setter
    def res_jewel(self, value):
        self.res_jewel = value
