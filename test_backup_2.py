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
    
class TestBackup(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        cls.daten = datenbank.Datenbank()
        cls.config = ih.get_json_info(device_name)
        cls.workingDirectory = str(pathlib.Path(__file__).parent.resolve())
        
        jewel_list = cls.config["jewel_sources"][device_name]

        for (index, element) in enumerate(jewel_list):
            jewel_list[index] = cls.workingDirectory + element

        
        cls.backup = Backup(jewel_list, cls.workingDirectory + '/' + cls.config["destination"][device_name], True)
        cls.backup.initialize_backup()
        #time.sleep(1)

    
        
    def test_a_fullbackup_jewel(self):
        try:
            self.assertTrue(are_dir_trees_equal(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel"),
                                                    os.path.join(os.path.dirname(__file__),"unitTestFiles/backupLocation/fullBackup"f"{device_name}/jewel")))
        except FileNotFoundError:
            print("Test A:")
            print("File or Directory not Found")
        else:
            print("Test A:")
            print("everything is fine in Test A")  
            
            
    def test_b_fullbackup_jewel2(self):
        try:
            self.assertTrue(are_dir_trees_equal(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel2"),
                                                os.path.join(os.path.dirname(__file__),"unitTestFiles/backupLocation/fullBackup"f"{device_name}/jewel2")))
        except FileNotFoundError:
            print("Test B:")
            print("File or Directory not Found")
        else:
            print("Test B:")
            print("everything is fine in")    
            
    def test_c_diffBackup_jewel(self):
        try:
            file = open(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel/test1.txt"), "a")
            file2 = open(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel2/test2.txt"), "a")
            try:            
                for i in range(5):
                    file.write("Hello World in test1.txt\n")
                    file2.write("Hello World in test2.txt\n")
                os.utime(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel"))
                os.utime(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel2"))        
            except:
                print("Something with writing or touching")
            else:
                print("Writing and touching managed")
            finally:
                file.close()
                file2.close()
            
        except FileNotFoundError:
            print("Test C:")
            print("File or Directory not Found")
            
       # time.sleep(1)
        self.backup.initialize_backup() 
        #time.sleep(1)
        try:
            self.assertTrue(are_dir_trees_equal(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel")
                            ,os.path.join(os.path.dirname(__file__),"unitTestFiles/backupLocation/"f"diff-{date.now().strftime('%d-%m-%Y-%H-%M')}/jewel")))
        except FileNotFoundError:
            print("Test C:")
            print("File or Directory not Found")
            
        else:
            print("Test C:")
            print("everything is fine")    
            
    def test_d_diffBackup_jewel2(self):
        try:
            self.assertTrue(are_dir_trees_equal(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel2")
                            , os.path.join(os.path.dirname(__file__),"unitTestFiles/backupLocation/"f"diff-{date.now().strftime('%d-%m-%Y-%H-%M')}/jewel2")))
        except FileNotFoundError:
            print("Test D")
            print("File or Directory not Found")
            
        else:
            print("Test C:")
            print("everything is fine")    
        
    @classmethod
    def tearDownClass(cls):
        os.remove("datenbank.db")
        shutil.rmtree(cls.config["destination"][device_name])
        shutil.rmtree(cls.config["restore_destination"][device_name])

   
if __name__ == "__main__":
    unittest.main()