import unittest
from backup import Backup
import info_handler as ih
import platform
import os
from filecmp import dircmp
from filecmp import cmpfiles
from datetime import datetime as date


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
    global backup
    backup = Backup(ih.get_str_list_info_from_config("jewel_sources", platform.node()), ih.get_str_info_from_config("destination", platform.node()))
    #erstellen von Fullbackup, wenn nicht keins vorhanden ist
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "unitTestFiles/backupLocation/fullBackup"f"{platform.node()}")): 
        backup.initialize_backup()
    
    
         
    def test_a_fullbackup_jewel(self):
    
        self.assertTrue(are_dir_trees_equal(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel"),
                                                    os.path.join(os.path.dirname(__file__),"unitTestFiles/backupLocation/fullBackup"f"{platform.node()}/jewel")))
    
    def test_b_fullbackup_jewel2(self):
    
        self.assertTrue(are_dir_trees_equal(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel2"),
                                             os.path.join(os.path.dirname(__file__),"unitTestFiles/backupLocation/fullBackup"f"{platform.node()}/jewel2")))
   
  
    def test_c_diffBackup_jewel(self):
       
        file = open(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel/test1.txt"), "a")
        file2 = open(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel2/test2.txt"), "a")
        
        for i in range(5):
            file.write("Hello World in test1.txt\n")
            file2.write("Hello World in test2.txt\n")
        file.close()
        file2.close()
        backup.initialize_backup() 
        
        
        self.assertTrue(are_dir_trees_equal(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel")
                        ,os.path.join(os.path.dirname(__file__),"unitTestFiles/backupLocation/"f"diff-{date.now().strftime('%d-%m-%Y-%H-%M')}/jewel")))
        
    def test_d_diffBackup_jewel2(self):

        self.assertTrue(are_dir_trees_equal(os.path.join(os.path.dirname(__file__), "unitTestFiles/jewel2")
                        , os.path.join(os.path.dirname(__file__),"unitTestFiles/backupLocation/"f"diff-{date.now().strftime('%d-%m-%Y-%H-%M')}/jewel2")))
        
if __name__ == "__main__":
    unittest.main()
