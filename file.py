class File:
    def __init__(self, name, f_hash, f_size, birth, modify):
        self.name = name
        self.f_hash = f_hash
        self.f_size = f_size
        self.birth = birth
        self.modify = modify

    def get_f_name(self):
        return self.name

    def get_f_hash(self):
        return self.f_hash

    def get_f_size(self):
        return self.f_size

    def get_creation_date(self):
        return self.birth

    def get_modify(self):
        return self.modify