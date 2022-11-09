class Data:
    def __init__(self, name, f_hash, f_size, birth, modify):
        self.name = name
        self.f_hash = f_hash
        self.f_size = f_size
        self.birth = birth
        self.modify = modify
    #Filename
    def get_f_name(self):
        return self.name
    #checksum
    def get_f_hash(self):
        return self.f_hash
    #filesize
    def get_f_size(self):
        return self.f_size
    #birth of file
    def get_birth(self):
        return self.birth
    #timestamp of filecontent modify
    def get_modify(self):
        return self.modify