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
    try:
        with open(json_file_name) as f:
            config = json.load(f)
            check_destination_path_exists(config,"backup", "destination")
            check_destination_path_exists(config,"restore", "restore_destination")
            check_str_list_info_from_config("jewel_sources", platform.node(),config)
            check_str_list_info_from_config("blacklist","directories",config)
            check_str_list_info_from_config("blacklist", "extensions",config)
            check_str_list_info_from_config("blacklist", "files",config)


    except json.decoder.JSONDecodeError:
        print("There is a form error in the config.json.")
        sys.exit()
    return config


def check_destination_path_exists(config, purpose:str, property:str):

    try:
        destination = check_str_info_from_config(property, platform.node(),config)

        print("creating "+ purpose +" in: "+destination)
        os.makedirs(destination, exist_ok=True)
        if not(os.path.exists(destination)):
           print("Creating " + purpose +"-destination directory failed")
        if not(destination.startswith("/")):
            print("Created "+ purpose +"-destination directory is realtive")
 
    except PermissionError:
        print("You do not have the necessary permission to create the "+ purpose +" folder "+ get_json_info()[property][platform.node()]+".")
        sys.exit()
    except FileNotFoundError:
        print("The Path in " + property +" could not be found nor be created. Please check the " + property +" path of the device " +platform.node())
        sys.exit()
    


def get_hash(total_file_path: str):
    file_name = total_file_path.split('/')[-1]
    file_path = '/'.join(total_file_path.split('/')[:-1])
    output = subprocess.run(f'openssl dgst -sha1 {file_name}', shell=True, cwd=file_path, stdout=subprocess.PIPE)
    hash = str(output.stdout.decode()).split('= ')[1]
    return hash


def check_str_info_from_config(property:str, key:str,config):
    value = check_info_from_config(property,key, config)
    if isinstance(value,str):
        return value
    else: 
        print("The corresponding Value of the Key in the " + property + " table has to be a String. For Example:\n \"myPC\": \"/home/username/backupLocation\"")
        sys.exit()


def check_str_list_info_from_config(property:str, key:str, config):
    value = check_info_from_config(property,key,config)
    if isinstance(value,list) and all(isinstance(n, str) for n in value):
        return value
    else:
        print("The corresponding Value of the Key in the " + property + " table has to be a List of Strings.")
        sys.exit()


def check_info_from_config(property:str, key:str, config):
    try: 
        return config[property][key] 
    except KeyError:
        print("Your Computer \""+platform.node()+"\" was not found as a key in the "+ property + " table of the config.json.\nOr the property '" + property +"' was deleted. Please create the property.")
        sys.exit()
    except json.decoder.JSONDecodeError:
        print("There is a form error in the config.json.")
        sys.exit()
