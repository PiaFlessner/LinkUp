
import os
import pathlib
import platform
import shutil
import subprocess
from time import sleep
import unittest
from filecmp import cmpfiles
import datenbank
from os.path import exists as path_exists
from filecmp import dircmp
from filecmp import cmpfiles

import info_handler
import test_database_insert

test_database_insert.insert_for_test_database()

device_name = platform.node()


def are_dir_trees_equal(dir1, dir2):

    dirs_cmp = dircmp(dir1, dir2)

    # überprüfen, ob unterschiedliche Files oder Dirs vom Namen her
    if len(dirs_cmp.left_only) > 0 or len(dirs_cmp.right_only) > 0 or len(dirs_cmp.funny_files) > 0:
        # existieren
        return False

    (match, mismatch, errors) = cmpfiles(
        dir1, dir2, dirs_cmp.common_files, shallow=False)

    if len(mismatch) > 0 or len(errors) > 0:    # nach Inhalt überprüfen
        return False

    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        if not are_dir_trees_equal(new_dir1, new_dir2):
            return False
    return True


config = info_handler.get_json_info(device_name)
database_path = config['destination'][device_name] + '/datenbank.db'
database_path = os.path.abspath(database_path)


class TestDatabase(unittest.TestCase):
    # for creating test data in backuptest folder
    # cd unitTestFiles
    # head -c 10M /dev/urandom > sample.txt
    # split sample.txt -n 500
    #
    @classmethod
    def setUpClass(cls):
        cls.platform_node = platform.node()
        # gonna use this in the future maybe
        pass

    def test_1_init_database_exists(self):
        datenbank.Datenbank()
        self.assertTrue(path_exists(database_path))

    def test_2_backup(self):
        process = subprocess.Popen(
            ["python3", "execute.py", "backup"], stdout=subprocess.PIPE)  # stdout is just to get rid of the prints
        process.wait()
        process.stdout.close()
        for jewel in config["jewel_sources"][self.platform_node]:
            jewel_absolute_path = str(pathlib.Path(jewel).resolve())
            jewel_name = jewel.rsplit("/", 1)[1]
            dest_path = config["destination"][self.platform_node] + \
                "/fullBackup"f"{device_name}/{jewel_name}"
            try:
                self.assertTrue(are_dir_trees_equal(dest_path,
                                                    jewel_absolute_path))
            except FileNotFoundError:
                print("Test A:")
                print("File or Directory not Found")
                self.assertTrue(False)

    def test_3_backup_and_create_redundancy(self):
        process = subprocess.Popen(
            ["python3", "execute.py", "backup"], stdout=subprocess.DEVNULL)  # stdout is just to get rid of the prints
        process.wait()
        # process.close()
        for jewel in config["jewel_sources"][self.platform_node]:
            jewel_absolute_path = str(pathlib.Path(jewel).resolve())
            jewel_name = jewel.rsplit("/", 1)[1]
            dest_path = config["destination"][self.platform_node] + \
                "/fullBackup"f"{device_name}/{jewel_name}"
            try:
                self.assertTrue(are_dir_trees_equal(dest_path,
                                                    jewel_absolute_path))
            except FileNotFoundError:
                print("Test A:")
                print("File or Directory not Found")
                self.assertTrue(False)
        process = subprocess.Popen(
            ["python3", "execute.py", "rs", "-ca"], stdout=subprocess.DEVNULL)
        process.wait()
        try:
            self.assertTrue(are_dir_trees_equal(dest_path,
                                                    jewel_absolute_path))
        except FileNotFoundError:
            print("Test A:")
            print("File or Directory not Found")
            self.assertTrue(False)
            
            

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
