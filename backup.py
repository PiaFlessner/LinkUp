from genericpath import isfile
import os
import hashlib
import pathlib
import sys
import file as fi
import argparse
import datetime

#Mirco: Methode um Metadaten der Datei zu erhalten
#gibt ein Object vom Typ File zurück. Getter sind geschrieben, können in Datenbank importiert werden
def get_metadata(filepath:str):
    stats = os.stat(filepath)
    checksum = calculate_checksum(filepath)
    size = stats.st_size / 1024 #file size in kb
    birth = datetime.datetime.fromtimestamp(stats.st_ctime)
    modify = datetime.datetime.fromtimestamp(stats.st_mtime)
    obj = fi.File(filepath, checksum, size, birth, modify)
    return obj

def calculate_checksum(filename:str):
    with open(filename, "rb") as f:
        file_as_bytes = f.read()
        readable_hash = hashlib.sha256(file_as_bytes).hexdigest()
    return readable_hash


#Hier startet das Programm
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dies ist eine Beschreibung des Programms", epilog="Dies ist der Epilog")
    parser.add_argument('-f',type=str, help='File input')
    args = parser.parse_args()
    arglist = sys.argv
    if arglist[1] == '-f':
        filepath = arglist[2]
        #filepath = "/home/mirco/Gitlab/ProjektgruppeBackup/projektgruppe/test.txt"
        data = pathlib.Path(filepath)
        if data.exists():
            file_obj = get_metadata(filepath)
            print(file_obj.get_f_hash())
            filesize = str(file_obj.get_f_size())
            print(filesize, "kb")
            print(file_obj.get_creation_date())
            print(file_obj.get_modify())
        else:
            print("No file")
    else:
        print("unknown option")
    