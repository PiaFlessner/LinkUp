from datenbank import *
from prettytable import PrettyTable

class ShowTables:

    def __init__(self):
        pass

    def show_all_jewels(self):
        daten = Datenbank()
        jewels = daten.get_all_Jewels()

        if jewels is not None:
            table = PrettyTable()
            table.field_names = ["Jewel ID","Comment","Monitoring startdate","Source of the jewel", "Device Name"]

            for jewel in jewels:
                table.add_row([str(jewel.id), str(jewel.comment), str(jewel.monitoring_Startdate), str(jewel.jewelSource), str(jewel.device_name)])

            print(table)

        else: 
            print("\nNo jewels have been created by the user yet")


    def show_all_files(self):
        daten = Datenbank()
        files = daten.get_all_Files()

        if files is not None:
            table = PrettyTable()
            table.field_names = ["File ID", "File versions", "File birth"]

            for file in files:
                table.add_row([str(file.id), str(len(file.blobs)), str(file.birth)])

            print(table)
        
        else: 
            print("\nNo files have been created by the user yet")


    def show_all_blobs(self):
        daten = Datenbank()
        blobs = daten.get_all_Blobs()
   
        if blobs is not None:
            table = PrettyTable()

            table.field_names = ["Blob ID", "File version", "Hash", "Name", "File size","Creationdate", "Change", "Modify", 
             "File ID", "Origin name","Source path", "Store destination"]

            for blob in blobs:
                table.add_row([str(blob.id), str(blob.number), str(blob.hash), str(blob.name), str(blob.fileSize), str(blob.creationDate),
                str(blob.change), str(blob.modify), str(blob.iD_File), str(blob.origin_name), str(blob.source_path), str(blob.store_destination)])

            print(table)

        else: print("\nNo blobs have been created by the user yet")


    def show_jewel_via_id(self,id):
        daten = Datenbank()
        jewel = daten.get_Jewel_via_id(id)
    
        if jewel is not None:
            table = PrettyTable()
            table.field_names = ["Jewel ID", "Comment","Monitoring startdate","Source of the jewel", "Device Name"]
            table.add_row([str(jewel.id), str(jewel.comment), str(jewel.monitoring_Startdate), str(jewel.jewelSource), str(jewel.device_name)])
            filetable = PrettyTable()
            files = daten.get_Files_via_jewel_id(id)
            filetable.field_names = ["File ID","Number of BackUps","File birth"]
       
            for file in files:
                filetable.add_row([str(file.id), str(len(file.blobs)), str(file.birth)])

            print(table)
            print(filetable)


        else: print("\nThere is no jewel with the id " + str(id))


    def show_file_via_id (self,id):
        daten = Datenbank()
        file = daten.get_File_via_id(id)

        if file is not None:
            table = PrettyTable()
            table.field_names = ["File ID","Number of BackUps","File birth"]
            table.add_row([str(file.id), str(len(file.blobs)), str(file.birth)])
            print(table)

            blobtable = PrettyTable()
            blobtable.field_names = ["Blob ID","File version","Hash","Name","File size","Creationdate","Change","Modify","File ID","Origin name","Source path", "Store destination"]

            for blob in file.blobs:
                blobtable.add_row([str(blob.id), str(blob.number), str(blob.hash), str(blob.name), str(blob.fileSize), str(blob.creationDate),
                str(blob.change), str(blob.modify), str(blob.iD_File), str(blob.origin_name), str(blob.source_path), str(blob.store_destination)] )

            print(blobtable)

        else: print("\nThere is no file with the id " + str(id))

    def show_blob_via_id (self,id):
        daten = Datenbank()
        blob = daten.get_Blob_via_id(id)

        if blob is not None:
            table =  PrettyTable()
            table.field_names = ["Blob ID", "File version", "Hash", "Name", "File size","Creationdate", "Change", "Modify", 
            "File ID", "Origin name","Source path", "Store destination"]
            table.add_row([str(blob.id), str(blob.number), str(blob.hash), str(blob.name), str(blob.fileSize), str(blob.creationDate),
            str(blob.change), str(blob.modify), str(blob.iD_File), str(blob.origin_name), str(blob.source_path), str(blob.store_destination)])
            print(table)
        else:  
            print("\nThere is no blob with the id " + str(id))


    def show_all_skipped_Files(self):
        daten = Datenbank()
        files = daten.get_all_skipped_files()

        if files is not None:
            table =  PrettyTable()
            table.field_names = ["File id", "Jewel id", "UUID", "Occurance_Date", "Hash", "Reason", "Additional information", "Connected file to jewel"]
            for file in files:
                table.add_row([str(file[0]), str(file[1]),str(file[2]), str(file[3]), str(file[4]), str(file[5]), str(file[6]), str(file[7])])
            print(table)
        else:
            print("\nThere are no skipped files yet")

    def show_skipped_file_via_id(self,id):
        daten = Datenbank()
        file = daten.get_skipped_file_via_id(id)
        print("Moin")
        if file is not None:
            table =  PrettyTable()
            table.field_names = ["File id", "Jewel id", "UUID", "Occurance_Date", "Hash", "Reason", "Additional information", "Connected file to jewel"]
            table.add_row([str(file[0]), str(file[1]),str(file[2]), str(file[3]), str(file[4]), str(file[5]), str(file[6]),str(file[7])])
            print(table)
        else:  print("\nThere is no skipped file with the id " + str(id))

    