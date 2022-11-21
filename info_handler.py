import os
import subprocess
from datetime import datetime as date
import json
import platform
from wrapper.file_wrapper import Data
import sys

json_file_name = "config.json"


def get_metadata(filepth: str):
    stats = os.stat(filepth)
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
