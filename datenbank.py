from ast import And
import itertools
import sqlite3
from os.path import exists as file_exists
from unicodedata import numeric
import uuid
import base64
import datetime
import platform


class Jewel:

    def __init__(self, id, comment, monitoring_Startdate, jewelSource, device_name, fullbackup_source):
        self.id = id
        self.comment = comment
        self.monitoring_Startdate = monitoring_Startdate
        self.jewelSource = jewelSource
        self.device_name = device_name
        self.fullbackup_source = fullbackup_source


class File:

    def __init__(self, id, blobs, birth):
        self.id = id
        self.blobs = blobs
        self.birth = birth

    def get_last_blob(self):
        return self.blobs[len(self.blobs) - 1]


class Blob:

    def __init__(self, id, number, hash, name, fileSize, creationDate, modify, iD_File, origin_name, source_path,
                 store_destination):
        self.id = id
        self.number = number
        self.hash = str(hash)
        self.name = str(name)
        self.fileSize = fileSize
        self.creationDate = creationDate
        self.modify = modify
        self.iD_File = iD_File
        self.origin_name = str(origin_name)
        self.store_destination = str(store_destination)
        self.source_path = str(source_path)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, self.__class__):
            return str(self.hash) == str(other.hash) and self.modify == other.modify and str(
                self.store_destination) == str(other.store_destination) and str(self.origin_name) == str(
                other.origin_name) and str(self.source_path) == str(other.source_path)
        else:
            return False


class Datenbank:

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        except sqlite3.Error as e:
            print(e)

        return conn

    def __init__(self):
        # Datenbank.create_connection = classmethod(Datenbank.create_connection)
        if not file_exists('datenbank.db'):
            conn = self.create_connection('datenbank.db')
            if conn != None:
                cur = conn.cursor()
                cur.execute("""CREATE TABLE Jewel (
                                    ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    Comment TEXT,
                                    Monitoring_Startdate NUMERIC NOT NULL,
                                    JewelSource TEXT NOT NULL,
                                    DeviceName TEXT NOT NULL,
                                    FullbackupSource TEXT NOT NULL
                                                 );""")

                cur.execute("""CREATE TABLE File (
                                    ID TEXT NOT NULL PRIMARY KEY,
                                    Birth TIMESTAMP NOT NULL
                                                );""")

                cur.execute("""CREATE TABLE Jewel_File_Assignment (
                                    ID_Jewel INTEGER NOT NULL,
                                    ID_File INTEGER NOT NULL,
                                    PRIMARY KEY(ID_Jewel,ID_File),
                                     constraint file_assignment_fk
                                     FOREIGN KEY (ID_File)
                                        REFERENCES File(ID),
                                     constraint jewel_assignment_fk
                                     FOREIGN KEY (ID_Jewel)
                                        REFERENCES Jewel(ID)
                                                 );""")

                cur.execute("""CREATE TABLE Blob (
                                    ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    Number INTEGER NOT NULL,
                                    Hash TEXT NOT NULL,
                                    Name TEXT NOT NULL,
                                    FileSize INTEGER NOT NULL,
                                    CreationDate TIMESTAMP,
                                    Modify TIMESTAMP,
                                    ID_File INTEGER NOT NULL,
                                    Origin_Name TEXT NOT NULL,
                                    Source_Path TEXT NOT NULL,
                                    Store_Destination TEXT NOT NULL,
                                    constraint file_blob_fk
                                    FOREIGN KEY (ID_File)
                                        REFERENCES File(ID)
                                                   );""")

                cur.execute("""CREATE TABLE Skipped_Files(
                    ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    ID_Jewel INTEGER NOT NULL,
                    UUID TEXT NOT NULL,
                    Occurance_Date TIMESTAMP NOT NULL,
                    Hash TEXT NOT NULL,
                    Reason TEXT NOT NULL,
                    Additional_Information TEXT,
                    Connected_File_to_Jewel TEXT
                );""")

                # Number, Hash, Name, FileSize, CreationDate, Modify, ID_File, Origin_Name, Source_Path, Store_Destination

                conn.commit()
                conn.close()

    def _encode_base64(self, name):
        name = str(name)
        name_bytes = bytes(name, 'UTF-8')
        return base64.b64encode(name_bytes).decode("UTF-8")

    def _decode_base64(self, name):
        name = str(name)
        name_bytes = bytes(name, 'UTF-8')
        return base64.b64decode(name_bytes).decode("UTF-8")

    def set_uri(self, file, device_name, file_path, file_name):
        # uri = uuid.uuid3(uuid.NAMESPACE_OID, device_name + file_path + file_name)
        uri = device_name + file_path
        file.id = uri

    def add_to_database(self, jewel, file, device_name):

        self.set_uri(file, device_name, file.blobs[0].source_path, file.blobs[0].origin_name)
        jewel.id = self.addJewel(jewel)

        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()

            old_file = self.check_if_uri_exists(file, cur)
            ## no uri 
            if old_file is None:
                old_file = self.check_if_hash_exists(file, cur, device_name)
                ##  no uri and no hash on same device
                if old_file is None:
                    self.insert_File(file, cur,conn)
                    self.insert_first_Blob(file,cur,conn)
                    self.addJewelFileAssignment(jewel.id,file.id)
                    conn.close()
                    return True
                # no uri but existing hash
                else:
                    ##find the same hash
                    for blob in old_file.blobs:
                        ## asa blob is same, we need the path to this file
                        if blob.hash == file.blobs[0].hash:
                            self.addJewelFileAssignment(jewel.id, old_file.id)
                            self.protocol_skipped_file(jewel,file,"Version existing in same File","Version Number:" + str(blob.number) + " Blob ID: " + str(blob.id), old_file.id, conn, cur )
                            conn.close()
                            return blob.store_destination
            # uri
            else:
                ##has old_file a blob with same hash?
                for blob in old_file.blobs:
                    ## asa blob is same,  we need the path to this file
                    if blob.hash == file.blobs[0].hash:
                        self.addJewelFileAssignment(jewel.id, old_file.id)
                        self.protocol_skipped_file(jewel,file,"Version existing in same File","Version Number:" + str(blob.number) + " Blob ID: " + str(blob.id), old_file.id, conn, cur )
                        conn.close()
                        return blob.store_destination
                #if no hash exists then add new blob
                self.insert_new_blob_to_existing_file(file,cur,conn,old_file)
                self.addJewelFileAssignment(jewel.id,old_file.id)
                conn.close()
                return True
        else:
            raise ValueError('No Connection to Database')

    def check_if_uri_exists(self, file, cur):
        command = """SELECT * FROM File INNER JOIN Blob on File.ID = Blob.ID_File WHERE File.ID = ?"""
        params = (self._encode_base64(file.id),)
        cur.execute(command, params)
        data = cur.fetchall()

        if len(data) == 0:
            return None

        ##create file from data
        blobs = []
        for row in data:
            blobs.append(Blob(row[2], row[3], row[4], self._decode_base64(row[5]), row[6], row[7], row[8],
                              self._decode_base64(row[9]), self._decode_base64(row[10]), self._decode_base64(row[11]),
                              self._decode_base64(row[12])))
        file = File(self._decode_base64(data[0][0]), blobs, data[0][1])
        return file

    def insert_new_blob_to_existing_file(self, new_file, cur, conn, old_file):
        command = """INSERT INTO Blob
                              (Number, Hash, Name, FileSize, CreationDate, Modify, ID_File, Origin_Name, Source_Path, Store_Destination) 
                              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        #         
        params = (
        old_file.get_last_blob().number + 1, new_file.blobs[0].hash, self._encode_base64(new_file.blobs[0].name),
        new_file.blobs[0].fileSize, new_file.blobs[0].creationDate, new_file.blobs[0].modify,
        self._encode_base64(old_file.id), self._encode_base64(new_file.blobs[0].origin_name),
        self._encode_base64(new_file.blobs[0].source_path), self._encode_base64(new_file.blobs[0].store_destination))
        cur.execute(command, params)
        conn.commit()

    def insert_first_Blob(self, file, cur, conn):
        command = """INSERT INTO Blob
                              (Number, Hash, Name, FileSize, CreationDate, Modify, ID_File, Origin_Name, Source_Path, Store_Destination) 
                              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

        params = (1, file.blobs[0].hash, self._encode_base64(file.blobs[0].name), file.blobs[0].fileSize,
                  file.blobs[0].creationDate, file.blobs[0].modify, self._encode_base64(file.id),
                  self._encode_base64(file.blobs[0].origin_name), self._encode_base64(file.blobs[0].source_path),
                  self._encode_base64(file.blobs[0].store_destination))
        cur.execute(command, params)
        conn.commit()

    def insert_File(self, file, cur, con):
        command = "INSERT INTO FILE (ID, Birth) VALUES (?, ?);"
        params = (self._encode_base64(file.id), file.birth,)
        cur.execute(command, params)
        con.commit()

    def check_if_hash_exists(self, file, cur, device_name):
        command = """SELECT File.ID, File.Birth, Blob.ID, Blob.Number, Blob.Hash, Blob.Name,Blob.FileSize, Blob.CreationDate, Blob.Modify, Blob.ID_File, Blob.Origin_Name, Blob.Source_Path, Blob.Store_Destination  FROM File 
                        INNER JOIN Blob on File.ID = Blob.ID_File
                        INNER JOIN Jewel_File_Assignment on Jewel_File_Assignment.ID_File = File.ID
                        INNER JOIN Jewel on Jewel.ID = Jewel_File_Assignment.ID_Jewel
                        WHERE File.ID =(SELECT ID_File FROM Blob WHERE Blob.Hash = ?)
                        AND Jewel.DeviceName = ?"""
        params = (file.blobs[0].hash, self._encode_base64(device_name))
        cur.execute(command, params)
        data = cur.fetchall()

        if len(data) == 0:
            return None

        ##create file from data
        blobs = []
        for row in data:
            blobs.append(Blob(row[2], row[3], row[4], self._decode_base64(row[5]), row[6], row[7], row[8],
                              self._decode_base64(row[9]), self._decode_base64(row[10]), self._decode_base64(row[11]),
                              self._decode_base64(row[12])))
        file = File(self._decode_base64(data[0][0]), blobs, data[0][1])
        return file

    def addJewel(self, jewel):
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()

            command = "SELECT ID FROM Jewel WHERE JewelSource = ? AND DeviceName = ?"
            data_tuple = (self._encode_base64(jewel.jewelSource), self._encode_base64(jewel.device_name))
            cur.execute(command, data_tuple)
            id = cur.fetchone()

            if id is not None:
                return id[0]
            else:
                command = """INSERT INTO 'Jewel'
                              ('Comment', 'Monitoring_Startdate', 'JewelSource', 'DeviceName', 'FullbackupSource') 
                              VALUES (?, ?, ?, ?, ?);"""
                data_tuple = (
                self._encode_base64(jewel.comment), jewel.monitoring_Startdate, self._encode_base64(jewel.jewelSource),
                self._encode_base64(jewel.device_name),
                self._encode_base64(jewel.fullbackup_source))
                cur.execute(command, data_tuple)
                conn.commit()
                return cur.lastrowid
        conn.close()

    def addJewelFileAssignment(self, id_jewel, id_file):
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            sqlite_insert_with_param = """INSERT INTO 'Jewel_File_Assignment'
                              ('ID_Jewel', 'ID_File') 
                              VALUES (?, ?);"""
            data_tuple = (id_jewel, self._encode_base64(id_file))
            try:
                cur.execute(sqlite_insert_with_param, data_tuple)
                conn.commit()
                conn.close()
            except sqlite3.IntegrityError:
                # sowohl jewel, als auch File existieren bereits in der Kombination in der Datenbank.
                # -> User hat Jewel bereits angelegt, und auch die Datei hat zu dem Zeitpunkt schon existiert.
                conn.close()
                return False

    def check_which_jewel_sources_exist(self, jewel_source_arr, device_name):
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            command = "SELECT JewelSource FROM Jewel WHERE (JewelSource = ? AND DeviceName = ?)"
            command = command + " ".join([" OR (JewelSource = ? AND DeviceName = ?)"] * (len(jewel_source_arr) - 1))

            params = []

            for source in jewel_source_arr:
                params.append(self._encode_base64(source))
                params.append(self._encode_base64(device_name))

            cur.execute(command, params)
            tmp = cur.fetchall()
            conn.close()
            answer = []
            for row in tmp:
                answer.append(self._decode_base64(row[0]))
            return answer

    def get_Jewel_via_id(self, id):
        jewel = None
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            sqlite_insert_with_param = "SELECT * FROM Jewel WHERE ID= ?"
            cur.execute(sqlite_insert_with_param, [id])
            j_tuple = cur.fetchone()
            if j_tuple is not None:
                jewel = Jewel(j_tuple[0], self._decode_base64(j_tuple[1]), j_tuple[2], self._decode_base64(j_tuple[3]),
                              self._decode_base64(j_tuple[4]), self._decode_base64(j_tuple[5]))
            conn.commit()
            conn.close()
        return jewel

    def get_File_via_id(self, id):
        file = None
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            sqlite_insert_with_param = "SELECT * FROM File WHERE ID= ?"
            cur.execute(sqlite_insert_with_param, [self._encode_base64(id)])
            b_tuple = cur.fetchone()
            conn.commit()
            conn.close()
            if b_tuple is not None:
                blobs = self.get_Blobs_via_file_id(self._decode_base64(b_tuple[0]))
                file = File(self._decode_base64(b_tuple[0]), blobs, b_tuple[1])
        return file

    def get_File_via_hash(self, hash):
        file = None
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            sqlite_insert_with_param = """SELECT DISTINCT File.ID, File.Birth 
                                          FROM File, Blob WHERE Blob.Hash = ? AND File.ID = Blob.ID_File"""
            cur.execute(sqlite_insert_with_param, [hash])
            b_tuple = cur.fetchone()
            conn.commit()
            conn.close()
            if b_tuple is not None:
                blobs = self.get_Blobs_via_file_id(self._decode_base64(b_tuple[0]))
                file = File(self._decode_base64(b_tuple[0]), blobs, b_tuple[1])
        return file

    def get_all_Files(self):
        files = []
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            cur.execute("SELECT * FROM File")
            records = cur.fetchall()
            conn.commit()
            conn.close()
            if records is not None:
                for row in records:
                    blobs = self.get_Blobs_via_file_id(self._decode_base64(row[0]))
                    file = File(self._decode_base64(row[0]), blobs, row[1])
                    files.append(file)
        return files

    def get_Files_via_jewel_id(self, jewel_id):
        files = []
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            # Alle Files, die zu einem Jewel gehören, werden aus der Datenbank geholt. 
            sqlite_insert_with_param = """SELECT DISTINCT File.ID, File.Birth
                                          FROM Jewel_File_Assignment, File WHERE Jewel_File_Assignment.ID_Jewel= ? AND Jewel_File_Assignment.ID_File = File.ID"""
            cur.execute(sqlite_insert_with_param, [jewel_id])
            records = cur.fetchall()
            conn.commit()
            conn.close()

            if records is not None:
                for row in records:
                    blobs = self.get_Blobs_via_file_id(self._decode_base64(row[0]))
                    file = File(self._decode_base64(row[0]), blobs, row[1])
                    files.append(file)
        return files

    def get_all_Jewels(self):
        jewels = []
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Jewel")
            records = cur.fetchall()

            if records is not None:
                for row in records:
                    jewel = Jewel(row[0], self._decode_base64(row[1]), row[2], self._decode_base64(row[3]),
                                  self._decode_base64(row[4]), self._decode_base64(row[5]))
                    jewels.append(jewel)

            conn.commit()
            conn.close()
        return jewels

    def get_all_Blobs(self):
        blobs = []
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Blob")
            records = cur.fetchall()

            if records is not None:
                for row in records:
                    blob = Blob(row[0], row[1], row[2], self._decode_base64(row[3]), row[4], row[5], row[6],
                                self._decode_base64(row[7]), self._decode_base64(row[8]), self._decode_base64(row[9]),
                                self._decode_base64(row[10]))
                    blobs.append(blob)

            conn.commit()
            conn.close()
        return blobs

    def get_Blobs_via_file_id(self, file_id):
        blobs = []
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Blob WHERE ID_File= ?", [self._encode_base64(file_id)])
            records = cur.fetchall()

            if records is not None:
                for row in records:
                    blob = Blob(row[0], row[1], row[2], self._decode_base64(row[3]), row[4], row[5], row[6],
                                self._decode_base64(row[7]), self._decode_base64(row[8]), self._decode_base64(row[9]),
                                self._decode_base64(row[10]))
                    blobs.append(blob)

            conn.commit()
            conn.close()
        return blobs

    def get_Blob_via_id(self, id):
        blob = None
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Blob WHERE ID= ?", [id])
            row = cur.fetchone()
            if row is not None:
                blob = Blob(row[0], row[1], row[2], self._decode_base64(row[3]), row[4], row[5], row[6],
                            self._decode_base64(row[7]), self._decode_base64(row[8]), self._decode_base64(row[9]),
                            self._decode_base64(row[10]))
            conn.commit()
            conn.close()

        return blob

    def protocol_skipped_file(self, jewel, file, reason, additional_information, connected_file, conn, cur):
        command = "INSERT INTO Skipped_Files (ID_Jewel, UUID, Occurance_Date, Hash, Reason, Additional_Information, Connected_File_to_Jewel) VALUES (?, ?, ?, ?, ?, ?, ? );"
        params = (jewel.id, self._encode_base64(file.id), datetime.datetime.today(), file.blobs[0].hash, reason,
                  additional_information, self._encode_base64(connected_file))
        cur.execute(command, params)
        conn.commit()

    def get_all_skipped_files(self):
        row = []
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Skipped_Files")
            row = cur.fetchall()
            conn.commit()
            conn.close()
            row[2] = self._decode_base64(row[2])
            row[7] = self._decode_base64(row[7])
        return row

    def get_skipped_file_via_id(self, id):
        row = []
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Skipped_Files WHERE ID= ?", [id])
            row = cur.fetchone()
            conn.commit()
            conn.close()
            row[2] = self._decode_base64(row[2])
            row[7] = self._decode_base64(row[7])
        return row

    def get_fullbackup_paths(self, jewel_source_arr):
        conn = self.create_connection('datenbank.db')
        params = []
        answer = []
        if conn != None:
            cur = conn.cursor()
            command = """SELECT * FROM Jewel WHERE JewelSource = ?"""
            command = command + " ".join([" OR JewelSource = ?"] * (len(jewel_source_arr) - 1))

            for source in jewel_source_arr:
                params.append(self._encode_base64(source))

            cur.execute(command, params)
            tmp = cur.fetchall()
            conn.close()
            for row in tmp:
                answer.append(Jewel(row[0], self._decode_base64(row[1]), row[2], self._decode_base64(row[3]),
                                    self._decode_base64(row[4]), self._decode_base64(row[5])))
            return answer

    def get_restore_Jewel(self, until_date: datetime.datetime, jewel_id: int):
        # the database shall look in every value of this day
        until_date = until_date.replace(hour=23, minute=59, second=59)
        assert (until_date.minute == 59 and until_date.hour == 23 and until_date.second == 59)
        conn = self.create_connection('datenbank.db')
        # temporär, da objekt struktur noch nicht existiert
        files = []
        jewel = None

        if conn != None:
            cur = conn.cursor()
            command = """SELECT Jewel.ID, Jewel.FullbackupSource, Jewel.JewelSource, Blob.ID_File, Max(Blob.Number) as Number,  Blob.Source_Path, Blob.Origin_Name, Blob.Store_Destination FROM File
                        INNER JOIN Blob on File.ID = Blob.ID_File
                        INNER JOIN Jewel_File_Assignment on Jewel_File_Assignment.ID_File = File.ID
                        INNER JOIN Jewel on Jewel.ID = Jewel_File_Assignment.ID_Jewel
                        WHERE Jewel.ID = ?
                        AND Blob.CreationDate <= ?
                        GROUP BY Blob.ID_File;"""
            params = (jewel_id, until_date)
            cur.execute(command, params)
            tmp = cur.fetchall()
            conn.close()

            if tmp:
                for row in tmp:
                    files.append(
                        (self._decode_base64(row[6]), self._decode_base64(row[5]), self._decode_base64(row[7]), row[4]))
                jewel = (row[0], files, self._decode_base64(row[3]))
                return jewel
            else:
                return None

    def get_restore_File(self, until_date: datetime, file_id: str):
        # the database shall look in every value of this day
        until_date = until_date.replace(hour=23, minute=59, second=59)
        assert (until_date.minute == 59 and until_date.hour == 23 and until_date.second == 59)
        conn = self.create_connection('datenbank.db')
        # temporär, da objekt struktur noch nicht existiert
        files = []

        if conn != None:
            cur = conn.cursor()
            command = """SELECT Jewel.ID, Jewel.FullbackupSource, Jewel.JewelSource, Blob.ID_File, Max(Blob.Number) as Number,  Blob.Source_Path, Blob.Origin_Name, Blob.Store_Destination FROM File
                        INNER JOIN Blob on File.ID = Blob.ID_File
                        INNER JOIN Jewel_File_Assignment on Jewel_File_Assignment.ID_File = File.ID
                        INNER JOIN Jewel on Jewel.ID = Jewel_File_Assignment.ID_Jewel
                        WHERE File.ID = ?
                        AND Blob.CreationDate <= ?
                        GROUP BY Blob.ID_File;"""
            params = (self._encode_base64(file_id), until_date)
            cur.execute(command, params)
            row = cur.fetchone()
            conn.close()   
        
            if row:
                files.append(
                    (self._decode_base64(row[6]), self._decode_base64(row[5]), self._decode_base64(row[7]), row[4]))
                jewel = (row[0], files, self._decode_base64(row[3]))
                return jewel
            else:
                return None
