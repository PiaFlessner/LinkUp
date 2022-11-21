class resFile:
    def __init__(self, file_name:str, origin_location:str, backup_location:str, version_number:int):
        self.file_name = file_name
        self.origin_location = origin_location
        self.backup_location = backup_location
        self.version_number = version_number

    # getter and setter methods for class properties
    @property
    def file_name(self):
        return self.file_name

    @file_name.setter
    def file_name(self, value):
        self.file_name = value

    @property
    def origin_location(self):
        return self.origin_location

    @origin_location.setter
    def origin_location(self, value):
        self.origin_location = value

    @property
    def backup_location(self):
        return self.backup_location

    @backup_location.setter
    def backup_location(self, value):
        self.backup_location = value
    
    @property
    def version_number(self):
        return self.version_number

    @version_number.setter
    def version_number(self, value):
        self.version_number = value