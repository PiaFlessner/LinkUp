from datenbank import *
from datetime import datetime 
from prettytable import PrettyTable

class ShowTables:

    """Class ShowTables. Shows the following objects: Jewels, Blobs, Files, skipped Files
    
    ShowTables shows objectes with different verbose levels.
    Level 0: short display
    Level 1: medium display
    Level 2: full display
    
    """


    def __init__(self):
        """Constructor"""
        self.daten = Datenbank()


    def generate_jewel_table(self, jewels:list[Jewel], verbose_level:int) ->None:
        """Adjusts the jewel table to the verbose level and prints the table.
        
            Args:
                jewels: a list of jewel objects that should be displayed
                verbose_level: the level that should be displayed"""


        table = PrettyTable()
        if verbose_level == 0:
                table.field_names = ["Jewel ID","Monitoring startdate","Source of the jewel"]
                table.align["Jewel ID"] = "l"
                for jewel in jewels:
                     startdate = str(jewel.monitoring_Startdate).split(" ")[0]
                     table.add_row([str(jewel.id), startdate, jewel.jewelSource])

        elif verbose_level == 1:
                table.field_names = ["Jewel ID","Monitoring startdate","Source of the jewel", "Fullbackup source"]
                table.align["Jewel ID"] = "l"
                for jewel in jewels:
                    startdate = str(jewel.monitoring_Startdate).split(".")[0]
                    table.add_row([str(jewel.id), startdate, jewel.jewelSource, jewel.fullbackup_source])

        else:
                table.field_names = ["Jewel ID", "Comment", "Monitoring startdate", "Source of the jewel", "Device name", "Fullbackup source"]
                table.align["Jewel ID"] = "l"
                for jewel in jewels:
                    startdate = str(jewel.monitoring_Startdate)
                    table.add_row([str(jewel.id),jewel.comment, startdate, jewel.jewelSource, jewel.device_name, jewel.fullbackup_source])

        print(table)
        
    
    def generate_file_table(self, files:list[File], verbose_level:int) ->None:
        """Adjusts the file table to the verbose level and prints the table.
        
            Args:
                files: a list of file objects that should be displayed
                verbose_level: the level that should be displayed"""


        table = PrettyTable()
        table.field_names = ["File ID","File versions","File birth"]
        table.align["File ID"] = "l"
        for file in files:
            birth = str(file.birth)
            if verbose_level == 0: birth = birth.split(" ")[0]
            elif verbose_level == 1: birth = birth.split(".")[0]
            table.add_row([file.id, str(len(file.blobs)), birth])

        print(table)


    def generate_blobs_table(self, blobs:list[Blob], verbose_level:int) ->None:
            """Adjusts the blob table to the verbose level and prints the table.
        
            Args:
                blobs: a list of blob objects that should be displayed
                verbose_level: the level that should be displayed"""


            table = PrettyTable()

            if verbose_level == 0:
                table.field_names = ["Blob ID"," File version", "Creationdate", "File ID", "Origin name"]
                table.align["Blob ID"] = "l"
                for blob in blobs:
                    table.add_row([str(blob.id), str(blob.number), str(blob.creationDate).split(" ")[0], blob.iD_File, blob.origin_name ])
                print(table)

            elif verbose_level == 1:
                secound_table = PrettyTable()
                table.field_names = ["Blob ID"," File version", "File size in kB", "Creationdate", "File ID"]
                table.align["Blob ID"] = "l"
                secound_table.field_names = ["Blob ID", "Origin name", " Source path", "Store destination "]
                secound_table.align["Blob ID"] = "l"
                for blob in blobs:
                    table.add_row([str(blob.id), str(blob.number), str(blob.fileSize),  str(blob.creationDate).split(".")[0], blob.iD_File])
                    secound_table.add_row([str(blob.id), blob.origin_name, blob.source_path, blob.store_destination])
                print("-------------------------the first part of the blob table.----------------------------------------------------------\n")
                print(table)
                print("\n-------------------------the secound part of the blob table.---------------------------------------------------------\n")
                print(secound_table)
            else: 
                secound_table = PrettyTable()
                table.field_names = ["Blob ID"," File version", "Hash", "File size in kB", "Creationdate", "Modifydate"]
                table.align["Blob ID"] = "l"
                secound_table.field_names = ["Blob ID",  "File ID", "Origin name", " Source path", "Store destination "]
                secound_table.align["Blob ID"] = "l"
                for blob in blobs:
                    table.add_row([str(blob.id), str(blob.number), blob.hash, str(blob.fileSize), str(blob.creationDate), str(blob.modify)])
                    secound_table.add_row([str(blob.id),  blob.iD_File, blob.origin_name, blob.source_path, blob.store_destination])
                print("-------------------------the first part of the blob table.----------------------------------------------------------\n")
                print(table)
                print("\n-------------------------the secound part of the blob table.---------------------------------------------------------\n")
                print(secound_table)
           

    def generate_sfiles_table(self, sfiles:tuple, verbose_level:int) ->None:
             """Adjusts the blob table to the verbose level and prints the table.
        
            Args:
                sfiles: a list of sfiles as tuple that should be displayed
                verbose_level: the level that should be displayed"""


             table = PrettyTable()
             if verbose_level == 0:
                table.field_names = ["File id","Jewel id", "UUID", "Occurance date"]
                table.align["File id"] = "l"
                for file in sfiles:
                    table.add_row([str(file[0]), str(file[1]), file[2], str(file[3]).split(" ")[0]])

             elif verbose_level == 1:
                table.field_names = ["File id","Jewel id", "UUID", "Occurance date", "Reason", "Connected file to jewel"]
                table.align["File id"] = "l"
                for file in sfiles:
                    table.add_row([str(file[0]), str(file[1]), file[2], str(file[3]).split(".")[0], file[5], str(file[7])])
            
             else:
                table.field_names = ["File id","Jewel id", "UUID", "Occurance date", "Hash", "Reason", "Additional information", "Connected file to jewel"]
                table.align["File id"] = "l"
                for file in sfiles:
                    table.add_row([str(file[0]), str(file[1]), file[2], str(file[3]), file[4], file[5], file[6], str(file[7])])
            
             print(table)



    def show_all_jewels(self, verbose_level:int) ->None:
        """Prints all jewels in table form in the console
        
           Args:
                verbose_level: the level that should be displayed"""


        jewels = self.daten.get_all_Jewels()
        
        if jewels is not None:
            self.generate_jewel_table(jewels, verbose_level)

        else: 
            print("\nNo jewels have been created by the user yet")



    def show_all_files(self, verbose_level:int) ->None:
        """Prints all files in table form in the console
        
           Args:
                verbose_level: the level that should be displayed"""


        files = self.daten.get_all_Files()

        if files is not None:
           self.generate_file_table(files, verbose_level)
        
        else: 
            print("\nNo files have been created by the user yet")


    def show_all_blobs(self, verbose_level:int) ->None:
        """Prints all blobs in table form in the console
        
           Args:
                verbose_level: the level that should be displayed"""


        blobs = self.daten.get_all_Blobs()
   
        if blobs is not None:
           self.generate_blobs_table(blobs, verbose_level)

        else: print("\nNo blobs have been created by the user yet")


    def show_jewel_via_id(self,id:int, verbose_level:int) ->None:
        """Prints a jewel and all associated files in table form in the console
        
           Args:
                id: the id of the jewel that should be displayed
                verbose_level: the level that should be displayed"""


        jewel = self.daten.get_Jewel_via_id(id)
    
        if jewel is not None:
            self.generate_jewel_table([jewel], verbose_level)
            files = self.daten.get_Files_via_jewel_id(id)
            self.generate_file_table(files, verbose_level)


        else: print("\nThere is no jewel with the id " + str(id))


    def show_file_via_id (self,id:str, verbose_level:int) ->None:
        """Prints a file and all associated blobs in table form in the console
        
           Args:
                id: the id of the file that should be displayed
                verbose_level: the level that should be displayed"""


        file = self.daten.get_File_via_id(id)

        if file is not None:
            self.generate_file_table([file], verbose_level)
            self.generate_blobs_table(file.blobs, verbose_level)

        else: print("\nThere is no file with the id " + str(id))


    def show_blob_via_id (self,id:int, verbose_level:int) ->None:
        """Prints a blob in table form in the console
        
           Args:
                id: the id of the blob that should be displayed
                verbose_level: the level that should be displayed"""


        blob = self.daten.get_Blob_via_id(id)
        if blob is not None: 
            self.generate_blobs_table([blob], verbose_level)
        else:  
            print("\nThere is no blob with the id " + str(id))


    def show_all_skipped_Files(self, verbose_level:int) ->None:
        """Prints all skipped files in table form in the console
        
           Args:
                verbose_level: the level that should be displayed"""


        files = self.daten.get_all_skipped_files()
 
        if files is not None:
            self.generate_sfiles_table(files, verbose_level)
        else:
            print("\nThere are no skipped files yet")


    def show_skipped_file_via_id(self,id:int, verbose_level:int) ->None:
        """Prints a skipped file in table form in the console
        
           Args:
                id: the id of the skipped file that should be displayed
                verbose_level: the level that should be displayed"""

  
        fi = self.daten.get_skipped_file_via_id(id)
        
        if fi is not None:
            self.generate_sfiles_table([fi], verbose_level)
        else:  print("\nThere is no skipped file with the id " + str(id))

    