from datenbank import *
from datetime import datetime 
from prettytable import PrettyTable

class ShowTables:

    def __init__(self):
        pass


# Diese Methoden passen die Ausgaben an dem vom Nutzer ausgewählten verbose-level an und geben eine Liste mit Strings zurück.
# Level 0: kurze Anzeige
# Level 1: mittlere Anzeige
# Level 2: vollständige Anzeige

    def _verbose_jewel_to_string(self, jewel, verbose_level):
        startdate = str(jewel.monitoring_Startdate)
        comment = str(jewel.comment)
        j_source = str(jewel.jewelSource)
        device = str(jewel.device_name)
        fullbackup_source = jewel.fullbackup_source

        if verbose_level == 0:
            startdate = startdate.split(" ")[0]
            if len(comment) > 15: comment = comment[0:12]+  "..."
            if len(device) > 15: device = device[0:12] + "..."
            if len(j_source) > 10: j_source = j_source[0:7] +"..."
            if len(fullbackup_source) > 10: fullbackup_source = fullbackup_source[0:7]+ "..."

        elif verbose_level == 1:
            startdate = startdate.split(".")[0]
            if len(comment) > 25: comment= comment[0:23] + "..."
            if len(device)> 25: device = device[0:23] + "..."
            if len(j_source) > 20: j_source =  device[0:17] + "..."
            if len(fullbackup_source) > 20: fullbackup_source = fullbackup_source[0:17]+ "..."

        return [str(jewel.id), comment, startdate,  j_source,device, fullbackup_source]


    def _verbose_blob_to_string(self, blob, verbose_level):
            hash = blob.hash
            name = blob.name
            creationDate = str(blob.creationDate)
            change = str(blob.change)
            modify = str(blob.creationDate)
            origin_name = blob.origin_name
            source_path = blob.source_path
            store_destination = blob.store_destination
            id_file = str(blob.iD_File)

            if verbose_level == 0:
                if len(hash) > 10: hash = hash[0:7] + "..."
                if len(name) > 10: name[0:7] + "..."
                creationDate = creationDate.split(" ")[0]
                change = change.split(" ")[0]
                modify = modify.split(" ")[0]
                if len(origin_name) > 5: origin_name = origin_name[0:7] + "..."
                if len(source_path) > 5: source_path = source_path[0:7] + "..."
                if len(store_destination) > 5: store_destination = store_destination[0:7] + "..."
                if len(id_file) > 5: id_file = id_file[0:7] + "..."


            elif verbose_level == 1:
                if len (hash) > 15: hash = hash[0:12] + "..."
                if len(name) > 15: name[0:12] + "..."
                creationDate = creationDate.split(".")[0]
                change = change.split(".")[0]
                modify = modify.split(".")[0]
                if len(origin_name) > 20: origin_name = origin_name[0:17] + "..."
                if len(source_path) > 15: source_path = source_path[0:12] + "..."
                if len(store_destination) > 15: store_destination = store_destination[0:12] + "..."
                if len(id_file) > 15: id_file = id_file[0:12] + "..."

            return [str(blob.id), str(blob.number),hash, name, str(blob.fileSize), creationDate, change, modify, id_file, origin_name, source_path,store_destination]


    def _verbose_skipped_files_to_string(self, s_file, verbose_level):
        file_id= str(s_file[0])
        jewel_id = str(s_file[1])
        uuid = str(s_file[2])
        occurance_Date = str(s_file[3])
        hash = str(s_file[4])
        reason = str(s_file[5])
        add_info = str(s_file[6])
        conn_jewel = str(s_file[7])

        if verbose_level == 0:
            if len(uuid) > 10: uuid = uuid[0:7] + "..."
            occurance_Date = occurance_Date.split(" ")[0]
            if len(hash) > 10: hash = hash[0:7] + "..."
            if len(reason) >15: reason = reason[0:12] + "..."
            if len(add_info) > 15: add_info = add_info[0:12] + "..."
            if len(conn_jewel) > 10: conn_jewel = conn_jewel[0:7] + "..."
    
        if verbose_level == 1:
            if len(uuid) > 15: uuid = uuid[0:12] + "..."
            occurance_Date = occurance_Date.split(" ")[0]
            if len(hash) > 15: hash = hash[0:12] + "..."
            if len(reason) >20: reason = reason[0:17] + "..."
            if len(add_info) > 20: add_info = add_info[0:17] + "..."
            if len(conn_jewel) > 15: conn_jewel = conn_jewel[0:12] + "..."

        return [file_id, jewel_id, uuid, occurance_Date, hash, reason, add_info, conn_jewel]


    def _verbose_files_to_string(self, file, verbose_level):
        birth = str(file.birth)
        id = str(file.id)

        if verbose_level == 0:
            birth = birth.split(" ")[0]
            if len(id) > 15: id = id[0:12] + "..."

        elif verbose_level == 1:
            birth = birth.split(".")[0]
            if len(id) > 25: id = id[0:23] + "..."

        return [id, str(len(file.blobs)) , birth]


# Diese Methoden erstellen Tabellen von Objekten (alle aus der Datenbank oder eins via id) und geben sie in der Console aus.
# Tabellen von den Objekten: Jewels, Files, Blobs und skipped Files.

    def show_all_jewels(self, verbose_level):
        daten = Datenbank()
        jewels = daten.get_all_Jewels()
        

        if jewels is not None:
            table = PrettyTable()
            table.field_names = ["Jewel ID","Comment","Monitoring startdate","Source of the jewel", "Device Name", "Fullbackup source"]

            for jewel in jewels:
                j_list = self._verbose_jewel_to_string(jewel, verbose_level)
                table.add_row([j_list[0], j_list[1], j_list[2], j_list[3],  j_list[4], j_list[5]])

            print(table)

        else: 
            print("\nNo jewels have been created by the user yet")



    def show_all_files(self, verbose_level):
        daten = Datenbank()
        files = daten.get_all_Files()

        if files is not None:
            table = PrettyTable()
            table.field_names = ["File ID", "File versions", "File birth"]

            for fi in files:
                file = self._verbose_files_to_string(fi, verbose_level)
                table.add_row([file[0], file[1], file[2]])

            print(table)
        
        else: 
            print("\nNo files have been created by the user yet")


    def show_all_blobs(self, verbose_level):
        daten = Datenbank()
        blobs = daten.get_all_Blobs()
   
        if blobs is not None:
            table = PrettyTable()

            table.field_names = ["Blob ID", "File version", "Hash", "Name", "File size","Creationdate", "Change", "Modify", 
             "File ID", "Origin name","Source path", "Store destination"]

            for blob in blobs:
                b_list = self._verbose_blob_to_string(blob, verbose_level)
                table.add_row([b_list[0], b_list[1], b_list[2], b_list[3], b_list[4], b_list[5], b_list[6], b_list[7], b_list[8], b_list[9],
                b_list[10], b_list[11]])

            print(table)

        else: print("\nNo blobs have been created by the user yet")


    def show_jewel_via_id(self,id, verbose_level):
        daten = Datenbank()
        jewel = daten.get_Jewel_via_id(id)
    
        if jewel is not None:
            table = PrettyTable()
            table.field_names = ["Jewel ID", "Comment","Monitoring startdate","Source of the jewel", "Device Name", "Fullbackup source"]
            j_list = self._verbose_jewel_to_string(jewel, verbose_level)
            table.add_row([j_list[0], j_list[1], j_list[2], j_list[3],  j_list[4], j_list[5]])
            filetable = PrettyTable()
            files = daten.get_Files_via_jewel_id(id)
            filetable.field_names = ["File ID","Number of BackUps","File birth"]
       
            for file in files:
                f_list = self._verbose_files_to_string(file, verbose_level)
                filetable.add_row([ f_list[0], f_list[1], f_list[2]])
               
            print(table)
            print(filetable)


        else: print("\nThere is no jewel with the id " + str(id))


    def show_file_via_id (self,id, verbose_level):
        daten = Datenbank()
        file = daten.get_File_via_id(id)

        if file is not None:
            table = PrettyTable()
            table.field_names = ["File ID","Number of BackUps","File birth"]
            f_list = self._verbose_files_to_string(file, verbose_level)
            table.add_row([f_list[0], f_list[1], f_list[2]])
            print(table)

            blobtable = PrettyTable()
            blobtable.field_names = ["Blob ID","File version","Hash","Name","File size","Creationdate","Change","Modify","File ID","Origin name","Source path", "Store destination"]

            for blob in file.blobs:
                b_list = self._verbose_blob_to_string(blob, verbose_level)
                blobtable.add_row([b_list[0], b_list[1], b_list[2], b_list[3], b_list[4], b_list[5], b_list[6], b_list[7], b_list[8], b_list[9],
                b_list[10], b_list[11]])

            print(blobtable)

        else: print("\nThere is no file with the id " + str(id))

    def show_blob_via_id (self,id, verbose_level):
        daten = Datenbank()
        blob = daten.get_Blob_via_id(id)

        if blob is not None:
            table =  PrettyTable()
            table.field_names = ["Blob ID", "File version", "Hash", "Name", "File size","Creationdate", "Change", "Modify", 
            "File ID", "Origin name","Source path", "Store destination"]
            b_list = self._verbose_blob_to_string(blob, verbose_level)
            table.add_row([b_list[0], b_list[1], b_list[2], b_list[3], b_list[4], b_list[5], b_list[6], b_list[7], b_list[8], b_list[9],
                b_list[10], b_list[11]])
            print(table)
        else:  
            print("\nThere is no blob with the id " + str(id))


    def show_all_skipped_Files(self, verbose_level):
        daten = Datenbank()
        files = daten.get_all_skipped_files()
 
        if files is not None:
            table =  PrettyTable()
            table.field_names = ["File id", "Jewel id", "UUID", "Occurance_Date", "Hash", "Reason", "Additional information", "Connected file to jewel"]
            for fi in files:
                file = self._verbose_skipped_files_to_string(fi, verbose_level)
                table.add_row([str(file[0]), str(file[1]),str(file[2]), str(file[3]), str(file[4]), str(file[5]), str(file[6]), str(file[7])])
            print(table)
        else:
            print("\nThere are no skipped files yet")

    def show_skipped_file_via_id(self,id, verbose_level):
        daten = Datenbank()
        fi = daten.get_skipped_file_via_id(id)
        
        if fi is not None:
            table =  PrettyTable()
            table.field_names = ["File id", "Jewel id", "UUID", "Occurance_Date", "Hash", "Reason", "Additional information", "Connected file to jewel"]
            file = self._verbose_skipped_files_to_string(fi, verbose_level)
            table.add_row([str(file[0]), str(file[1]),str(file[2]), str(file[3]), str(file[4]), str(file[5]), str(file[6]),str(file[7])])
            print(table)
        else:  print("\nThere is no skipped file with the id " + str(id))

    