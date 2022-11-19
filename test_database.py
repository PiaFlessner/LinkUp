
import unittest
from backup import Backup
import info_handler as ih
from filecmp import dircmp
from filecmp import cmpfiles
from datetime import datetime as date
import datenbank
from os.path import exists as path_exists

device_name = "testCases"

def are_dir_trees_equal(dir1, dir2):
    
    pass


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_a_init_database_exists(self):
        daten = datenbank.Datenbank()
        self.assertTrue(path_exists('datenbank.db'))
    
    def test_b_init_same_tables_exist(self):
        daten = datenbank.Datenbank()
        conn = daten.create_connection('datenbank.db')
        if conn != None:
            cur = conn.cursor()
            cur.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
            data = cur.fetchall()
            for row in data:
                print(row)


    def test_c_init_all_columns_are_as_expected(self):
        pass

    def test_d_something(self):
        pass

    def addJewel(self,jewel):
    def addJewelFileAssignment (self, id_jewel, id_file):
    def check_which_jewel_sources_exist(self, jewel_source_arr, device_name):    
    def get_Jewel_via_id(self,id):
    def get_File_via_id(self,id):
    def get_File_via_hash(self,hash):
    def get_all_Files(self):
    def get_Files_via_jewel_id(self,jewel_id):

   


def suite():
  suite = unittest.TestSuite()
  return suite

        
if __name__ == "__main__":
    unittest.main()
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())

    #run tests with python3 -m unittest test_backup.py
