from datetime import datetime


class HardlinkInfo:

    def __init__(self, id:int, link_path:str, destination_path:str, insert_date:datetime.date, origin_name:str, source_path:str, jewel_id:int, old_hardlink_existing:bool ):
        self._id = id
        self._source_path = source_path
        self._destination_path = destination_path
        self._insert_date = insert_date
        self._origin_name = origin_name
        self._link_path = link_path
        self._jewel_id = jewel_id
        self._old_hardlink_existing = old_hardlink_existing

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

    @property
    def origin_name(self):
        return self._origin_name

    @origin_name.setter
    def origin_name(self, value):
        self._origin_name = value

    @property
    def link_path(self):
        return self._link_path

    @link_path.setter
    def link_path(self, value):
        self._link_path = value

    @property
    def jewel_id(self):
        return self._jewel_id

    @jewel_id.setter
    def jewel_id(self, value):
        self._jewel_id = value

    @property
    def old_hardlink_existing(self):
        return self._old_hardlink_existing

    @old_hardlink_existing.setter
    def old_hardlink_existing(self,value):
        self._old_hardlink_existing = value
