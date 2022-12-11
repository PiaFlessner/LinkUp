import pathlib
import time
import unittest
from backup import Backup
import info_handler as ih
import platform
import os
from filecmp import dircmp
from filecmp import cmpfiles
from datetime import datetime as date
import datenbank
import shutil

device_name = "testCases"
class TestRestore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.daten = datenbank.Datenbank(testcase=True)
        cls.config = ih.get_json_info(device_name)
        cls.workingDirectory = str(pathlib.Path(__file__).parent.resolve())

        cls.jewel_list = cls.config["jewel_sources"][device_name]
        i = 0
        for element in cls.jewel_list:
            cls.jewel_list[i] = cls.workingDirectory + element
            i= i+ 1

        cls.backup = Backup(cls.jewel_list, cls.workingDirectory + "/" + cls.config["destination"][device_name], True)
        cls.backup.initialize_backup(0)
        time.sleep(15)

    def test_a_restore_Jewel_only_Fullbackup(self):
        restoreDay = date.today()
        jewel = self.daten.get_restore_Jewel(restoreDay, 1)
        self.assertTrue(jewel!= None,"An answer is None")
        self.assertTrue(len(jewel.res_file) == 1,f"The lenght is incorrect. Should be 1, but is {len(jewel.res_file)}")
        self.assertTrue(jewel.jewel_id == 1, f"The id is wrong. Must be 1, but is {jewel.jewel_id}")
        self.assertTrue(jewel.res_file[0].file_name == 'test1.txt', 'Name is wrong')
        self.assertTrue(jewel.res_file[0].origin_location == f'{self.workingDirectory}/unitTestFiles/jewel/test1.txt', f'jewel path is wrong. Its {jewel.res_file[0].origin_location}')
        self.assertTrue(jewel.res_file[0].backup_location == f'{self.workingDirectory}/unitTestFiles/backupLocation/fullBackuptestCases/jewel/test1.txt', 'backup location is wrong')
        self.assertTrue(jewel.res_file[0].version_number == 1, f'Version Number is wrong. Should be 1, but is {jewel.res_file[0].version_number}')

    def test_b_restore_Jewel_date_in_past(self):
        restoreDay = date.today()
        restoreDay = restoreDay.replace(year=2000)
        jewel = self.daten.get_restore_Jewel(restoreDay,1)
        self.assertTrue(jewel== None,"The answer should be None")


    def test_c_restore_File_only_Fullbackup(self):
        restoreDay = date.today()
        jewel = self.daten.get_restore_File(restoreDay, f"testCases{self.workingDirectory}/unitTestFiles/jewel/test1.txt")
        self.assertTrue(jewel!= None,"An answer is None")

        self.assertTrue(jewel.res_file[0].file_name == 'test1.txt', f'Name is wrong, it returns {jewel.res_file[0].file_name}')
        self.assertTrue(jewel.res_file[0].origin_location == f'{self.workingDirectory}/unitTestFiles/jewel/test1.txt', f'jewel path is wrong: {jewel.res_file[0].origin_location}')
        self.assertTrue(jewel.res_file[0].backup_location == f'{self.workingDirectory}/unitTestFiles/backupLocation/fullBackuptestCases/jewel/test1.txt', 'backup location is wrong')

    def test_d_restore_jewel_diff_backup_change_file(self):
      restoreDay = date.today()
      file = open(f"{self.workingDirectory}/unitTestFiles/jewel/test1.txt", "a")
      for i in range(5):
          file.write("Change change change")
      file.close()
      #touch the the dir, for the real behavior of
      os.utime(f"{self.workingDirectory}/unitTestFiles/jewel")

    
      time.sleep(10)
      backup_d = Backup(self.jewel_list, self.workingDirectory + "/" + self.config["destination"][device_name], True)
      backup_d.initialize_backup(0)
      time.sleep(30)
      jewel = self.daten.get_restore_Jewel(restoreDay,1)
      self.assertTrue(jewel.res_file[0].version_number == 2, f'Version Number is wrong. Should be 2, but is {jewel.res_file[0].version_number}')

   
    def test_e_restore_Jewel_diff_backup_new_file(self):
        restoreDay = date.today()
        #create_new_file
        file = open(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel/test_new.txt"), "a")

        for i in range(5):
            file.write("Hello World in test_new.txt\n")
        file.close()
        backup_e = Backup(self.jewel_list, self.workingDirectory + "/" + self.config["destination"][device_name], True)
        backup_e.initialize_backup(0)
        time.sleep(45)
        jewel = self.daten.get_restore_Jewel(restoreDay,1)
        self.assertTrue(jewel!= None,"An answer is None")
        self.assertTrue(len(jewel.res_file) == 2,"The lenght is incorrect")


    def test_f_restore_File_diff_backup(self):
        restoreDay = date.today()
        restoreDay.replace(hour=23, minute = 59, second=59)
        jewel = self.daten.get_restore_File(restoreDay, f"testCases{self.workingDirectory}/unitTestFiles/jewel/test1.txt")
        self.assertTrue(jewel!= None,"An answer is None")
        self.assertTrue(jewel.res_file[0].version_number == 2, f"Version Number ist wrong, should be 2, is {jewel.res_file[0].version_number}")

    def test_g_restore_symlink_file(self):
        open(os.path.join(os.path.dirname(__file__), "unitTestFiles/reference_file_to_symlink.txt"), "a")
        os.symlink("unitTestFiles/reference_file_to_symlink.txt", "unitTestFiles/jewel/symlink")
        backup_g = Backup(self.jewel_list, self.workingDirectory + "/" + self.config["destination"][device_name], True)
        backup_g.initialize_backup(0)

        latest_diff_folder = max([os.path.join('unitTestFiles/backupLocation',d) for d in os.listdir('unitTestFiles/backupLocation') if not d.endswith("db") and  not d.endswith("log")], key=os.path.getmtime)
        self.assertTrue(os.path.islink(latest_diff_folder + "/" + "jewel/symlink"), "File should be a symlink")


    def test_h_db_log (self):
        self.assertTrue(os.path.join(os.path.dirname(__file__), "unitTestFiles/backupLocation" + "/" + "db.log"), "db.log does not exist")


    def test_i_restore_database_and_backup (self):
        os.mkdir(os.path.join(os.path.dirname(__file__), "unitTestFiles/backupLocation" + "/" + "diff-test"))
        file = open(os.path.join(os.path.dirname(__file__), "unitTestFiles/backupLocation" + "/" + "db.log"), "r")
        old_hash = file.readlines()[0].rstrip()
        file.close()
        ih.update_db_hash(os.path.join(os.path.dirname(__file__), "unitTestFiles/backupLocation"), "diff-test")
        ih.check_db_hash(os.path.join(os.path.dirname(__file__), "unitTestFiles/backupLocation"), "diff-test", True)
        jewel = self.daten.get_Jewel_via_id(1)
        jewel.device_name = "Hallo"
        jewel.fullbackup_source = "Test"
        self.daten.addJewel(jewel)
        ih.check_db_hash(os.path.join(os.path.dirname(__file__), "unitTestFiles/backupLocation"), "test", True)
        file = open(os.path.join(os.path.dirname(__file__), "unitTestFiles/backupLocation" + "/" + "db.log"), "r")
        self.assertTrue(file.readlines()[0].rstrip() == old_hash, "database hash should be the same")
        self.assertFalse(os.path.exists(os.path.join(os.path.dirname(__file__), "unitTestFiles/backupLocation" + "/" + "diff-test")))
        file.close()






    @classmethod
    def tearDownClass(cls):
        os.remove(cls.config["destination"][device_name] + '/datenbank.db')
        os.remove(cls.config["destination"][device_name] + '/db.log')
        shutil.rmtree(cls.config["destination"][device_name])
        shutil.rmtree(cls.config["restore_destination"][device_name])
        os.remove("unitTestFiles/jewel/test_new.txt")
        os.remove("unitTestFiles/reference_file_to_symlink.txt")
        os.remove("unitTestFiles/jewel/symlink")


def suite():
  suite = unittest.TestSuite()

 

  suite.addTest(TestRestore.test_a_restore_Jewel_only_Fullbackup)
  suite.addTest(TestRestore.test_b_restore_Jewel_date_in_past)
  suite.addTest(TestRestore.test_c_restore_File_only_Fullbackup)
  suite.addTest(TestRestore.test_d_restore_jewel_diff_backup_change_file)
  suite.addTest(TestRestore.test_e_restore_Jewel_diff_backup_new_file)
  suite.addTest(TestRestore.test_f_restore_File_diff_backup)
  suite.addTest(TestRestore.test_g_restore_symlink_file)
  return suite

        
if __name__ == "__main__":
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())

    #run tests with python3 -m unittest test_backup.py
