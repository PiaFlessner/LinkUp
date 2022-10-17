from ast import And
import sqlite3
from os.path import exists as file_exists

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

    def __init__(self,id, file_Destination, store_Destination, origin_Name, backups):
        self.id = id
        self.file_Destination = file_Destination
        self.store_Destination =  store_Destination
        self.origin_Name =  origin_Name
        self.backups = backups

    
    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_file_Destination(self):
        return self.file_Destination

    def set_file_Destination(self, file_Destination):
        self.file_Destination = file_Destination
    
    def get_store_Destination(self):
        return self.store_Destination

    def set_store_Destination(self,store_Destination):
        self.store_Destination = store_Destination
    
    def get_origin_Name (self):
        return self.origin_Name

    def set_origin_Name (self,origin_Name):
        self.origin_Name = origin_Name

    def get_backups(self):
        return self.backups

    def set_backups (self,backups):
        self.backups = backups


class BackUp:

    def __init__(self,id, number, hash, name, fileSize, creationDate, birth, change, modify,  iD_File ):
        self.id = id
        self.number = number
        self.hash = hash
        self.name = name
        self.fileSize = fileSize
        self.creationDate = creationDate
        self.birth = birth
        self.change = change
        self.modify = modify
        self.iD_File = iD_File

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

    def get_birth(self):
        self.birth
    
    def set_birth (self,birth):
        self.birth = birth

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

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, self.__class__):
            return self.hash == other.hash
        else:
            return False


class Datenbank:

     def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
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
                                    File_Destination text NOT NULL,
                                    Store_Destination text NOT NULL,
                                    Origin_Name text NOT NULL
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


                cur.execute("""CREATE TABLE BackUp (
                                    ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    Number INTEGER NOT NULL,
                                    Hash TEXT NOT NULL,
                                    Name TEXT NOT NULL,
                                    FileSize INTEGER NOT NULL,
                                    CreationDate NUMERIC,
                                    Birth NUMERIC NOT NULL,
                                    Change NUMERIC,
                                    Modify NUMERIC,
                                    ID_File INTEGER NOT NULL,

                                    constraint file_backup_fk
                                    FOREIGN KEY (ID_File)
                                        REFERENCES File(ID)
                                                   
                                             );""")
  
                conn.commit()
                conn.close()

     def addToDataBase(self, jewel, file):
        jewel_id = self.addJewel(jewel)
        file1_id = self.addFile(file)
        self.addJewelFileAssignment(jewel_id,file1_id)
        self.addBackUp(file)

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

     def addFile(self, file):
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()

            
            #Insert File, if not Existed
            sqlite_insert_with_param = """INSERT INTO File
                              (File_Destination, Store_Destination, Origin_Name) 
                              SELECT ?, ?, ?
                              WHERE NOT EXISTS(SELECT 1 FROM File WHERE File_Destination = ? AND Origin_Name = ?);
                              """
            data_tuple = (file.file_Destination,file.store_Destination, file.origin_Name, file.file_Destination, file.origin_Name)
                          
            cur.execute(sqlite_insert_with_param, data_tuple)
            conn.commit()
            ##get the ID of the inserted File. Extra Statement is Necessary, since "last inserted" does not work when inserts where ignored
            command = "SELECT ID FROM File WHERE File_Destination = ? AND Origin_Name = ? AND Store_Destination = ?;"
            data_tuple =(file.file_Destination, file.origin_Name, file.store_Destination )
            cur.execute(command, data_tuple)
            conn.commit()
            id = cur.fetchone()

            conn.close()
            if id is not None:
                return id[0]
            else:
                return 0
            

     def addBackUp(self, file):
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()    
            #gibt es schon backups
            command = """SELECT * FROM BackUp WHERE
                                  ID_File = ?
                                  ORDER BY Number DESC;"""
            data_tuple = (file.backups[0].iD_File, )
            cur.execute(command, data_tuple)
            last_backup = cur.fetchone();
            conn.commit()

            ###nummer des letzten backups holen
            #wenn das letzte backUp nicht leer ist, dann gucken ob es schon drin steht.
            if last_backup is not None:
                last_backup_number =  last_backup[1]
                backup = BackUp(last_backup[0], last_backup[1], last_backup[2], last_backup[3],last_backup[4],last_backup[5],last_backup[6],last_backup[7],last_backup[8],last_backup[9])
                
                ##wenn das "neue" backUp schon in der Datenbank steht, dann nichts machen
                if backup == (file.backups[0]):
                    pass
                else:
                    #Wenn nicht, dann bitte einfügen aber mit erhöhter Versionsnummer
                    command = """INSERT INTO Backup
                              (Number, Hash, Name, FileSize, CreationDate, Birth, Change, Modify, ID_File) 
                              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);"""
                    data_tuple = (last_backup_number+1, file.backups[0].hash, file.backups[0].name , file.backups[0].fileSize, file.backups[0].creationDate,  file.backups[0].birth, file.backups[0].change, file.backups[0].modify, file.backups[0].iD_File )
                    cur.execute(command, data_tuple)
                    conn.commit()
            #Ansonsten wurde die Datei das erste mal gebackuped, und muss auf alle Fälle eingefügt werden.
            else:
                command = """INSERT INTO Backup
                              (Number, Hash, Name, FileSize, CreationDate, Birth, Change, Modify, ID_File) 
                              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);"""
                    
                data_tuple = (1, file.backups[0].hash, file.backups[0].name , file.backups[0].fileSize, file.backups[0].creationDate,  file.backups[0].birth, file.backups[0].change, file.backups[0].modify, file.backups[0].iD_File )
                cur.execute(command, data_tuple)
                conn.commit()
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


    
     def updateJewel(self,jewel):
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            sqlite_insert_with_param = """UPDATE 'Jewel'
                                        SET 'Comment' = ?,
                                            'Monitoring_Startdate' = ?,
                                            'JewelSource' = ?
                                        WHERE ID = ?;"""
            data_tuple = (jewel.comment, jewel.monitoring_Startdate,jewel.jewelSource, jewel.id)
            cur.execute(sqlite_insert_with_param, data_tuple)

           
            conn.commit()
            conn.close()

     def updatefile(self,file):
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            sqlite_insert_with_param = """UPDATE 'File'
                                        SET 'File_Destination' = ?,
                                            'Store_Destination' = ?,
                                            'Origin_Name' = ?
                                        WHERE ID = ?;"""
            data_tuple = (file.file_Destination,file.store_Destination, file.origin_Name, file.id)
            cur.execute(sqlite_insert_with_param, data_tuple)

           
            conn.commit()
            conn.close()

     def updateBackUp(self,backup):
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys=OFF;")
            sqlite_insert_with_param = """
                                        UPDATE 'BackUp'
                                        SET 'Number' = ?,
                                            'Hash' = ?,
                                            'Name' = ?,
                                            'FileSize' = ?,
                                            'CreationDate' = ?,
                                            'Checksum' = ?,
                                            'Birth' = ?,
                                            'Change' = ?,
                                            'Modify' = ?,
                                            'ID_File' = ?
                                        WHERE ID = ?;"""
            data_tuple =  (backup.number, backup.hash, backup.name , backup.fileSize, backup.creationDate, backup.checksum,  backup.birth, backup.change, backup.modify, backup.iD_File, backup.id)
            cur.execute(sqlite_insert_with_param, data_tuple)
            cur.execute("PRAGMA foreign_keys=ON;")                               
           
            conn.commit()
            conn.close()


     def getJewel(self,id):
        jewel = None
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            sqlite_insert_with_param = "SELECT * FROM Jewel WHERE ID= ?"
            cur.execute( sqlite_insert_with_param, id)
            j_tuple = cur.fetchone()
            jewel = Jewel(j_tuple[0], j_tuple[1], j_tuple[2], j_tuple[3])
            conn.commit()
            conn.close()
        return jewel

     def getFile(self,id):
        file = None
        conn = self.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            sqlite_insert_with_param = "SELECT * FROM File WHERE ID= ?"
            cur.execute( sqlite_insert_with_param, id)
            b_tuple = cur.fetchone()
            file = File(b_tuple[0], b_tuple[1], b_tuple[2], b_tuple[3])
            conn.commit()
            conn.close()
        return file

            

