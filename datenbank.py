from ast import And
import itertools
import sqlite3
from os.path import exists as file_exists
from unicodedata import numeric

class Jewel:

    def __init__(self,id,comment, monitoring_Startdate, jewelSource):
        self.id = id
        self.comment = comment
        self.monitoring_Startdate = monitoring_Startdate
        self.jewelSource = jewelSource

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_comment(self):
        return self.comment

    def set_comment(self, comment):
        self.comment = comment

    def get_monitoring_Startdate(self):
        return self.monitoring_Startdate

    def set_monitoring_Startdate(self, monitoring_Startdate):
        self.monitoring_Startdate = monitoring_Startdate

    def get_jewelSource(self):
        return self.jewelSource

    def set_jewelSource(self, jewelSource):
        self.jewelSource = jewelSource



class File:

    def __init__(self,id, blobs, birth):
        self.id = id
        self.blobs = blobs
        self.birth = birth

    
    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_blobs(self):
        return self.blobs

    def set_blobs (self,blobs):
        self.blobs = blobs

    def get_birth(self):
        return self.birth

    def set_birth (self,birth):
        self.birth = birth

    def get_last_blob(self):
        return self.blobs[len(self.blobs)-1]

class Blob:

    def __init__(self,id, number, hash, name, fileSize, creationDate, change, modify,  iD_File, origin_name, source_path, store_destination ):
        self.id = id
        self.number = number
        self.hash = hash
        self.name = name
        self.fileSize = fileSize
        self.creationDate = creationDate
        self.change = change
        self.modify = modify
        self.iD_File = iD_File
        self.origin_name = origin_name
        self.store_destination = store_destination
        self.source_path = source_path

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_number(self):
        return self.number

    def set_number(self, number):
        self.number = number

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_fileSize(self):
        return self.fileSize

    def set_fileSize(self, fileSize):
        self.fileSize = fileSize

    def get_creationDate(self):
        return self.creationDate

    def set_creationDate(self, creationDate):
        self.creationDate = creationDate

    def get_change(self):
        return self.change

    def set_change(self, change):
        self.change = change

    def get_modify(self):
        return self.modify

    def set_modify(self, modify):
        self.modify = modify

    def get_iD_File(self):
        return self.iD_File

    def set_iD_File(self,iD_File):
        self.iD_File = iD_File

    def get_origin_name(self):
        return self.origin_name

    def set_origin_name(self,origin_name):
        self.origin_name = origin_name

    def get_source_path(self):
        return self.source_path

    def set_source_path(self,source_path):
        self.source_path = source_path

    def get_store_destination(self):
        return self.store_destination

    def set_store_destination(self,store_destination):
        self.store_destination = store_destination
    

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, self.__class__):
            return str(self.hash) == str(other.hash) and self.modify == other.modify and self.change == other.change and str(self.store_destination) == str(other.store_destination) and str(self.origin_name) == str(other.origin_name) and str(self.source_path) == str(other.source_path)
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
                                    JewelSource TEXT NOT NULL
                                                 );""")

                cur.execute("""CREATE TABLE File (
                                    ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
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
                                    Origin_Name TEXT NOT NULL,
                                    Source_Path TEXT NOT NULL,
                                    Store_Destination TEXT NOT NULL,
                                    Change TIMESTAMP,
                                    Modify TIMESTAMP,
                                    ID_File INTEGER NOT NULL,

                                    constraint file_blob_fk
                                    FOREIGN KEY (ID_File)
                                        REFERENCES File(ID)
                                                   
                                             );""")
  
                conn.commit()
                conn.close()

     def addToDataBase(self, jewel, file):
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            jewel.id = self.addJewel(jewel)
            old_file = self.checkIfHashExists(file, cur)
            
            #if hash does not exists in db
            if old_file is None:
                originNameFiles = self.checkIfOriginNameExists(file, cur)

                #does origin name exists
                ##disclaimer: As soon as the user inserts a file with a unkown hash AND unkown origin Name, the application
                ##sees this as a new File!
                if originNameFiles is None:
                    file.id = self.insert_File(file, cur,conn)
                    self.insert_first_Blob(file,cur,conn)
                    self.addJewelFileAssignment(jewel.id,file.id)
                    return True

                else:
                    #######################is it really this file?
                    #####TODO what if there are more files with same origin name and same birth
                    #####current solution: just insert for every file (wtf)
                    for element in originNameFiles:
                        #check if birth is the same, so then it will be **most likely*** be the same file, 
                        #meaning it could be inserted
                        if str(file.birth) == str(element.birth):
                            self.insert_new_blob_to_existing_file(file,cur,conn,element)
                            self.addJewelFileAssignment(jewel.id,element.id)
                            return True
                    return False

            #if hash is existing, just find out, if something has changed
            else:
                for blob in old_file.blobs:
                    ## as soon as there is the same blob, the new blob does not needed to be inserted
                    ##because its already existing
                    if blob == file.blobs[0]:
                        self.addJewelFileAssignment(jewel.id,old_file.id)
                        return False
                    
                self.insert_new_blob_to_existing_file(file,cur,conn,old_file)
                self.addJewelFileAssignment(jewel.id,old_file.id)
                return True
        return False


     def insert_new_blob_to_existing_file(self,new_file,cur,conn,old_file):
        command = """INSERT INTO Blob
                              (Number, Hash, Name, FileSize, CreationDate, Change, Modify, ID_File, Origin_Name, Source_Path, Store_Destination) 
                              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        #         
        params = (old_file.get_last_blob().number+1, new_file.blobs[0].hash,new_file.blobs[0].name , new_file.blobs[0].fileSize, new_file.blobs[0].creationDate, new_file.blobs[0].change, new_file.blobs[0].modify, old_file.id, new_file.blobs[0].origin_name, new_file.blobs[0].source_path, new_file.blobs[0].store_destination)
        cur.execute(command, params)
        conn.commit()

     def insert_first_Blob(self,file,cur,conn):
        command = """INSERT INTO Blob
                              (Number, Hash, Name, FileSize, CreationDate, Change, Modify, ID_File, Origin_Name, Source_Path, Store_Destination) 
                              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
                    
        params = (1, file.blobs[0].hash, file.blobs[0].name , file.blobs[0].fileSize, file.blobs[0].creationDate, file.blobs[0].change, file.blobs[0].modify, file.id, file.blobs[0].origin_name, file.blobs[0].source_path, file.blobs[0].store_destination)
        cur.execute(command, params)
        conn.commit()

     def insert_File(self,file,cur,con):
        command = "INSERT INTO FILE (Birth) VALUES (?);"
        params = (file.birth,)
        cur.execute(command,params)
        fileID = cur.lastrowid
        con.commit()
        return fileID

    #Returns Array with Jewels with the same origin name as file
     def checkIfOriginNameExists(self,file, cur):
        command = "SELECT ID_File FROM Blob WHERE Origin_Name = ?"
        params = (file.blobs[0].origin_name,)
        cur.execute(command,params)
        ids = cur.fetchall()

        if len(ids) == 0:
            return None

        command = "SELECT * FROM File INNER JOIN Blob ON File.ID = Blob.ID_File WHERE File.ID = ?"
        command = command + " ".join(list(itertools.repeat("OR FILE.ID = ?",len(ids)-1)))
        
        cur.execute(command,ids[0])
        data = cur.fetchall()

        if data is None:
            return None
        
        oldFileID = data[0][13]
        files = []
        blobs = []

        # go through data and translate it to file array
        for row in data:
            #if file has changed, add file to answer and reset params
            if oldFileID != row[13]:
                files.append((File(row[0],blobs,row[1])))
                blobs = []
                oldFileID = row[13]
            blobs.append(Blob(row[2], row[3],row[4], row[5], row[6], row[7],row[11], row[12],row[13], row[8], row[9],row[10]))
        files.append((File(row[0],blobs,row[1])))

        return files
            
     def checkIfHashExists(self,file, cur):
        command = """SELECT * FROM File INNER JOIN Blob on File.ID = Blob.ID_File WHERE File.ID =(SELECT ID_File FROM Blob WHERE Blob.Hash = ?)"""
        params = (file.blobs[0].hash,)
        cur.execute(command, params)
        data = cur.fetchall()

        if len(data) == 0:
            return None

        ##create file from data
        blobs = []
        for row in data:
            blobs.append(Blob(row[2], row[3],row[4], row[5], row[6], row[7],row[11], row[12],row[13], row[8], row[9],row[10]))
        file = File(data[0][0],blobs,data[0][1])
        return file

     def addJewel(self,jewel):
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()

            command= "SELECT ID FROM Jewel WHERE JewelSource = ?"
            data_tuple = (jewel.jewelSource,)
            cur.execute(command, data_tuple)
            id = cur.fetchone()

            if id is not None:
                return id[0]
            else:
                command = """INSERT INTO 'Jewel'
                              ('Comment', 'Monitoring_Startdate', 'JewelSource') 
                              VALUES (?, ?, ?);"""
                data_tuple = (jewel.comment, jewel.monitoring_Startdate,jewel.jewelSource )
                cur.execute(command, data_tuple)  
                conn.commit()
                return cur.lastrowid
        conn.close()

     def addJewelFileAssignment (self, id_jewel, id_file):
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            sqlite_insert_with_param = """INSERT INTO 'Jewel_File_Assignment'
                              ('ID_Jewel', 'ID_File') 
                              VALUES (?, ?);"""
            data_tuple = (id_jewel, id_file)
            try:
                cur.execute(sqlite_insert_with_param, data_tuple)
                conn.commit()
            except sqlite3.IntegrityError:
                #sowohl jewel, als auch File existieren bereits in der Kombination in der Datenbank.
                # -> User hat Jewel bereits angelegt, und auch die Datei hat zu dem Zeitpunkt schon existiert.
                return False
            conn.close()


 
     def get_Jewel_via_id(self,id):
        jewel = None
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            sqlite_insert_with_param = "SELECT * FROM Jewel WHERE ID= ?"
            cur.execute( sqlite_insert_with_param, [id])
            j_tuple = cur.fetchone()
            if j_tuple is not None:
              jewel = Jewel(j_tuple[0], j_tuple[1], j_tuple[2], j_tuple[3])
            conn.commit()
            conn.close()
        return jewel



     def get_File_via_id(self,id):
        file = None
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            sqlite_insert_with_param = "SELECT * FROM File WHERE ID= ?"
            cur.execute( sqlite_insert_with_param, [id])
            b_tuple = cur.fetchone()
            conn.commit()
            conn.close()
            if b_tuple is not None:
               blobs = self.get_Blobs_via_file_id(b_tuple[0])
               file = File(b_tuple[0], blobs, b_tuple[1])
        return file

   
     def get_File_via_hash(self,hash):
        file = None
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            sqlite_insert_with_param = """SELECT DISTINCT File.ID, File.Birth 
                                          FROM File, Blob WHERE Blob.Hash = ? AND File.ID = Blob.ID_File"""
            cur.execute( sqlite_insert_with_param, [hash])
            b_tuple = cur.fetchone()
            conn.commit()
            conn.close()
            if b_tuple is not None:
               blobs = self.get_Blobs_via_file_id(b_tuple[0])
               file = File(b_tuple[0], blobs, b_tuple[1])
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
                    blobs = self.get_Blobs_via_file_id(row[0])
                    file = File(row[0], blobs, row[1])
                    files.append(file)          
        return files
    

     def get_Files_via_jewel_id(self,jewel_id):
        files = []
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            # Alle Files, die zu einem Jewel gehören, werden aus der Datenbank geholt. 
            sqlite_insert_with_param = """SELECT DISTINCT File.ID, File.Birth
                                          FROM Jewel_File_Assignment, File WHERE Jewel_File_Assignment.ID_Jewel= ? AND Jewel_File_Assignment.ID_File = File.ID"""
            cur.execute( sqlite_insert_with_param, [jewel_id])
            records = cur.fetchall()
            conn.commit()
            conn.close()

            if records is not None:
                for row in records:
                   blobs = self.get_Blobs_via_file_id(row[0])
                   file = File(row[0], blobs, row[1])
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
                    jewel =  Jewel(row[0], row[1], row[2], row[3])
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
                    blob = Blob(row[0], row[1], row[2], row[3],row[4],row[5], row[6], row[7], row[8], row[9], row[10], row [11])
                    blobs.append(blob)
            
            conn.commit()
            conn.close()
        return blobs

 
     def get_Blobs_via_file_id(self, file_id):
        blobs = []
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            cur.execute("SELECT * FROM Blob WHERE ID_File= ?", [file_id])
            records = cur.fetchall()

            if records is not None:
                for row in records:
                   blob = Blob(row[0], row[1], row[2], row[3],row[4],row[5], row[6], row[7], row[8], row[9], row[10], row[11])
                   blobs.append(blob)
            
            conn.commit()
            conn.close()
        return blobs
            

