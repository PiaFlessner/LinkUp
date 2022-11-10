import os
import subprocess
from datetime import datetime as date
import hashlib
import json
import platform
from wrapper.file_wrapper import Data
import subprocess
import sys

json_file_name = "config.json"


def get_metadata(filepth: str):
    stats = os.stat(filepth)
    checksum = calculate_checksum(filepth)
    # checksum = get_hash(filepth)
    size = stats.st_size / 1024  # file size in kb
    birth = date.fromtimestamp(stats.st_ctime)
    modify = date.fromtimestamp(stats.st_mtime)
    file_obj = Data(filepth, checksum, size, birth, modify)
    return file_obj


def calculate_checksum(filename: str):
    with open(filename, "rb") as f:
        file_as_bytes = f.read()
        readable_hash = hashlib.sha256(file_as_bytes).hexdigest()
    return readable_hash


def get_json_info():
    with open(json_file_name) as f:
        config = json.load(f)

    return config


def check_destination_path_exists():

    try:
        config = get_json_info()
        destination = get_str_info_from_config("destination", platform.node())

        print("creating backup in: "+destination)
        os.makedirs(destination, exist_ok=True)
        if not(os.path.exists(destination)):
           print("Backup-Zielordner erstellen hat nicht geklappt")
        if not(destination.startswith("/")):
            print("Der erstellte Backup-Zielordner ist relativ!")
 
    except PermissionError:
        print("You do not have the necessary permission to create the backup folder "+ get_json_info()["destination"][platform.node()]+".")
        sys.exit()
    except FileNotFoundError:
        print("The Path in Destination could not be found nor be created. Please check the destination path of the device " +platform.node())
        sys.exit()
    


def get_hash(total_file_path: str):
    file_name = total_file_path.split('/')[-1]
    file_path = '/'.join(total_file_path.split('/')[:-1])
    output = subprocess.run(f'openssl dgst -sha1 {file_name}', shell=True, cwd=file_path, stdout=subprocess.PIPE)
    hash = str(output.stdout.decode()).split('= ')[1]
    return hash


def get_str_info_from_config(property:str, key:str):
    value = get_info_from_config(property,key)
    try: 
         if isinstance(value,str):
            return value
         else: raise TypeError() 
    except TypeError:
        print("The corresponding Value of the Key in the " + property + " table has to be a String. For Example:\n \"myPC\": \"/home/username/backupLocation\"")
        sys.exit()


def get_str_list_info_from_config(property:str, key:str):
    value = get_info_from_config(property,key)
    try: 
         if isinstance(value,list):
            return value
         else: raise TypeError() 
    except TypeError:
        print("The corresponding Value of the Key in the " + property + " table has to be a String List.")
        sys.exit()
    


def get_info_from_config(property:str, key:str):
    config = get_json_info()
    try: 
        return config[property][key] 
    except KeyError:
        print("Your Computer \""+platform.node()+"\" was not found as a key in the "+ property + " table of the config.json.")
        sys.exit()
    except json.JSONDecodeError:
        print("There is a form error in the config.json.")
        sys.exit()
