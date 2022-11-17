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

#
#class TestBackup(unittest.TestCase):
#    global backup
#    config = ih.get_json_info()
#    backup = Backup(config["jewel_sources"][device_name], config["destination"][device_name],True)
#    #erstellen von Fullbackup, wenn nicht keins vorhanden ist
#    if not os.path.exists(os.path.join(os.path.dirname(__file__), "unitTestFiles/backupLocation/fullBackup"f"{device_name}")): 
#        backup.initialize_backup()
#    
#    
#         
#    def test_a_fullbackup_jewel(self):
#    
#        self.assertTrue(are_dir_trees_equal(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel"),
#                                                    os.path.join(os.path.dirname(__file__),"unitTestFiles/backupLocation/fullBackup"f"{device_name}/jewel")))
#    
#    def test_b_fullbackup_jewel2(self):
#    
#        self.assertTrue(are_dir_trees_equal(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel2"),
#                                             os.path.join(os.path.dirname(__file__),"unitTestFiles/backupLocation/fullBackup"f"{device_name}/jewel2")))
#   
#  
#    def test_c_diffBackup_jewel(self):
#       
#        file = open(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel/test1.txt"), "a")
#        file2 = open(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel2/test2.txt"), "a")
#        
#        for i in range(5):
#            file.write("Hello World in test1.txt\n")
#            file2.write("Hello World in test2.txt\n")
#        file.close()
#        file2.close()
#        backup.initialize_backup() 
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
#    #def __del__(self):
#        #os.remove("datenbank.db")
#        #os.remove(self.config["destination"][device_name])
#        #os.remove(self.config["restore_destination"][device_name])


class TestRestore(unittest.TestCase):

    daten = datenbank.Datenbank()
    config = ih.get_json_info(device_name)
    backup = Backup(config["jewel_sources"][device_name], config["destination"][device_name], True)
    backup.initialize_backup()

    def test_a_restore_Jewel_only_Fullbackup(self):
        restoreDay = date.today()
        self.daten.get_restore_Jewel(restoreDay, 1)

    def __del__(self):
        os.remove("datenbank.db")
        shutil.rmtree(self.config["destination"][device_name])
        shutil.rmtree(self.config["restore_destination"][device_name])

    
        
if __name__ == "__main__":
    unittest.main()
