from ast import And
import itertools
from operator import attrgetter
import sqlite3
from os.path import exists as file_exists
import time
from unicodedata import numeric
import uuid
import base64
import datetime
import platform
from hardlink_info import HardlinkInfo
from resFile import resFile
from resJewel import resJewel
from info_handler import get_json_info
import datetime


class Jewel:
    """Class Jewel. Contains many Files
    
    A Jewel is a starting point of a backup. All Files which are in the Jewel will be also be backupped
    
    """

    def __init__(self, id:int, comment:str|None, monitoring_Startdate:datetime.date, jewelSource:str, device_name:str, fullbackup_source:str) -> "Jewel":
        """Constructor

        Args:
            id (int): Database id of Jewel
            comment (str | None): comment to the Jewel
            monitoring_Startdate (datetime.date): date, when Jewel was inserted in database
            jewelSource (str): Path to the actual Jewel
            device_name (str): name of the device, where jewel is found
            fullbackup_source (str): path where the fullbackup of Jewel is located

        Returns:
            Jewel: Instance of Jewel
        """
        self.id = id
        self.comment = comment
        self.monitoring_Startdate = monitoring_Startdate
        self.jewelSource = jewelSource
        self.device_name = device_name
        self.fullbackup_source = fullbackup_source


class File:
    """Class File Contains many Blobs

    A File contains mainly the blobs to a File. One File can contain many Blobs.
    The is_hardlink property is set to True, if the File was a Hardlink in the past or is a hardlink in the present."""
    def __init__(self, id:str, blobs:list("Blob"), birth:datetime.datetime, is_hardlink:bool = False)->"File":
        """Constructor

        Args:
            id (str): DB ID of FIle
            blobs (list): Blobs(Versions) of File
            birth (datetime.datetime): Date when actual File were created
            is_hardlink (bool, optional): States if File was or is an Hardlink. Defaults to False.

        Returns:
        File: Instance of File
        """
        self.id = id
        self.blobs = blobs
        self.birth = birth
        self.is_hardlink = is_hardlink

    def get_last_blob(self) -> "Blob":#
        """Returns the Blob with the highes Version Number"""
        last_blob = max(self.blobs, key=attrgetter('number'))
        return last_blob


class Blob:
    """Blob Class which represents the Blob (Versions) of a whole File
    
    A Blob contains the main infos to a File Version. Such as Hash, number origin_name etc."""
    

    def __init__(self, id:int, number:int, hash:str, name:str, fileSize:numeric, creationDate:datetime, modify:datetime.datetime, iD_File:str, origin_name:str, source_path:str,
                 store_destination:str, reed_solomon_path:str = None)->"Blob":
        """Constructor

        Args:
            id (int): Database ID
            number (int): Version number
            hash (str): Hash
            name (str): alternative name of file
            fileSize (numeric): size of the file in bytes
            creationDate (datetime): insert date of this specific blob
            modify (datetime.datetime): date, when file was last modified
            iD_File (str): Reference to a File ID
            origin_name (str): the actual name of the file
            source_path (str): Path to where the actual File is located
            store_destination (str): Path to where the backup file is located
            reed_solomon_path (str): Path to possible Reed Solomon File Default=None

        Returns:
            Blob: Instance of Blob
        """
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
        self.reed_solomon_path = str(reed_solomon_path)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, self.__class__):
            return str(self.hash) == str(other.hash) and self.modify == other.modify and str(
                self.store_destination) == str(other.store_destination) and str(self.origin_name) == str(
                other.origin_name) and str(self.source_path) == str(other.source_path)
        else:
            return False

    def __iter__(self):
        return self


class Datenbank:

    device_name = platform.node()

    def create_connection(self, db_file:str) -> sqlite3.Connection:
        """Create Connection to db

        Args:
            db_file (str): Takes location of DB

        Returns:
            sqlite3.Connection: Connection to DB
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        except sqlite3.Error as e:
            print("sqlite_error!: ",e)

        return conn

    def __init__(self, testcase=False):
        if (testcase):
            self.device_name = "testCases"
        self.config = get_json_info(self.device_name)
        self.database_path = self.config['destination'][self.device_name] + '/datenbank.db'
        # Datenbank.create_connection = classmethod(Datenbank.create_connection)
        if not file_exists(self.database_path):
            conn = self.create_connection(self.database_path)
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
                                    Reed_Solomon_Path TEXT,
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

                cur.execute("""CREATE TABLE "Hardlinks" (
                                "ID_File" TEXT NOT NULL,
	                            "ID_Blob"	INTEGER NOT NULL,
	                            "destination_path"	TEXT NOT NULL,
                                "source_path" TEXT NOT NULL,
	                            "insert_date"	TIMESTAMP NOT NULL,
                                "origin_name" TEXT NOT NULL,
	                            PRIMARY KEY("ID_Blob", "ID_File"),
	                            FOREIGN KEY("ID_Blob") REFERENCES "Blob"("ID")

                            );""")

                # Number, Hash, Name, FileSize, CreationDate, Modify, ID_File, Origin_Name, Source_Path, Store_Destination

                conn.commit()
                conn.close()

    def _encode_base64(self, name:str) -> str:
        name = str(name)
        name_bytes = bytes(name, 'UTF-8')
        return base64.b64encode(name_bytes).decode("UTF-8")

    def _decode_base64(self, name:str)-> str:
        name = str(name)
        name_bytes = bytes(name, 'UTF-8')
        return base64.b64decode(name_bytes).decode("UTF-8")

    def set_uri(self, file:"File", device_name:str, file_path:str, file_name:str)-> str:
        # uri = uuid.uuid3(uuid.NAMESPACE_OID, device_name + file_path + file_name)
        uri = device_name + file_path
        file.id = uri
        return uri


    def add_to_database(self, jewel:"Jewel", file:"File", device_name:str)-> Blob | bool:
        """Function which handles the insertion from files and jewels to the database

        Args:
            jewel (Jewel): Jewel which should be inserted
            file (File): File which should be inserted
            device_name (str): name of the current device

        Raises:
            ValueError: No DB Connection

        Returns:
            Blob | bool: Blob -> Blob which should be a Hardlink | Bool -> True means, no further steps needed after Insertion
        """
        self.set_uri(file, device_name, file.blobs[0].source_path, file.blobs[0].origin_name)
        jewel.id = self.addJewel(jewel)

        conn = self.create_connection(self.database_path)
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
                    #find the same hash
                    ##asa blob is same, we need the path to this file
                    same_blob = next((blob for blob in old_file.blobs if blob.hash == file.blobs[0].hash), None)
                    if same_blob != None:
                        self.protocol_skipped_file(jewel,file,"Version existing in same File","Version Number:" + str(same_blob.number) + " Blob ID: " + str(same_blob.id), old_file.id, conn, cur )
                        conn.close()
                        return [same_blob, old_file.is_hardlink]
            # uri
            else:
                ##has old_file a blob with same hash?
                ##asa blob is same,  we need the blob to this file
                same_blob = next((blob for blob in old_file.blobs if blob.hash == file.blobs[0].hash), None)                
                if same_blob != None:
                    self.protocol_skipped_file(jewel,file,"Version existing in same File","Version Number:" + str(same_blob.number) + " Blob ID: " + str(same_blob.id), old_file.id, conn, cur )
                    conn.close()
                    return [same_blob, old_file.is_hardlink]

                #if no hash exists then add new blob
                self.insert_new_blob_to_existing_file(file,cur,conn,old_file)
                self.addJewelFileAssignment(jewel.id,old_file.id)
                conn.close()
                return True
        else:
            raise ValueError('No Connection to Database')


    def check_if_uri_exists(self, file:"File", cur:sqlite3.Cursor)-> File | None:    
        """Looks into database and checks, if any record with same Uri exists
        
        Args:
            file (File): File which should be checked
            cur (sqlite3.Cursor): cursor of DB connection
            
        Returns:
            File | None: File with same URI or None when URI not existing in DB"""

        is_hardlink = False
        command = """SELECT * FROM File INNER JOIN Blob on File.ID = Blob.ID_File WHERE File.ID = ? ORDER BY Blob.Number ASC;"""
        params = (self._encode_base64(file.id),)
        cur.execute(command, params)
        data = cur.fetchall()
        choosed_data = data

        ## maybe there is also an hardlink existing
        command = """select File.ID, File.Birth, Blob.ID, Blob.Number, Blob.Hash, Blob.name, Blob.FileSize, Hardlinks.insert_date, Blob.Modify, Blob.ID_File, Hardlinks.origin_name, Hardlinks.source_path, Hardlinks.destination_path, Blob.Reed_Solomon_Path from File INNER JOIN Hardlinks on File.ID = Hardlinks.ID_File INNER JOIN Blob on Hardlinks.ID_Blob = Blob.ID
                         WHERE File.ID = ? ORDER BY Blob.Number ASC;"""
        cur.execute(command,params)
        data_hardlink = cur.fetchall()

    ##note, if blob was or is a hardlink
        if len(data_hardlink)!=0:
            is_hardlink = True
            if len(data) != 0:
                choosed_data = data
            else:
                choosed_data = data_hardlink
        elif len(data) == 0:
            return None

        blobs_files = self.create_Blob_List_from_db_input(data,2,3,4,5,6,7,8,9,10,11,12,13)
        blobs_hardlink = self.create_Blob_List_from_db_input(data_hardlink,2,3,4,5,6,7,8,9,10,11,12,13)

        blobs = blobs_files + blobs_hardlink       
        file = File(self._decode_base64(choosed_data[0][0]), blobs, choosed_data[0][1], is_hardlink)
        return file

    def insert_new_blob_to_existing_file(self, new_file:File, cur:sqlite3.Cursor, conn:sqlite3.Connection, old_file:File) -> None:
        """Insert a new Blob to an existing File in DB

        Args:
            new_file (File): File which should be inserted.
            cur (sqlite3.Cursor): cursor of DB.
            conn (sqlite3.Connection): Connection of DB.
            old_file (File): the file, to which the new fil(blob) should be appended"""

        command = """INSERT INTO Blob
                              (Number, Hash, Name, FileSize, CreationDate, Modify, ID_File, Origin_Name, Source_Path, Store_Destination, Reed_Solomon_Path) 
                              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
          
        params = (
        old_file.get_last_blob().number + 1, new_file.blobs[0].hash, self._encode_base64(new_file.blobs[0].name),
        new_file.blobs[0].fileSize, new_file.blobs[0].creationDate, new_file.blobs[0].modify,
        self._encode_base64(old_file.id), self._encode_base64(new_file.blobs[0].origin_name),
        self._encode_base64(new_file.blobs[0].source_path), self._encode_base64(new_file.blobs[0].store_destination), self._encode_base64(new_file.blobs[0].reed_solomon_path))
        cur.execute(command, params)
        conn.commit()

    def insert_first_Blob(self, file:File, cur: sqlite3.Cursor, conn:sqlite3.Connection) -> None:
        """Insert the first Blob to a File with no Blobs in DB
        
        Args:
            file (File): File which should be inserted.
            cur (sqlite3.Cursor): cursor of DB.
            conn (sqlite3.Connection): Connection of DB.
        """

        command = """INSERT INTO Blob
                              (Number, Hash, Name, FileSize, CreationDate, Modify, ID_File, Origin_Name, Source_Path, Store_Destination, Reed_Solomon_Path) 
                              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

        params = (1, file.blobs[0].hash, self._encode_base64(file.blobs[0].name), file.blobs[0].fileSize,
                  file.blobs[0].creationDate, file.blobs[0].modify, self._encode_base64(file.id),
                  self._encode_base64(file.blobs[0].origin_name), self._encode_base64(file.blobs[0].source_path),
                  self._encode_base64(file.blobs[0].store_destination), self._encode_base64(file.blobs[0].reed_solomon_path))
        cur.execute(command, params)
        conn.commit()

    def insert_File(self, file: File, cur: sqlite3.Cursor, con:sqlite3.Connection)-> None:
        """Insert a File to DB
        
        Args:
            file (File): File which should be inserted.
            cur (sqlite3.Cursor): cursor of DB.
            con (sqlite3.Connection): Connection of DB.
        """

        command = "INSERT INTO FILE (ID, Birth) VALUES (?, ?);"
        params = (self._encode_base64(file.id), file.birth,)
        cur.execute(command, params)
        con.commit()

    def check_if_hash_exists(self, file:File, cur:sqlite3.Cursor, device_name:str) -> File | None:
        """Checks if a hash of a file is alredy existing in db
        
        Args:
            file (File): File which contains the named hash.
            cur (sqlite3.Cursor): cursor of DB.
            conn (sqlite3.Connection): Connection of DB.
            device_name (str): tname of the current device
        """

        command = """SELECT File.ID, File.Birth, Blob.ID, Blob.Number, Blob.Hash, Blob.Name,Blob.FileSize, Blob.CreationDate, Blob.Modify, Blob.ID_File, Blob.Origin_Name, Blob.Source_Path, Blob.Store_Destination, Blob.Reed_Solomon_Path FROM File 
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

        blobs = self.create_Blob_List_from_db_input(data,2,3,4,5,6,7,8,9,10,11,12,13)
        file = File(self._decode_base64(data[0][0]), blobs, data[0][1])
        return file

    def addJewel(self, jewel:Jewel)-> int:
        """adds a JEwel if the Jewel is not existing yet
        
        Args:
            jewel (Jewel): the Jewel which should be inserted
        Returns:
            int : id of Jewel
        """
        conn = self.create_connection(self.database_path)
        if conn != None:
            cur = conn.cursor()
            # check if the jewel already exists in the database
            command = "SELECT ID FROM Jewel WHERE JewelSource = ? AND DeviceName = ?"
            data_tuple = (self._encode_base64(jewel.jewelSource), self._encode_base64(jewel.device_name))
            cur.execute(command, data_tuple)
            id = cur.fetchone()

            if id is not None: #if it exists, return the id
                return id[0]
            else: #else add it to the database
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

    def addJewelFileAssignment(self, id_jewel:int, id_file:str)-> None | bool:
        """Connects a file with a Jewel
        
        Args:
            id_jewel (int): id of jewel which should be connected to a file
            id_file (str): id of file which should be connected to a jewel

        Returns:
            None | bool: False means something went wrong, None means everything is finde"""
        conn = self.create_connection(self.database_path)
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

    def check_which_jewel_sources_exist(self, jewel_source_arr: list[str], device_name:str)-> list[str]:
        """searches for the jewel sources in db

        Args:
            jewel_source_arr (list[str]): sources which should be checked
            device_name (str): name of the current device

        Returns:
            list[str]: all sources which are already existing in db
        """
        command = "SELECT JewelSource FROM Jewel WHERE (JewelSource = ? AND DeviceName = ?)"
        command = command + " ".join([" OR (JewelSource = ? AND DeviceName = ?)"] * (len(jewel_source_arr) - 1))

        params = []

        #append the params of the array to the params
        for source in jewel_source_arr:
            params.append(self._encode_base64(source))
            params.append(self._encode_base64(device_name))

        data = self.execute_db_command_fetchall(command,params)

        answer = []
        answer = [self._decode_base64(row[0]) for row in data]
        return answer

    def get_Jewel_via_id(self, id:int)-> Jewel:
        jewel = None
        sqlite_insert_with_param = "SELECT * FROM Jewel WHERE ID= ? Limit 1"
        data = self.execute_db_command_fetchall(sqlite_insert_with_param, [id])
        if len(data) > 0:
            jewel = Jewel(data[0][0], self._decode_base64(data[0][1]), data[0][2], self._decode_base64(data[0][3]),
                        self._decode_base64(data[0][4]), self._decode_base64(data[0][5]))
        return jewel

    def get_File_via_id(self, id:str)-> File:
        file = None
        sqlite_insert_with_param = "SELECT * FROM File WHERE ID= ? Limit 1"
        data = self.execute_db_command_fetchall(sqlite_insert_with_param, [self._encode_base64(id)])
        if len(data) > 0:
            blobs = self.get_Blobs_via_file_id(self._decode_base64(data[0][0]))
            file = File(self._decode_base64(data[0][0]), blobs, data[0][1])
        return file

    def get_File_via_hash(self, hash:str)-> File:
        file = None
        sqlite_insert_with_param = """SELECT DISTINCT File.ID, File.Birth 
                                      FROM File, Blob WHERE Blob.Hash = ? AND File.ID = Blob.ID_File Limit 1"""
        data = self.execute_db_command_fetchall(sqlite_insert_with_param,[hash])

        if len(data) > 0:
                blobs = self.get_Blobs_via_file_id(self._decode_base64(data[0][0]))
                file = File(self._decode_base64(data[0][0]), blobs, data[0][1])
        return file


    def get_all_Files(self)-> list[File]:
        files = []
        command = "SELECT * FROM File"
        records = self.execute_db_command_fetchall(command)

        if len(records) > 0:
            for row in records:
                blobs = self.get_Blobs_via_file_id(self._decode_base64(row[0]))
                file = File(self._decode_base64(row[0]), blobs, row[1])
                files.append(file)
        return files

    def get_Files_via_jewel_id(self, jewel_id:int)-> list[File]:
        files = []
        sqlite_insert_with_param = """SELECT DISTINCT File.ID, File.Birth
                                          FROM Jewel_File_Assignment, File WHERE Jewel_File_Assignment.ID_Jewel= ? AND Jewel_File_Assignment.ID_File = File.ID"""
        records = self.execute_db_command_fetchall(sqlite_insert_with_param, [jewel_id])

        if len(records) > 0:
                for row in records:
                    blobs = self.get_Blobs_via_file_id(self._decode_base64(row[0]))
                    file = File(self._decode_base64(row[0]), blobs, row[1])
                    files.append(file)
        return files

    def get_all_Jewels(self)->list[Jewel]:
        records = self.execute_db_command_fetchall("SELECT * FROM Jewel")
        if len(records) > 0:
            jewels = [Jewel(row[0], self._decode_base64(row[1]), row[2], self._decode_base64(row[3]),
                      self._decode_base64(row[4]), self._decode_base64(row[5]))for row in records]
        return jewels
 

    def get_all_Blobs(self)-> list[Blob]:
        blobs = []
        records = self.execute_db_command_fetchall("SELECT * FROM Blob")
        if len(records)>0:
            blobs = self.create_Blob_List_from_db_input(records,0,1,2,3,4,5,6,7,8,9,10,11)
        return blobs

    def get_Blobs_via_file_id(self, file_id:str)-> list[Blob]:
        records = self.execute_db_command_fetchall("SELECT * FROM Blob WHERE ID_File= ?", [self._encode_base64(file_id)])
        blobs = self.create_Blob_List_from_db_input(records,0,1,2,3,4,5,6,7,8,9,10,11)
        return blobs


    def get_Blob_via_id(self, id:str)-> Blob:
        blob = None
        row = self.execute_db_command_fetchall("SELECT * FROM Blob WHERE ID= ?", [id])
        if len(row) > 0:
                blob = Blob(row[0][0], row[0][1], row[0][2], self._decode_base64(row[0][3]), row[0][4], row[0][5], row[0][6],
                            self._decode_base64(row[0][7]), self._decode_base64(row[0][8]), self._decode_base64(row[0][9]),
                            self._decode_base64(row[0][10]))
        return blob

    def protocol_skipped_file(self, jewel:Jewel, file:File, reason:str, additional_information:str, connected_file:str, conn:sqlite3.Connection, cur:sqlite3.Cursor)-> None:
        """protocols skipped files which where not inserted again as a whole new file to the database

        Args:
            jewel (Jewel): Jewel of File
            file (File): File which was skipped
            reason (str): The Reason why
            additional_information (str): some optional reasons
            connected_file (str): file which is the reason of skipping
            conn (sqlite3.Connection): connection to db
            cur (sqlite3.Cursor): cursor to db
        """
        command = "INSERT INTO Skipped_Files (ID_Jewel, UUID, Occurance_Date, Hash, Reason, Additional_Information, Connected_File_to_Jewel) VALUES (?, ?, ?, ?, ?, ?, ? );"
        params = (jewel.id, self._encode_base64(file.id), datetime.datetime.today(), file.blobs[0].hash, reason,
                  additional_information, self._encode_base64(connected_file))
        self.execute_db_command_fetchall(command,params)


    def get_all_skipped_files (self)-> list[tuple[str]]:
        """Gives informatinos of skipped files for the show method

        Returns:
            list[tuple[str]]: files which should be displayed
        """
        result = []
        records = self.execute_db_command_fetchall("SELECT * FROM Skipped_Files")
        for row in records: 
            result.append((row[0], row[1], self._decode_base64(row[2]), row[3], row[4], row[5], row[6], self._decode_base64(row[7])))

        return result


    def get_skipped_file_via_id (self, id:str)-> list[str]:
        row = []
        row = self.execute_db_command_fetchall("SELECT * FROM Skipped_Files WHERE ID= ? Limit 1", [id])
        if len(row) > 0: row = (row[0], row[0][1], self._decode_base64(row[0][2]), row[0][3], row[0][4], row[0][5], row[0][6], self._decode_base64(row[0][7]))
        return row

    def get_restore_Jewel(self, until_date: datetime.datetime, jewel_id: int)->resJewel|None:
        """Gets the information from DB for Jewel restoring
        
        Args:
            until_date (datetime.datetime): Date to which time the jewel should be restored
            jewel_id (int): jewel id which should be restored
            
        Returns:
            resJewel | None: The Jewel or nothing if Id is not existing"""

        # the database shall look in every value of this day
        until_date = until_date.replace(hour=23, minute=59, second=59)
        assert (until_date.minute == 59 and until_date.hour == 23 and until_date.second == 59)

        command = """SELECT Id, FullbackupSource, JewelSource, ID_File, Number, source_path, Origin_Name, Store_Destination, max(insert_date) as insert_date, Hash, Reed_Solomon_Path FROM 
                        (SELECT Jewel.ID, Jewel.FullbackupSource, Jewel.JewelSource, Hardlinks.ID_File, Blob.Number as Number,  Hardlinks.Source_Path,
                        Hardlinks.origin_Name as Origin_Name, Hardlinks.destination_path as Store_Destination, Hardlinks.insert_date, Blob.Hash, Blob.Reed_Solomon_Path FROM File
                        INNER JOIN Jewel_File_Assignment on Jewel_File_Assignment.ID_File = File.ID
                        INNER JOIN Jewel on Jewel.ID = Jewel_File_Assignment.ID_Jewel
						INNER JOIN Hardlinks on File.ID = Hardlinks.ID_File
						INNER JOIN Blob on Hardlinks.ID_Blob = Blob.ID
                        WHERE Jewel.ID = ?
                        AND Hardlinks.insert_date <= ?
                        UNION
                        SELECT Jewel.ID, Jewel.FullbackupSource, Jewel.JewelSource, Blob.ID_File, Max(Blob.Number) as Number,  
                        Blob.Source_Path, Blob.Origin_Name, Blob.Store_Destination, Blob.CreationDate as insert_date, Blob.Hash, Blob.Reed_Solomon_Path FROM File
                        INNER JOIN Blob on File.ID = Blob.ID_File
                        INNER JOIN Jewel_File_Assignment on Jewel_File_Assignment.ID_File = File.ID
                        INNER JOIN Jewel on Jewel.ID = Jewel_File_Assignment.ID_Jewel
                        WHERE Jewel.ID = ?
                        AND Blob.CreationDate <= ?
                        GROUP BY Blob.ID_File)
                        GROUP BY ID_File"""

        params = (jewel_id, until_date, jewel_id, until_date)
        tmp = self.execute_db_command_fetchall(command, params)

        jewel = self.generate_resJewel_from_db_output(tmp,0,2,6,5,7,4,9,10)
        return jewel


    def get_restore_File(self, until_date: datetime, file_id: str)-> resFile | None:
        """Gets the data for File restoring from DB
        
            Args:
                until_date(datetime.datetime): Date to which time the file should be restored
                file_id(str): id of file which should be restored
                
            Returns:
                resFile | None: restored file data or nothing if id is not existing"""
 
        command = """SELECT Jewel.ID, Jewel.FullbackupSource, Jewel.JewelSource, Blob.ID_File, Max(Blob.Number) as Number,  Blob.Source_Path, Blob.Origin_Name, Blob.Store_Destination, Blob.CreationDate, Blob.hash, Blob.Reed_Solomon_Path FROM File
                    INNER JOIN Blob on File.ID = Blob.ID_File
                    INNER JOIN Jewel_File_Assignment on Jewel_File_Assignment.ID_File = File.ID
                    INNER JOIN Jewel on Jewel.ID = Jewel_File_Assignment.ID_Jewel
                    WHERE File.ID = ?
                    AND Blob.CreationDate <= ?
                    GROUP BY Blob.ID_File LIMIT 1;"""

        params = (self._encode_base64(file_id), until_date)
        row_files = self.execute_db_command_fetchall(command, params)


        command = """SELECT Jewel.ID, Jewel.FullbackupSource, Jewel.JewelSource, Hardlinks.ID_File, Blob.Number as Number,  Hardlinks.Source_Path, Hardlinks.origin_Name as Origin_Name, Hardlinks.destination_path as Store_Destination, Hardlinks.insert_date, Blob.hash, Blob.Reed_Solomon_Path FROM File
                    INNER JOIN Jewel_File_Assignment on Jewel_File_Assignment.ID_File = File.ID
                    INNER JOIN Jewel on Jewel.ID = Jewel_File_Assignment.ID_Jewel
					INNER JOIN Hardlinks on File.ID = Hardlinks.ID_File
					INNER JOIN Blob on Hardlinks.ID_Blob = Blob.ID
                    WHERE File.ID = ?
                    AND Hardlinks.insert_date <= ?
                    ORDER BY Hardlinks.insert_date DESC;"""
        row_hardlink = self.execute_db_command_fetchall(command,params)

        jewel = self.generate_resJewel_from_db_output(row_files,0,2,6,5,7,4,9,10)
        jewel_hardlink = self.generate_resJewel_from_db_output(row_hardlink,0,2,6,5,7,4,9,10)

        #decide,which one to choose
        ##if both have solutions, take the one which is newer, since it is closer to the date, the user wants
        if len(row_hardlink) > 0 and len(row_files) > 0 and row_hardlink[0][8] > row_files[0][8]:
            return jewel_hardlink
        #when no normal data exists, choose the hardlink
        elif len(row_hardlink) > 0 and not len(row_files)>0:
            return jewel_hardlink
        #else if the user gave an id wich is non existent
        elif not len(row_files)>0 and not  len(row_hardlink) > 0:
            return None
        #otherwise the normal file is the desired file
        else: return jewel


    def protocol_hardlink(self, hardlink_info:HardlinkInfo, device_name:str) -> None:
        """insert a hardlink to a file
        
            Args:
                hardlink_info(HardlinkInfo): all infos provided for hardlink
                device_name: name of current device"""

        command = """INSERT INTO FILE(ID, Birth) SELECT ?, ?
                     WHERE NOT EXISTS(SELECT 1 FROM FILE WHERE ID = ?);"""

        uri = self.set_uri(File(None,None,None), device_name, hardlink_info.source_path,hardlink_info.origin_name)
        params = (self._encode_base64(uri), hardlink_info.insert_date, self._encode_base64(uri))
        self.execute_db_command_fetchall(command,params)
        self.addJewelFileAssignment(hardlink_info.jewel_id, uri)

        command = """INSERT INTO "main"."Hardlinks"
                    ("ID_File", "ID_Blob", "destination_path", "source_path", "insert_date", "origin_name")
                    SELECT ?, ?, ?, ?, ?, ?
                    WHERE NOT EXISTS(SELECT 1 FROM Hardlinks WHERE ID_File = ? AND ID_Blob = ?);"""
        params = (self._encode_base64(uri),hardlink_info.id, self._encode_base64(hardlink_info.destination_path), self._encode_base64(hardlink_info.source_path), hardlink_info.insert_date, self._encode_base64(hardlink_info.origin_name), self._encode_base64(uri),hardlink_info.id)
        self.execute_db_command_fetchall(command,params)

            
    def get_all_blobs_for_repair(self)-> list[Blob]:
        """Returns all blobs which were needed to proceeds with Reed Solomon
        Meaning all Blobs,which do not have a RS path.  

        Returns:
            list[Blob]: list of blobs with no reed solomon path.
        """

        command = "SELECT * FROM Blob WHERE Reed_Solomon_Path == ?"
        param = (self._encode_base64("None"),)
        records = self.execute_db_command_fetchall(command, param)
        blobs = self.create_Blob_List_from_db_input(records, 0,1,2,3,4,5,6,7,8,9,10,11)
        return blobs

   
    def update_blobs_after_repair(self, rs_blobs:list("Blob"))-> None:
        """Inserts the new Reed Solomon paths to the blobs in the db.

            Args:
            rs_blobs(list(Blob)): List ob blobs with new reed solomon paths
        """
        insert_batch = [(self._encode_base64(blob.reed_solomon_path), blob.id) for blob in rs_blobs]
        command = """UPDATE Blob
                     SET Reed_Solomon_Path = ?
                     WHERE Blob.ID = ? Limit 1;"""
        self.execute_db_command_fetchall(command,insert_batch, executemany=True)


    def create_Blob_List_from_db_input(self, db_output_row:list[tuple[str]], id_idx:int, number_idx:int, hash_idx:int,name_idx:int,fileSize_idx:int,
    creationDate_idx:int,modify_idx:int,iD_File_idx:int,origin_name_idx:int,source_path_idx:int, store_destination_idx:int, reed_Solomon_path_idx:int )->list("Blob"):
        """takes a multirow db output and creates an bloblist

        Args:
        db_output_row (list[tuple[str]]): multirow db output
        id_idx (int): index which to search for this property
        number_idx (int): index which to search for this property
        hash_idx (int): index which to search for this property
        name_idx (int): index which to search for this property
        fileSize_idx (int): index which to search for this property
        creationDate_idx (int): index which to search for this property
        modify_idx (int): index which to search for this property
        iD_File_idx (int): index which to search for this property
        origin_name_idx (int): index which to search for this property
        source_path_idx (int): index which to search for this property
        store_destination_idx (int): index which to search for this property
        reed_Solomon_path_idx (int): index which to search for this property
            

        Returns:
            list(Blob): a list of Blobs
        """
        blob_list = []

        if db_output_row:
            blob_list = [Blob(
                    id=row[id_idx], 
                    number=row[number_idx], 
                    hash = row[hash_idx],
                    name = self._decode_base64(row[name_idx]),
                    fileSize= row[fileSize_idx],
                    creationDate =row[creationDate_idx],
                    modify=row[modify_idx],
                    iD_File = self._decode_base64(row[iD_File_idx]),
                    origin_name = self._decode_base64(row[origin_name_idx]),
                    source_path= self._decode_base64(row[source_path_idx]),
                    store_destination = self._decode_base64(row[store_destination_idx]),
                    reed_solomon_path = self._decode_base64(row[reed_Solomon_path_idx])
                    )for row in db_output_row]
        return blob_list

    def execute_db_command_fetchall(self, command:str,params:tuple=(), executemany:bool=False):
        """Creates a db connection. Execute a db command, commits it and does fetchall. Closes the connection

        Args:
            command (str): the desired command which should be executed
            params (tuple, optional): needed params. Defaults to ().
            executemany (bool, optional): If wished, the command and params will executed with executemany. Defaults to False.

        Raises:
            ConnectionError: If no connection is possible, this Error will be raised.

        Returns:
            list(tuple(str)): Database output, which will be always in a form of many rows, because of fetchall().
        """
        records = None
        conn = self.create_connection(self.database_path)

        if conn == None:
            raise ConnectionError

        cur = conn.cursor()

        if executemany:
            cur.executemany(command,params)
        else:
            cur.execute(command, params)

        records = cur.fetchall()
        conn.commit()
        conn.close()

        return records


    def generate_resJewel_from_db_output(self,database_rows:list[str], jewel_id_idx:int, jewel_source_idx:int,
                                         file_name_idx:int, origin_location_idx:int, backup_location_idx:int,
                                         version_number_idx:int, hash_idx:int, reed_solomon_path_idx:int)-> resJewel | None:
        """generate a resJewel from a multiline db output

        Args:
            database_rows (list[str]): multiline db output
            jewel_id_idx (int): index which to search for this property
            jewel_source_idx (int): index which to search for this property
            file_name_idx (int): index which to search for this property
            origin_location_idx (int): index which to search for this property
            backup_location_idx (int): index which to search for this property
            version_number_idx (int): index which to search for this property
            hash_idx (int): index which to search for this property
            reed_solomon_path_idx (int): index which to search for this property

        Returns:
            resJewel | None: resJewel if db output has values, None if db output has no values
        """
        if len(database_rows) > 0:
            files = [self.generate_resFile_from_db_output(row,file_name_idx,origin_location_idx,
                     backup_location_idx,version_number_idx,hash_idx,reed_solomon_path_idx)
                     for row in database_rows]

            jewel = resJewel(None, database_rows[0][jewel_id_idx], files, self._decode_base64(database_rows[0][jewel_source_idx]))
            return jewel
        else:
            return None 

    def generate_resFile_from_db_output(self, db_output_row:list[str], file_name_idx:int, origin_location_idx:int, backup_location_idx:int,
                                        version_number_idx:int, hash_idx:int, reed_solomon_path_idx:int) ->resFile:
        """takes an db row and converts it to a resFile

        Args:
            db_output_row (list[str]): db output row
            file_name_idx (int): index which to search for this property
            origin_location_idx (int): index which to search for this property
            backup_location_idx (int): index which to search for this property
            version_number_idx (int): index which to search for this property
            hash_idx (int): index which to search for this property
            reed_solomon_path_idx (int): index which to search for this property

        Returns:
            resFile: a resFile
        """
    
        res_file = resFile(
        file_name = self._decode_base64(db_output_row[file_name_idx]),
        origin_location = self._decode_base64(db_output_row[origin_location_idx]),
        backup_location = self._decode_base64(db_output_row[backup_location_idx]),
        version_number = db_output_row[version_number_idx],
        hash = db_output_row[hash_idx],
        reed_solomon_path = self._decode_base64(db_output_row[reed_solomon_path_idx])) 

        return res_file

