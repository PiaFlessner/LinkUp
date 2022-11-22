from resFile import resFile
class resJewel:
    def __init__(self, restore_destination:str, jewel_id:int, res_file, jewel_source:str):
        self._restore_destination = restore_destination
        self._jewel_id = jewel_id
        self._res_file = res_file
        self._jewel_source = jewel_source

    # getter and setter methods for class properties
    @property
    def restore_destination(self):
        return self._restore_destination

    @restore_destination.setter
    def restore_destination(self, value):
        self._restore_destination = value

    @property
    def jewel_id(self):
        return self._jewel_id

    @jewel_id.setter
    def jewel_id(self, value):
        self._jewel_id = value

    @property
    def res_file(self):
        return self._res_file

    @res_file.setter
    def res_file(self, value):
        self._res_file = value

    @property
    def jewel_source(self):
        return self._jewel_source

    @jewel_source.setter
    def jewel_source(self, value):
        self._jewel_source = value
