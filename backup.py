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

        subprocess_return = subprocess.Popen(f"rsync -aAX --out-format='%n' "
                                                    f"--compare-dest={self.destination}/{self.fullbackup_name} {jewel_sources} "
                                                    f"{self.destination}/{differential_backup_name}",
                                                    shell=True,
                                                    stdout=subprocess.PIPE)
        output = subprocess_return.stdout.read()
        output = output.decode('utf-8')
        output_array = output.splitlines()

        #since we do it for every jewel, the first line ist always './' and not needed
        print(output_array)
        if len(output_array) != 0:
            output_array.pop(0)

        for line in output_array:
            if line.endswith('/'):
                self.current_source_path = line

            else:
                filename_arr = line.rsplit('/', 1)
                if len(filename_arr) == 1:
                    file_name = filename_arr[0]
                else:
                    file_name = filename_arr[1]

                    file_object = info_handler.get_metadata(old_jewels[i].jewelSource + '/' + line)
                    blob = Blob(0, 0, file_object.f_hash, "PLATZHALTER", file_object.f_size,
                    self.current_date_time, file_object.modify, file_object.modify, 0, file_name, old_jewels[i].jewelSource + "/" + line, f'{self.destination}/{differential_backup_name}/{line}')
                    file = File(0, [blob], file_object.birth)
                    result = self.db.add_to_database(old_jewels[i],file,platform.node())
                    print(result)

                    if(not result):
                        ##when result false, the file must be deleted
                        #why? rsync checks if the whole jewel has changed, and then, it stores EVERY FILE 
                        #therefore some files would be store again and again and again, 
                        # even tho in one diff backup was this change regognized
                        os.remove(f'{self.destination}/{differential_backup_name}/{line}')

                




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
        
        for line in output_array:                     
            if line.endswith('/'):
                self.current_source_path = line

                #check wether path is now the jewel
                for jewel_path in jewel_sources:

                    #stripping and splitting is needed, since comparison does not work otherwise
                    if jewel_path.rsplit('/', 1)[1].strip("/") == line.strip("/"):
                        jewel = Jewel(0, None, date.today(),jewel_path, platform.node(), f'{self.destination}/{self.fullbackup_name}/{line.strip("/")}')
                        break

            else:
                #get only the working dir without the jewel(because line inherits the jewel)
                working_dir = jewel_path.rsplit('/',1)[0]
                file_object = info_handler.get_metadata(working_dir + '/' + line)
                # Erstellt Array erstes element vor letztem Slash, zweites Element nach dem Slash
                file_name = line.rsplit('/', 1)[1]
                blob = Blob(0, 0, file_object.f_hash, "PLATZHALTER", file_object.f_size,
                            self.current_date_time, file_object.modify, file_object.modify, 0, file_name,
                            working_dir + "/" + line, f'{self.destination}/{self.fullbackup_name}/{line}')

                file = File(0, [blob], file_object.birth)
                datenbank = Datenbank()
                result = datenbank.add_to_database(jewel, file, platform.node())
                print(result)

    def list_to_string(self, string_list):
        formatted_string = " ".join(string_list)
        return formatted_string

    def filter_non_existing_paths(self, paths):
        for jewel_path in paths:
            if not(os.path.exists(jewel_path)):
                paths.remove(jewel_path)
        return paths