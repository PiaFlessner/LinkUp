
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
import test_database_insert
test_database_insert.insert_for_test_database()

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

    def test_1_init_database_exists():
        assertTrue(True)

def suite():
    suite = unittest.TestSuite()
    return suite


if __name__ == "__main__":
    unittest.main()
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())

    # run tests with python3 -m unittest test_backup.py
