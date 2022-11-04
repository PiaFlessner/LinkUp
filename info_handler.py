import os
from datetime import datetime as date
import file as mirco_file
import hashlib
import json

json_file_name = "config.json"


def get_metadata(filepth: str):
    stats = os.stat(filepth)
    checksum = calculate_checksum(filepth)
    size = stats.st_size / 1024  # file size in kb
    birth = date.fromtimestamp(stats.st_ctime)
    modify = date.fromtimestamp(stats.st_mtime)
    file_obj = mirco_file.File(filepth, checksum, size, birth, modify)
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