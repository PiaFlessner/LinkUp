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

def are_dir_trees_equal(dir1, dir2):
    
    dirs_cmp = dircmp(dir1, dir2) 
    
    if len(dirs_cmp.left_only) > 0 or len(dirs_cmp.right_only) > 0 or len(dirs_cmp.funny_files) > 0: # überprüfen, ob unterschiedliche Files oder Dirs vom Namen her
                                                                                                     #existieren 
        return False                                                                                 
    
    (match, mismatch, errors) =  cmpfiles(dir1, dir2, dirs_cmp.common_files, shallow=False)
    
    if len(mismatch) > 0 or len(errors) > 0:    # nach in halt überprüfen
        return False
    
    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        if not are_dir_trees_equal(new_dir1, new_dir2):
            return False
    return True
#class TestBackup(unittest.TestCase):
#
#    @classmethod
#    def setUpClass(cls):
#        cls.daten = datenbank.Datenbank()
#        cls.config = ih.get_json_info(device_name)
#        cls.backup = Backup(cls.config["jewel_sources"][device_name], cls.config["destination"][device_name], True)
#        cls.backup.initialize_backup()
# 
#         
#    def test_a_fullbackup_jewel(self):
#        self.assertTrue(are_dir_trees_equal(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel"),
#                                                    os.path.join(os.path.dirname(__file__),"unitTestFiles/backupLocation/fullBackup"f"{device_name}/jewel")))
#    
#    def test_b_fullbackup_jewel2(self):
#        self.assertTrue(are_dir_trees_equal(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel2"),
#                                             os.path.join(os.path.dirname(__file__),"unitTestFiles/backupLocation/fullBackup"f"{device_name}/jewel2")))
#   
#  
#    def test_c_diffBackup_jewel(self):
#        file = open(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel/test1.txt"), "a")
#        file2 = open(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel2/test2.txt"), "a")
#        
#        for i in range(5):
#            file.write("Hello World in test1.txt\n")
#            file2.write("Hello World in test2.txt\n")
#        file.close()
#        file2.close()
#        self.backup.initialize_backup() 
#        
#        
#        self.assertTrue(are_dir_trees_equal(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel")
#                        ,os.path.join(os.path.dirname(__file__),"unitTestFiles/backupLocation/"f"diff-{date.now().strftime('%d-%m-%Y-%H-%M')}/jewel")))
#        
#    def test_d_diffBackup_jewel2(self):
#
#        self.assertTrue(are_dir_trees_equal(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel2")
#                        , os.path.join(os.path.dirname(__file__),"unitTestFiles/backupLocation/"f"diff-{date.now().strftime('%d-%m-%Y-%H-%M')}/jewel2")))
#
#    @classmethod
#    def tearDownClass(cls):
#        time.sleep(20)
#        os.remove("datenbank.db")
#        shutil.rmtree(cls.config["destination"][device_name])
#        shutil.rmtree(cls.config["restore_destination"][device_name])
#

class TestRestore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.daten = datenbank.Datenbank()
        cls.config = ih.get_json_info(device_name)
        cls.workingDirectory = str(pathlib.Path(__file__).parent.resolve())

        jewel_list = cls.config["jewel_sources"][device_name]
        i = 0
        for element in jewel_list:
            jewel_list[i] = cls.workingDirectory + element
            i= i+ 1

        print(jewel_list)

        cls.backup = Backup(jewel_list, cls.workingDirectory + "/" + cls.config["destination"][device_name], True)
        cls.backup.initialize_backup()
        time.sleep(15)

    def test_a_restore_Jewel_only_Fullbackup(self):
        restoreDay = date.today()
        jewel = self.daten.get_restore_Jewel(restoreDay, 1)
        self.assertTrue(jewel!= None,"An answer is None")
        self.assertTrue(len(jewel[1]) == 1,"The lenght is incorrect")
        self.assertTrue(jewel[0] == 1, f"The id is wrong. Must be 1, but is {jewel[0]}")
        self.assertTrue(jewel[1][0][0] == 'test1.txt', 'Name is wrong')
        self.assertTrue(jewel[1][0][1] == '/home/gruppe/Schreibtisch/Projektgruppe/projektgruppe/unitTestFiles/jewel/test1.txt', f'jewel path is wrong. Its {jewel[1][0][1]}')
        self.assertTrue(jewel[1][0][2] == '/home/gruppe/Schreibtisch/Projektgruppe/projektgruppe/unitTestFiles/backupLocation/fullBackuptestCases/jewel/test1.txt', 'backup location is wrong')
        self.assertTrue(jewel[1][0][3] == 1, f'Version Number is wrong. Should be 1, but is {jewel[1][0][3]}')

    def test_b_restore_Jewel_date_in_past(self):
        restoreDay = date.today()
        restoreDay = restoreDay.replace(year=2000)
        jewel = self.daten.get_restore_Jewel(restoreDay,1)
        self.assertTrue(jewel== None,"The answer should be None")


    def test_c_restore_File_only_Fullbackup(self):
        restoreDay = date.today()
        file = self.daten.get_restore_File(restoreDay, "testCases/home/gruppe/Schreibtisch/Projektgruppe/projektgruppe/unitTestFiles/jewel/test1.txt")
        self.assertTrue(file!= None,"An answer is None")

        self.assertTrue(file[0] == 'test1.txt', 'Name is wrong')
        self.assertTrue(file[1] == '/home/gruppe/Schreibtisch/Projektgruppe/projektgruppe/unitTestFiles/jewel/test1.txt', f'jewel path is wrong: {file[1]}')
        self.assertTrue(file[2] == '/home/gruppe/Schreibtisch/Projektgruppe/projektgruppe/unitTestFiles/backupLocation/fullBackuptestCases/jewel/test1.txt', 'backup location is wrong')

    def test_d_restore_jewel_diff_backup_change_file(self):
      restoreDay = date.today()
      file = open("/home/gruppe/Schreibtisch/Projektgruppe/projektgruppe/unitTestFiles/jewel/test1.txt", "a")
      for i in range(5):
          file.write("Change change change")
      file.close()
      #touch the the dir, for the real behavior of
      os.utime("/home/gruppe/Schreibtisch/Projektgruppe/projektgruppe/unitTestFiles/jewel")

    
      time.sleep(10)
      self.backup.initialize_backup()
      time.sleep(30)
      jewel = self.daten.get_restore_Jewel(restoreDay,1)
      self.assertTrue(jewel[1][0][3] == 2, f'Version Number is wrong. Should be 2, but is {jewel[1][0][3]}')

   
    def test_e_restore_Jewel_diff_backup_new_file(self):
        restoreDay = date.today()
        #create_new_file
        file = open(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel/test_new.txt"), "a")

        for i in range(5):
            file.write("Hello World in test_new.txt\n")
        file.close()
        self.backup.initialize_backup()
        time.sleep(45)
        jewel = self.daten.get_restore_Jewel(restoreDay,1)
        self.assertTrue(jewel!= None,"An answer is None")
        self.assertTrue(len(jewel[1]) == 2,"The lenght is incorrect")


    def test_f_restore_File_diff_backup(self):
        restoreDay = date.today()
        file = self.daten.get_restore_File(restoreDay, "testCases/home/gruppe/Schreibtisch/Projektgruppe/projektgruppe/unitTestFiles/jewel/test1.txt")
        self.assertTrue(file!= None,"An answer is None")
        self.assertTrue(file[3] == 2, f"Version Number ist wrong, should be 2, is {file[3]}")


    @classmethod
    def tearDownClass(cls):

        os.remove("datenbank.db")
        shutil.rmtree(cls.config["destination"][device_name])
        shutil.rmtree(cls.config["restore_destination"][device_name])
        os.remove("unitTestFiles/jewel/test_new.txt")
   
        
if __name__ == "__main__":
    unittest.main()
