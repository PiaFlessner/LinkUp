
import os
import platform
import shutil
from time import sleep
import unittest
from filecmp import cmpfiles
import datenbank
from os.path import exists as path_exists
import random
import string
import datetime
import info_handler
from datenbank import Jewel

device_name = platform.node()


def are_dir_trees_equal(dir1, dir2):
    pass

config = info_handler.get_json_info(device_name)
database_path=config['destination'][device_name] + '/datenbank.db'
database_path=os.path.abspath(database_path)
class TestDatabase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        #gonna use this in the future maybe
        pass

    def test_1_init_database_exists(self):
        daten = datenbank.Datenbank() #debating whether or not the assignment to daten makes sense because it's the same in the next method
        self.assertTrue(path_exists(database_path))

    def test_2_init_same_tables_exist(self):
        table_names = ["Jewel", "sqlite_sequence", "File", "Jewel_File_Assignment",
                       "Blob", "Skipped_Files"]  # correct list of table names. sqlite_sequence is an automatically created table that could be excluded from this list
        daten = datenbank.Datenbank()
        conn = daten.create_connection(database_path)
        if conn != None:
            cur = conn.cursor()
            cur.execute(
                """SELECT name FROM sqlite_master WHERE type='table'""")
            data = cur.fetchall()
            mylist = []  # table names extracted from database
            for row in data:
                mylist.append(row[0])
            # assert that all 6 tablenames are equal
            self.assertTrue(set(table_names).intersection(mylist).__len__() == 6)
            conn.close()

    # we look into the sqlite_master table and compare it to our table-creating-commands, to make sure that everything is as expected https://www.sqlite.org/schematab.html
    def test_3_init_all_columns_are_as_expected(self):
        sql_befehle = ["""CREATE TABLE Jewel (
                                    ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    Comment TEXT,
                                    Monitoring_Startdate NUMERIC NOT NULL,
                                    JewelSource TEXT NOT NULL,
                                    DeviceName TEXT NOT NULL,
                                    FullbackupSource TEXT NOT NULL
                                                 )""", """CREATE TABLE File (
                                    ID TEXT NOT NULL PRIMARY KEY,
                                    Birth TIMESTAMP NOT NULL
                                                )""", """CREATE TABLE Jewel_File_Assignment (
                                    ID_Jewel INTEGER NOT NULL,
                                    ID_File INTEGER NOT NULL,
                                    PRIMARY KEY(ID_Jewel,ID_File),
                                     constraint file_assignment_fk
                                     FOREIGN KEY (ID_File)
                                        REFERENCES File(ID),
                                     constraint jewel_assignment_fk
                                     FOREIGN KEY (ID_Jewel)
                                        REFERENCES Jewel(ID)
                                                 )""", """CREATE TABLE Blob (
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
                                                   )""", """CREATE TABLE Skipped_Files(
                    ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    ID_Jewel INTEGER NOT NULL,
                    UUID TEXT NOT NULL,
                    Occurance_Date TIMESTAMP NOT NULL,
                    Hash TEXT NOT NULL,
                    Reason TEXT NOT NULL,
                    Additional_Information TEXT,
                    Connected_File_to_Jewel TEXT
                )"""]
        daten = datenbank.Datenbank()
        conn = daten.create_connection(database_path)
        if conn != None:
            cur = conn.cursor()
            cur.execute(
                """SELECT name FROM sqlite_master WHERE type='table'""")
            data = cur.fetchall()
            mylist = []
            for tablename in data:
                command = """SELECT sql FROM sqlite_master
                WHERE tbl_name = ? AND type = 'table'"""
                params = (tablename[0],)
                cur.execute(command, params)
                data2 = cur.fetchall()
                for columnname in data2:
                    mylist.append(columnname[0])
            self.assertTrue(set(sql_befehle).intersection(mylist).__len__(), 5)
            conn.close()

    def test_4_something(self):
        pass

    def test_5_encode_base64(self):
        to_test = "Hallö, Welt!?§$%&/5534.-_:#*~+´'`}][{¬½¼³²¹!§$%&/()?\""
        daten = datenbank.Datenbank()
        encoded = daten._encode_base64(to_test)
        decoded = daten._decode_base64(encoded)
        self.assertEqual(to_test, decoded)

    def test_6_encode_base64(self):
        to_test = ''.join(random.choice(string.printable)
                          for i in range(50000))
        daten = datenbank.Datenbank()
        encoded = daten._encode_base64(to_test)
        decoded = daten._decode_base64(encoded)
        self.assertEqual(to_test, decoded)

    def test_7_set_uri(self):
        daten = datenbank.Datenbank()
        my_file =datenbank.File( "id", "blobs", "birth")
        daten.set_uri(my_file, device_name, "file_path", "file_name")
        self.assertEqual(device_name+"file_path",my_file.id)

    def test_8_addJewel(self):
        daten = datenbank.Datenbank()
        jewel = Jewel(0, None, datetime.date.today(), "jewel_path", device_name,"fullbackup_source")
        jewel2 = Jewel(0, "meepツ", datetime.date.today(), "jewdel_path", device_name,"fullbackup_source")
        self.assertTrue(daten.addJewel(jewel)==1)
        self.assertTrue(daten.addJewel(jewel2)==2)
        conn = daten.create_connection(database_path)
        if conn != None:
            cur = conn.cursor()
            # check if the jewel already exists in the database
            command = "SELECT MAX(ID) FROM Jewel"
            cur.execute(command)
            cur.execute("SELECT * FROM Jewel")
            data = cur.fetchall()
            mylist = []
            for entry in data:
                mylist.append(entry)
            self.d_r_y(1,jewel,daten,mylist[0])
            self.d_r_y(2,jewel2,daten,mylist[1])
            conn.close() 

    def d_r_y(self, id, jewel:Jewel, daten, jewel_from_database):
        if(jewel.comment==None):
            jewel.comment="None" #TODO fix the fact that the database returns "None" instead of None or decide the bug doesn't matter
        self.assertEqual(id, jewel_from_database[0])
        self.assertEqual(jewel.comment, daten._decode_base64(jewel_from_database[1]))
        self.assertEqual(jewel.monitoring_Startdate.isoformat(), jewel_from_database[2])
        self.assertEqual(jewel.jewelSource, daten._decode_base64(jewel_from_database[3]))
        self.assertEqual(jewel.device_name, daten._decode_base64(jewel_from_database[4]))
        self.assertEqual(jewel.fullbackup_source, daten._decode_base64(jewel_from_database[5]))
    
    
    def test_9_check_if_uri_exists(self):
        db = datenbank.Datenbank()
        blob= datenbank.Blob("id","number","hash","name","fileSize",datetime.datetime.now(),"modify","iD_File","origin_name","source_path","store_destination")
        file = datenbank.File("id", blob, "birth", False)
        conn = db.create_connection(database_path)
        self.assertTrue(conn != None)
        if conn != None:
            cur = conn.cursor()
            db.insert_File(file,cur,conn)
            file = db.get_File_via_id("1")
        print(file)
        conn.close
        conn.close
        pass

    def addJewelFileAssignment(self, id_jewel, id_file):
        pass

    def add_to_database(self, jewel, file, device_name):
        pass


    def insert_new_blob_to_existing_file(self, new_file, cur, conn, old_file):
        pass

    def insert_first_Blob(self, file, cur, conn):
        pass

    def insert_File(self, file, cur, con):
        pass

    def check_if_hash_exists(self, file, cur, device_name):
        pass

   

   

    def check_which_jewel_sources_exist(self, jewel_source_arr, device_name):
        pass

    def get_Jewel_via_id(self, id):
        pass

    def get_File_via_id(self, id):
        pass

    def get_File_via_hash(self, hash):
        pass

    def get_all_Files(self):
        pass

    def get_Files_via_jewel_id(self, jewel_id):
        pass

    def get_all_Jewels(self):
        pass

    def get_all_Blobs(self):
        pass

    def get_Blobs_via_file_id(self, file_id):
        pass

    def get_Blob_via_id(self, id):
        pass

    def protocol_skipped_file(self, jewel, file, reason, additional_information, connected_file, conn, cur):
        pass

    def get_all_skipped_files(self):
        pass

    def get_skipped_file_via_id(self, id):
        pass

    def get_fullbackup_paths(self, jewel_source_arr):
        pass


    @classmethod
    def tearDown(foobar):
        config = info_handler.get_json_info(device_name)
        if path_exists("datenbank.db"):
            os.remove("datenbank.db")
        shutil.rmtree(config["destination"][device_name])
        shutil.rmtree(config["restore_destination"][device_name])


def suite():
    suite = unittest.TestSuite()
    return suite


if __name__ == "__main__":
    unittest.main()
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())

    # run tests with python3 -m unittest test_backup.py
