from datetime import datetime


class HardlinkInfo:

    def __init__(self, id:int, source_path:str, destination_path:str, insert_date:datetime.date):
        self._id = id
        self._source_path = source_path
        self._destination_path = destination_path
        self._insert_date = insert_date

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def source_path(self):
        return self._source_path

    @source_path.setter
    def source_path(self, value):
        self._source_path = value

    @property
    def destination_path(self):
        return self._destination_path

    @destination_path.setter
    def destination_path(self, value):
        self._destination_path = value

    @property
    def insert_date(self):
        return self._insert_date

    @insert_date.setter
    def insert_date(self, value):
        self._insert_date = value
