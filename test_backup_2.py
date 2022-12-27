import pathlib
import unittest
from backup import Backup
import info_handler as ih
import os
import filecmp
from filecmp import dircmp
from filecmp import cmpfiles
from datetime import datetime as date
import shutil
import subprocess 
from subprocess import run
import argparse
import test_backup_2_insert
from os import walk
    
test_backup_2_insert.insert_for_test_backup_2()

#device_name = platform.node()
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
        global directory_count
        global data_count
        global data_size
        global storage_unit

        # os.makedirs("unitTestFiles/jewel",exist_ok=True)
        # cls.daten = datenbank.Datenbank()
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
        os.utime(f"{cls.workingDirectory}/test_Files_Backup/jewel3")

        cls.backup = Backup(jewel_list, cls.workingDirectory + '/' + cls.config["destination"][device_name], True)
        cls.backup.initialize_backup(1)
        # process = subprocess.run(
        #     ["python3", "./execute.py", "backup"])
     
        parser = argparse.ArgumentParser(description = "whether the pipeline executes")
        
        parser.add_argument("-p", nargs='?', const = True, default = False, help = "to start it in pipeline", 
                            dest="pipeline")
        args = parser.parse_args()
        
        # for the pipline
        if(args.pipeline):
            
            directory_count = 3
            data_count = 3
            storage_unit = 'b'
            data_size = 1
        # for user    
        else:
            while(True):
                directory_count = input("enter desired number of folders\n")
                try:
                    directory_count = int(directory_count)
                    if(directory_count >= 1):
                        break
                    else:
                        print("it has to be greater than 0")
                except:
                    print("must be an integer")
                    
                fail_condition = input("do you want to quit the test ? press q or anyting else for continue\n")
                if(fail_condition == 'q'):
                    cls.skipTest("test skipped")
            
            while(True):    
                data_count = input("enter desired number of data files\n")
                try:
                    data_count = int(data_count)
                    if(data_count >= 1):
                        break
                    else:
                        print("it has to be greater than 0")
                except:
                    print("must be an integer")
                fail_condition = input("do you want to quit the test ? press q or anyting else for continue\n")
                if(fail_condition == 'q'):
                    cls.skipTest("test skipped")
            
            while(True):
                storage_unit = input("should the data in byte (b) or gigabyte (g) ?\n")
                if(storage_unit not in ['g', 'b']):
                    print("you have to press g for GigaByte or b Byte")
                else:
                    break
                fail_condition = input("do you want to quit the test ? press q or anyting else for continue\n")
                if(fail_condition == 'q'):
                    cls.skipTest("test skipped")
            
            while(True):    
                storage_unit = "Gigabyte" if storage_unit == 'g' else 'Byte'
                data_size = input("enter desired data size in "f"{storage_unit}\n")
                try:
                    data_size = int(data_size)
                    if(data_size >= 0):
                        
                        if(storage_unit == 'Gigabyte'):
                            data_size = data_size * 1000000000
                            print("in g")
                        break
                    else:
                        print("it has to be greater than 0")
                except:
                    print("must be an integer")
                fail_condition = input("do you want to quit the test ? press q or anyting else for continue\n")
                if(fail_condition == 'q'):
                    cls.skipTest("test skipped")
  
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
    # test for blacklist
    def test_c_fullbackup_blacklist(self):
        config = ih.get_json_info(device_name)
        working_directory = str(pathlib.Path(__file__).parent.resolve())
        
        blacklist_dirs = config["blacklist"]["directories"]
        blacklist_files = config["blacklist"]["files"]

        print(blacklist_dirs)
        print(blacklist_files)
        
        for(root, dir_names, file_names) in walk(working_directory + '/'
                                                            + "test_Files_Backup/backup_Location/fullBackup"f"{device_name}/jewel3"):
            
            for file in file_names:
                to_cmp_file = os.path.basename(file)
                for black_file in blacklist_files:
                    if black_file == to_cmp_file:
                        self.assertTrue(False)
            
            for dir in dir_names:
                to_cmp_dir = os.path.basename(dir)
                for black_dir in blacklist_dirs:
                    if to_cmp_dir == black_dir:
                        self.assertTrue(False)
        self.assertTrue(True)        
                
        
    def test_d_diffBackup_jewel(self):
        subprocess.check_call(["./test_Files_Backup/execScripts.sh", str(directory_count), str(data_count), str(data_size)])  
   
        os.utime(f"{str(pathlib.Path(__file__).parent.resolve())}/test_Files_Backup/jewel")
        os.utime(f"{str(pathlib.Path(__file__).parent.resolve())}/test_Files_Backup/jewel2")
        os.utime(f"{str(pathlib.Path(__file__).parent.resolve())}/test_Files_Backup/jewel3")
        
        
       # time.sleep(1)
        #global date_Format
        #date_Format = date.now().strftime('%d-%m-%Y-%H-%M')
        self.backup.initialize_backup(1) 
        # process = subprocess.run(
        #     ["python3", "./execute.py", "backup"])
        
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
        os.remove("./test_Files_Backup/backup_Location/db.log")
        
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
   # unittest.main()
    runner = unittest.TextTestRunner()
    itersuite = unittest.TestLoader().loadTestsFromTestCase(TestBackup)
    runner.run(itersuite)