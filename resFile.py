class resFile:
    def __init__(self, file_name:str, origin_location:str, backup_location:str, version_number:int):
        self._file_name = file_name
        self._origin_location = origin_location
        self._backup_location = backup_location
        self._version_number = version_number

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