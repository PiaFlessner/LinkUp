import pathlib

import unittest
from backup import Backup
import info_handler as ih

import os
from filecmp import dircmp
from filecmp import cmpfiles
from datetime import datetime as date
import datenbank
import shutil
import subprocess 
from subprocess import run

device_name = "testCases"

def are_dir_trees_equal(dir1, dir2):
    
    dirs_cmp = dircmp(dir1, dir2) 
    
    if len(dirs_cmp.left_only) > 0 or len(dirs_cmp.right_only) > 0 or len(dirs_cmp.funny_files) > 0: # überprüfen, ob unterschiedliche Files oder Dirs vom Namen her
                                                                                                     #existieren 
        return False                                                                                 
    
    (match, mismatch, errors) =  cmpfiles(dir1, dir2, dirs_cmp.common_files, shallow=False)
    
    if len(mismatch) > 0 or len(errors) > 0:    # nach Inhalt überprüfen
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
        #os.makedirs("unitTestFiles/jewel",exist_ok=True)
        #cls.daten = datenbank.Datenbank()
        cls.config = ih.get_json_info(device_name)
        cls.workingDirectory = str(pathlib.Path(__file__).parent.resolve())
        
        jewel_list = cls.config["jewel_sources"][device_name]

        for (index, element) in enumerate(jewel_list): 
            jewel_list[index] = cls.workingDirectory + element
           
       
        with open("./test_Files_Backup/init.sh", 'rb') as file:
             script = file.read()
        subprocess.call(script, shell=True)  

        
        os.utime(f"{cls.workingDirectory}/test_Files_Backup/jewel")
        os.utime(f"{cls.workingDirectory}/test_Files_Backup/jewel2")

        
        cls.backup = Backup(jewel_list, cls.workingDirectory + '/' + cls.config["destination"][device_name], True)
        cls.backup.initialize_backup(2)
        

    
    def test_a_fullbackup_jewel(self):
      
        try:
            self.assertTrue(are_dir_trees_equal(str(pathlib.Path(__file__).parent.resolve()) + '/' + "test_Files_Backup/jewel",
                                                    str(pathlib.Path(__file__).parent.resolve()) + '/' + "test_Files_Backup/backup_Location/fullBackup"f"{device_name}/jewel"))
        except FileNotFoundError:
            print("Test A:")
            print("File or Directory not Found")
            self.assertTrue(False)
            
    def test_b_fullbackup_jewel2(self):
      
        try:
            self.assertTrue(are_dir_trees_equal(str(pathlib.Path(__file__).parent.resolve()) + '/' + "test_Files_Backup/jewel2",
                                                str(pathlib.Path(__file__).parent.resolve()) + '/' + "test_Files_Backup/backup_Location/fullBackup"f"{device_name}/jewel2"))
        except FileNotFoundError:
            print("Test B:")
            print("File or Directory not Found")
            self.assertTrue(False)
    # def test_c_fullbackup_special_Files(self):
    #     try:
    #         self.assertTrue(are_dir_trees_equal(str(pathlib.Path(__file__).parent.resolve()) + '/' + "test_Files_Backup/jewel3",
    #                                             str(pathlib.Path(__file__).parent.resolve()) + '/' + "test_Files_Backup/backup_Location/fullBackup"f"{device_name}/jewel3"))
    #     except FileNotFoundError:
    #         print("Test C:")
    #         print("File or Directory not Found")
    #         self.assertTrue(False)
    def test_d_diffBackup_jewel(self):
        
        with open('./test_Files_Backup/execScripts.sh', 'rb') as file:
             script = file.read()
        subprocess.call(script, shell=True)  
        
        os.utime(f"{str(pathlib.Path(__file__).parent.resolve())}/test_Files_Backup/jewel")
        os.utime(f"{str(pathlib.Path(__file__).parent.resolve())}/test_Files_Backup/jewel2")
        os.utime(f"{str(pathlib.Path(__file__).parent.resolve())}/test_Files_Backup/jewel3")
        
        
       # time.sleep(1)
        #global date_Format
        #date_Format = date.now().strftime('%d-%m-%Y-%H-%M')
        self.backup.initialize_backup(2) 
        
        # time.sleep(1)
        global diffPath
        result = run(["find ./test_Files_Backup/backup_Location -type d -name 'diff*'"], capture_output=True, shell=True)
        diffPath = str(result.stdout)
       
        diffPath = diffPath[3:len(diffPath) - 3]
       
        try:
            self.assertTrue(are_dir_trees_equal(str(pathlib.Path(__file__).parent.resolve()) + '/' + "test_Files_Backup/jewel/make_Data_Dir"
                   ,str(pathlib.Path(__file__).parent.resolve()) + diffPath + "/jewel/make_Data_Dir"))
        except FileNotFoundError:
            print("Test D:")
            print("File or Directory not Found")
            self.assertTrue(False)
            
            
    def test_e_diffBackup_jewel2(self):
       
        try:
            self.assertTrue(are_dir_trees_equal(str(pathlib.Path(__file__).parent.resolve()) + '/' + "test_Files_Backup/jewel2/data_And_Link_Dir"
                            , str(pathlib.Path(__file__).parent.resolve()) + diffPath + "/jewel2/data_And_Link_Dir"))
        except FileNotFoundError:
            print("Test E")
            print("File or Directory not Found")
            self.assertTrue(False)
      
            
    @classmethod
    def tearDownClass(cls):
        os.remove("./test_Files_Backup/backup_Location/datenbank.db")
        
        
        rel_path = cls.config["destination"][device_name]
   
        for root, dirs, files in os.walk(cls.workingDirectory + '/' + rel_path, topdown=False):
            for name in dirs:
                shutil.rmtree(os.path.join(root, name))
                
   
        shutil.rmtree(cls.config["restore_destination"][device_name])
        
       
        jewel_list = cls.config["jewel_sources"][device_name]

        for element in jewel_list:    
            for root, dirs, files in os.walk(element, topdown=False):
                for name in dirs:
                    shutil.rmtree(os.path.join(root, name))
                for name in files:
                    os.remove(os.path.join(root, name))
                    
            

   
if __name__ == "__main__":
    unittest.main()