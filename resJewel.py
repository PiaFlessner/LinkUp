class resJewel:
    def __init__(self, restore_destination, jewel_id, res_file):
        self.restore_destination = restore_destination
        self.jewel_id = jewel_id
        self.res_file = res_file

    # getter and setter methods for class properties
    @property
    def restore_destination(self):
        return self.restore_destination

    @restore_destination.setter
    def restore_destination(self, value):
        self.restore_destination = value

    @property
    def jewel_id(self):
        return self.jewel_id

    @jewel_id.setter
    def jewel_id(self, value):
        self.jewel_id = value

    @property
    def res_file(self):
        return self.res_file

    @res_file.setter
    def res_file(self, value):
        self.res_file = value
