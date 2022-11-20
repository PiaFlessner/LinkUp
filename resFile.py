class resFile:
    def __init__(self, file_name, origin_location, backup_location):
        self.file_name = file_name
        self.origin_location = origin_location
        self.backup_location = backup_location

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