import os
from zfec import easyfec
from zfec import filefec
from datenbank import Datenbank
from datenbank import Blob
from resFile import resFile
import info_handler

#Reed-Solomon parameter. If they change, they can't decode old data anymore
k=5
m=8

class Repair: # TODO try zfec shell
    """_summary_

    Returns:
        _type_: _description_
    """
    def __init__(self): #, blob : Blob
        self.daten = Datenbank()# TODO kommentare schreiben
        self.blobs = self.daten.get_all_Blobs()
        self.path_of_repair_information = self.daten.database_path.rsplit("/",1)[0]+"/Reed-Solomon" # put it next to the database for now... or get the backup path from the config
        self.destination=self.path_of_repair_information
        os.makedirs(self.destination, exist_ok=True)
        
    def create_repair_data(self, blob:Blob, _overwrite: bool=False):
        file_io = open(blob.store_destination, "rb")
        file_size = int(1024*blob.fileSize)  # TODO check for rounding errors
        subdirectory_name="/RS_"+str(blob.id)
        reed_solomon_path_for_this_file=self.path_of_repair_information+subdirectory_name

        os.makedirs(reed_solomon_path_for_this_file, exist_ok=True)
        filefec.encode_to_files(file_io, file_size, reed_solomon_path_for_this_file, k=k, m=m,prefix="RS",overwrite=_overwrite)
        blob.reed_solomon_path=reed_solomon_path_for_this_file
        self.daten.update_blobs_after_repair([blob])
    
    def repair_file(self, res_file : resFile, _verbose: bool=False)-> None:
        """this method repairs the resFile with the help of the 

        Args:
            res_file (resFile): _description_
            _verbose (bool, optional): _description_. Defaults to False.
        """
        file_to_write = open(res_file.backup_location, "wb") 
        files_to_read=[]
        for i in range(m): #the zfec program creates
            file_name=res_file.reed_solomon_path+"/RS."+str(i)+"_"+str(m)+".fec"
            files_to_read.append(open(file_name, "rb"))
        filefec.decode_from_files(file_to_write,files_to_read,verbose=_verbose) # TODO check if file has to be deleted

    def check_if_file_is_broken(self, resFile:resFile) -> bool:
        my_hash=info_handler.get_hash(resFile.backup_location)
        return my_hash != resFile.hash

