import os
import subprocess
import platform
from datetime import datetime as date
import info_handler
from datenbank import Blob, Datenbank, File, Jewel


class Backup:

    current_source_path = None
    current_date_time = date.now()
    current_date_time_formatted = current_date_time.strftime("%d-%m-%Y-%H-%M")
    new_backup_location = f"backup-{current_date_time_formatted}"
    fullbackup_name = "fullBackup"+platform.node()

    def __init__(self, jewel_path_list, destination):
        self.jewel_path_list = jewel_path_list
        self.destination = destination
        self.db = Datenbank()

    def initialize_backup(self):
        #to minimize work, first check if these paths even exists, then continue
        tmp = self.filter_non_existing_paths(self.jewel_path_list)

        diff_backup_sources = self.db.check_which_jewel_sources_exist(tmp, platform.node())
        #filter out everything, that is in diff_backup already
        full_backup_sources = [e for e in tmp if e not in  diff_backup_sources]

        #execute,when not empty
        if diff_backup_sources:
            self.execute_backup(diff_backup_sources)

        #execute, when not empty
        if full_backup_sources:
            self.execute_fullbackup(full_backup_sources)

    def execute_backup(self, jewel_sources):
        print("Creating differential backup")
        differential_backup_name = f"diff-{date.now().strftime('%d-%m-%Y-%H-%M')}"
        old_jewels = self.db.get_fullbackup_paths(jewel_sources)
        backup_sources_for_r_sync = " ".join(jewel_sources)

        #a would equals -rlptgoD but in Order to make O work, it needs to be written out
        #O is needed, because otherwise rsync would always backup a folder, when the user only Clicks on it (an therefore opens the folder)
        #unwanted behavior, so O omits directory changes (only of the folder, not of the files inside the folder!)
        subprocess_return = subprocess.Popen(f"rsync -rlptgoDAXO --out-format='%n' "
                                                    f"--compare-dest={self.destination}/{self.fullbackup_name} {backup_sources_for_r_sync} "
                                                    f"{self.destination}/{differential_backup_name}",
                                                    shell=True,
                                                    stdout=subprocess.PIPE)
        output = subprocess_return.stdout.read()
        output = output.decode('utf-8')
        output_array = output.splitlines()

        self.read_files_and_jewel_from_rsync_output(output_array, jewel_sources, f"{self.destination}/{differential_backup_name}", self.destination+"/"+self.fullbackup_name )   
     

                




    def execute_fullbackup(self, jewel_sources):
        print("Creating full backup")

        jewel_path_list_string = self.list_to_string(jewel_sources)
        subprocess_return = subprocess.Popen(f'rsync -aAX --out-format="%n" {jewel_path_list_string} '
                                             f'{self.destination}/{self.fullbackup_name}',
                                             shell=True,
                                             stdout=subprocess.PIPE)

        output = subprocess_return.stdout.read()
        output = output.decode('utf-8')
        output_array = output.splitlines()

        self.read_files_and_jewel_from_rsync_output(output_array, jewel_sources, f"{self.destination}/{self.fullbackup_name}", self.destination+"/"+self.fullbackup_name ) 

    def list_to_string(self, string_list):
        formatted_string = " ".join(string_list)
        return formatted_string

    def filter_non_existing_paths(self, paths):
        for jewel_path in paths:
            if not(os.path.exists(jewel_path)):
                paths.remove(jewel_path)
        return paths


    def read_files_and_jewel_from_rsync_output(self, output_array, jewel_sources,store_destination_body, fullbackup_store_destination_body):
        result = []
        for line in output_array:                     
            if line.endswith('/'):
                self.current_source_path = line

                #check wether path is now the jewel
                for jewel_path in jewel_sources:

                    #stripping and splitting is needed, since comparison does not work otherwise
                    if jewel_path.rsplit('/', 1)[1].strip("/") == line.strip("/"):
                        jewel = Jewel(0, None, date.today(),jewel_path, platform.node(), f'{fullbackup_store_destination_body}/{line.strip("/")}')
                        break

            else:
                #get only the working dir without the jewel(because line inherits the jewel)
                working_dir = jewel_path.rsplit('/',1)[0]
                file_object = info_handler.get_metadata(working_dir + '/' + line)
                # Erstellt Array erstes element vor letztem Slash, zweites Element nach dem Slash
                file_name = line.rsplit('/', 1)[1]
                blob = Blob(0, 0, file_object.f_hash, "PLATZHALTER", file_object.f_size,
                            self.current_date_time, file_object.modify, file_object.meta_change, 0, file_name,
                            working_dir + "/" + line, f'{store_destination_body}/{line}')

                file = File(0, [blob], file_object.birth)
                datenbank = Datenbank()
                r = datenbank.add_to_database(jewel, file, platform.node())
                result.append(r)

                ##when result false, the file must be deleted
                #why? rsync chekcs, if the jewel has changed to the fullbackup, but whats with already registered changes in dif backup? 
                #therefore some files would be store again and again and again, 
                # even tho in one diff backup was this change regognized
                #other cause: rsync only can store THE WHOLE directory layer, when one file in this directory layer has changed.
                #also unwanted behavior.
                #as long as rsync does not work this out, this line is needed. since now, rsync does not doe all copies right
                if(not r):
                    os.remove(f'{store_destination_body}/{line}')

        return result