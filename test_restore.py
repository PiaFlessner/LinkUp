import argparse
import pathlib
import unittest
from backup import Backup
import info_handler as ih
import os
from filecmp import dircmp
from filecmp import cmpfiles
from datetime import date

import shutil
import subprocess
import platform
import test_restore_insert
device_name = platform.node()
test_restore_insert.insert_for_test_restore()
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
    
class TestRestore(unittest.TestCase):
   
    @classmethod
    def setUpClass(cls):
        global directory_count
        global data_count
        global data_size
        global storage_unit
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
        os.utime(f"{cls.workingDirectory}/test_Files_Backup/jewel3")
        
        
        cls.backup = Backup(jewel_list, cls.workingDirectory + '/' + cls.config["destination"][device_name], False)
        cls.backup.initialize_backup(1)
        # process = subprocess.Popen(
        #     ["python3", "execute.py", "backup"], stdout=subprocess.PIPE)  # stdout is just to get rid of the prints
        # process.wait()
        # process.stdout.close()
       
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
        
    def test_a_Restore_Jewel(self):
        # change Jewel and Jewel2 and Create a Diff Backup
        subprocess.check_call(["./test_Files_Backup/execScripts.sh", str(directory_count), str(data_count), str(data_size)])  
   
        os.utime(f"{str(pathlib.Path(__file__).parent.resolve())}/test_Files_Backup/jewel")
        os.utime(f"{str(pathlib.Path(__file__).parent.resolve())}/test_Files_Backup/jewel2")
        os.utime(f"{str(pathlib.Path(__file__).parent.resolve())}/test_Files_Backup/jewel3")
        
        curr_date = str(date.today())
        # process = subprocess.Popen(
        #     ["python3", "execute.py", "backup"], stdout=subprocess.PIPE)  # stdout is just to get rid of the prints
        # process.wait()
        self.backup.initialize_backup(1)
        for i in range(3):
            process = subprocess.Popen(
                ["python3", "execute.py", "restore", "-J", str(i + 1), curr_date], stdout=subprocess.PIPE)  # stdout is just to get rid of the prints
            process.wait()
            process.stdout.close()
            
        try:
            self.assertTrue(are_dir_trees_equal(str(pathlib.Path(__file__).parent.resolve()) + '/' + "test_Files_Backup/jewel",
                                                str(pathlib.Path(__file__).parent.resolve()) + '/' + "test_Files_Backup/restore_Location/jewel"))
        except FileNotFoundError:
            print("Jewel:")
            print("File or Directory not Found")
            self.assertTrue(False)
    def test_b_Restore_Jewel2(self):                    
        try:
            self.assertFalse(are_dir_trees_equal(str(pathlib.Path(__file__).parent.resolve()) + '/' + "test_Files_Backup/jewel2",
                                                str(pathlib.Path(__file__).parent.resolve()) + '/' + "test_Files_Backup/restore_Location/jewel2"))
        except FileNotFoundError:
            print("Jewel2:")
            print("File or Directory not Found")
            self.assertTrue(False)
            
    def test_c_Restore_Jewel3(self):                    
        try:
            self.assertFalse(are_dir_trees_equal(str(pathlib.Path(__file__).parent.resolve()) + '/' + "test_Files_Backup/jewel3",
                                                str(pathlib.Path(__file__).parent.resolve()) + '/' + "test_Files_Backup/restore_Location/jewel3"))
        except FileNotFoundError:
            print("Jewel3:")
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
    itersuite = unittest.TestLoader().loadTestsFromTestCase(TestRestore)
    runner.run(itersuite)