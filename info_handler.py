import os
import subprocess
from datetime import datetime as date
import json
import platform
from wrapper.file_wrapper import Data
import sys
import shutil

json_file_name = os.path.dirname(os.path.abspath(__file__))+"/config.json"
db_log= os.path.dirname(os.path.abspath(__file__))+"/db.log"
tmp_db= os.path.dirname(os.path.abspath(__file__))+"/tmp.db"


def get_metadata(filepth: str):
    try:
        stats = os.stat(filepth)
    #needed because sometimes the OS cannot find the symlink via stats
    except FileNotFoundError:
        stats = os.lstat(filepth)

    checksum = get_hash(filepth)
    size = stats.st_size / 1024  # file size in kb
    birth = date.fromtimestamp(stats.st_ctime)
    modify = date.fromtimestamp(stats.st_mtime)
    file_obj = Data(filepth, checksum, size, birth, modify)
    return file_obj


def get_json_info(device_name=platform.node()):
    try:
        with open(json_file_name) as f:
            config = json.load(f)
            check_destination_path_exists(config,"backup", "destination", device_name)
            check_destination_path_exists(config,"restore", "restore_destination", device_name)
            check_str_list_info_from_config("jewel_sources", device_name,config, device_name)
            check_str_list_info_from_config("blacklist","directories",config,device_name)
            check_str_list_info_from_config("blacklist", "extensions",config,device_name)
            check_str_list_info_from_config("blacklist", "files",config,device_name)


    except json.decoder.JSONDecodeError:
        print("There is a form error in the config.json.")
        sys.exit()
    return config


def check_destination_path_exists(config, purpose:str, property:str, device_name:str):

    try:
        destination = check_str_info_from_config(property, device_name,config,device_name)

        #print("creating "+ purpose +" in: "+destination)
        os.makedirs(destination, exist_ok=True)
        if not(os.path.exists(destination)):
           #print("Creating " + purpose +"-destination directory failed")
            pass
        if not(destination.startswith("/")):
            #print("Created "+ purpose +"-destination directory is realtive")
            pass
 
    except PermissionError:
        print("You do not have the necessary permission to create the "+ purpose +" folder "+ get_json_info()[property][device_name]+".")
        sys.exit()
    except FileNotFoundError:
        print("The Path in " + property +" could not be found nor be created. Please check the " + property +" path of the device " + device_name)
        sys.exit()
    

# Description:  Generate a SHA-1 Hash based on the content of a file.
# Input:        Total path of a file as a String. Example: "home/user/directory/file.txt"
# Output:       20 bytes (40 characters) large SHA-1 Hash as a String. Example: "da39a3ee5e6b4b0d3255bfef95601890afd80709"
def get_hash(total_file_path: str):
    try:
        file_name = total_file_path.split('/')[-1]
        file_path = '/'.join(total_file_path.split('/')[:-1])
        bash_output = subprocess.run(f'openssl dgst -sha1 "{file_name}"', shell=True, cwd=file_path, stdout=subprocess.PIPE)
        hash = str(bash_output.stdout.decode()).replace("\n","")[-40:]
        return hash
    except:
        print(f'\nError in function "get_hash": Hash couldn\'t be generated\n'
              f'Input of the function: {total_file_path}\n'
              f'Extracted file path: {file_path}\n'
              f'Extracted file name: {file_name}')
        sys.exit()


def check_str_info_from_config(property:str, key:str,config,device_name:str, ):
    value = check_info_from_config(property,key, config, device_name)
    if isinstance(value,str):
        return value
    else: 
        print("The corresponding Value of the Key in the " + property + " table has to be a String. For Example:\n \"myPC\": \"/home/username/backupLocation\"")
        sys.exit()


def check_str_list_info_from_config(property:str, key:str, config, device_name:str):
    value = check_info_from_config(property,key,config,device_name)
    if isinstance(value,list) and all(isinstance(n, str) for n in value):
        return value
    else:
        print("The corresponding Value of the Key in the " + property + " table has to be a List of Strings.")
        sys.exit()


def check_info_from_config(property:str, key:str, config, device_name):
    try: 
        return config[property][key] 
    except KeyError:
        print("Your Computer \""+device_name+"\" was not found as a key in the "+ property + " table of the config.json.\nOr the property '" + property +"' was deleted. Please create the property.")
        sys.exit()
    except json.decoder.JSONDecodeError:
        print("There is a form error in the config.json.")
        sys.exit()

def validate_date_format(date_var:str, format:str):
    res = True
    try:
        res = bool(date.strptime(date_var, format))
    except:
        res = False
    return res



def check_db_hash(backup_path:str, backup_name:str, test=False):
    """Checks if the old hash of the database and resets the backups and the database to the previous state if the old and new database hash do not match.
        
        Args:
            backup_path: the path where the backup for the device is located
            backup_name: the current name of the backup folder
            test: bool if it's a test"""

    log_file = None
    # Checks if a log file for database exist, when not will create it after if. 
    if  os.path.exists(backup_path + "/" + "db.log"):

            # Reads file and checks if the hash is right and replace by false datenbank.db with tmp.db and the last backup folder will be deleted.
            log_file  = open(backup_path + "/" + "db.log", "r")
            if os.stat(backup_path + "/" + "db.log").st_size != 0:
                lines = log_file.readlines()
                old_hash = lines[0].rstrip()
                current_hash = get_hash(backup_path + "/" + "datenbank.db")
                log_file.close()
               
                if old_hash != current_hash:
                    if not os.path.exists(backup_path + "/" + "tmp.db"):
                        print("The backup database was corrupted and could not be restored, because the file tmp.db could not be found.")
                        print("Please delete the specific backup folder and start from scratch or add the file tmp.db into: "+ backup_path + ".")
                        sys.exit()
                    else:
                        os.remove(backup_path + "/" + "datenbank.db") 
                        os.rename(backup_path + "/" + "tmp.db", backup_path + "/" + "datenbank.db")
                        if len(lines) >1: 
                            shutil.rmtree(backup_path + "/" + lines[1].rstrip(), ignore_errors=True)
                            # If the first backup failed the db.log and datenbank.db must be removed.
                            if not lines[1].rstrip().startswith("diff") and not test:
                                os.remove(backup_path + "/datenbank.db")
                                os.remove(backup_path + "/db.log")
                                print("The database changed before the first backup process could be completed and reset the backup.")
                                sys.exit()
                            print("The database changed before the backup process could be completed and the old version of the database and backup was restored.")
                            log_file  = open(backup_path + "/" + "db.log", "w")
                            log_file.write(get_hash(backup_path + "/" + "datenbank.db") + "\n" + backup_name)
                            log_file.close()
                            if not test: sys.exit()  

                        else:
                             print("The backup database was corrupted and could not be restored, because db.log got also corrupted.")
                             print("Please delete the specific backup folder and start from scratch.")
                             sys.exit()
                        
            else:
                 print("The backup database was corrupted and could not be restored.")
                 print("Please delete the specific backup folder and start from scratch.")
                 sys.exit()

    # Creates a new tmp.db and delete the old one if it is still there.
    # Overrides or creates a new db.log
    if os.path.exists(backup_path + "/" + "tmp.db"):  os.remove(backup_path + "/" + "tmp.db") 
    log_file  = open(backup_path + "/" + "db.log", "w")
    log_file.write(get_hash(backup_path + "/" + "datenbank.db") + "\n" + backup_name)
    log_file.close()
    status = subprocess.call('cp ' + backup_path + '/' + 'datenbank.db ' + backup_path + '/' +  'tmp.db', shell=True) 


def update_db_hash(backup_path:str, backup_name:str):
    """Writes the database hash and the current backup name into the db.log file, also it deletes the tmp.db.
        
        Args:
            backup_path: the path where the backup for the device is located
            backup_name: the current name of the backup folder"""


    log_file  = open(backup_path + "/" + "db.log", "w")
    log_file.write(get_hash(backup_path + "/" + "datenbank.db") + "\n" + backup_name)
    log_file.close()
    if os.path.exists(backup_path + "/" +"tmp.db"):  os.remove(backup_path +"/" +"tmp.db") 


def reset_backup(device=platform.node()):
    """Resets the backup of a device.
        
        Args:
            device: the device where the backup is on"""


    reset_path = get_json_info()['destination'][device]
    shutil.rmtree(reset_path, ignore_errors=True)
    print("The reset was successfully performed for the device: " + device+ ".")

