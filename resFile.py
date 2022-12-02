class resFile:
    def __init__(self, file_name: str, origin_location: str, backup_location: str, version_number: int, hash:str, reed_solomon_path:str=None):
        self._file_name = file_name
        self._origin_location = origin_location
        self._backup_location = backup_location
        self._version_number = version_number
        self._hash = hash
        self._reed_solomon_path = reed_solomon_path

    # getter and setter methods for class properties
    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def origin_location(self):
        return self._origin_location

    @origin_location.setter
    def origin_location(self, value):
        self._origin_location = value

    @property
    def backup_location(self):
        return self._backup_location

    @backup_location.setter
    def backup_location(self, value):
        self._backup_location = value

    @property
    def version_number(self):
        return self._version_number

    @version_number.setter
    def version_number(self, value):
        self._version_number = value
        
    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self, value):
        self._hash = value

    @property
    def reed_solomon_path(self):
        return self._reed_solomon_path

    @reed_solomon_path.setter
    def reed_solomon_path(self, value):
        self._reed_solomon_path = value

        
