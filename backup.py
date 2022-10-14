from genericpath import isfile
import os
import hashlib
import file as fi



#Mirco: Methode um Metadaten der Datei zu erhalten
def get_metadata(filepath:str):
    stats = os.stat(filepath)
    checksum = calculate_checksum(filepath)
    return 0

def calculate_checksum(filename:str):
    with open(filename, "rb") as f:
        file_as_bytes = f.read()
        readable_hash = hashlib.sha256(file_as_bytes).hexdigest()
    return readable_hash

if __name__ == "__main__":
    filepath = 'README.md'
    if os.path.isfile(filepath):
        file_obj = get_metadata(filepath)
    else:
        print("No file")
    print("Hello World")
    print ("bye")
    