class Data:
    def __init__(self, name, f_hash, f_size, birth, meta_change, modify):
        self.name = name
        self.meta_change = meta_change
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
    #change Date -> timestamp of change of metadata
    def get_meta_change(self):
        return self.get_meta_change
    #birth of file
    def get_birth(self):
        return self.birth
    #timestamp of filecontent modify
    def get_modify(self):
        return self.modify