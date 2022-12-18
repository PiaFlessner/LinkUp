
import os
import platform
import shutil
import subprocess
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
database_path = config['destination'][device_name] + '/datenbank.db'
database_path = os.path.abspath(database_path)


class TestDatabase(unittest.TestCase):
    #for creating test data in backuptest folder
    #cd unitTestFiles
    #head -c 10M /dev/urandom > sample.txt
    #split sample.txt -n 500
    #
    @classmethod
    def setUpClass(cls):
        # gonna use this in the future maybe
        pass

    def test_1_init_database_exists(self):
        # debating whether or not the assignment to daten makes sense because it's the same in the next method
        daten = datenbank.Datenbank()
        self.assertTrue(path_exists(database_path))

    def test_2_backup_and_repair(self):
        process = subprocess.Popen(
            ["python3", "execute.py", "backup"],stdout=subprocess.PIPE) # stdout is just to get rid of it..
        process.wait()
        process.stdout.close()


    @classmethod
    def tearDown(foobar):
        config = info_handler.get_json_info(device_name)
        shutil.rmtree(config["destination"][device_name])
        shutil.rmtree(config["restore_destination"][device_name])
        pass


def suite():
    suite = unittest.TestSuite()
    return suite


if __name__ == "__main__":
    unittest.main()
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())

    # run tests with python3 -m unittest test_backup.py
