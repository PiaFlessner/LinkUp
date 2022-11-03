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
    jewel_path_list = ["/home/gruppe/backupTest/jewels", "/home/gruppe/backupTest/jewels2", "/home/peter"]

    def __init__(self, filepath):
        self.filepath = filepath

    def execute_backup(self):
        print("Creating differential backup")
        full_backup_path = "/home/ole/backupTest/fullBackup"
        pass

    def execute_fullbackup(self):
        print("Creating full backup")

        for jewel_path in self.jewel_path_list:
            if not(os.path.exists(jewel_path)):
                self.jewel_path_list.remove(jewel_path)

        jewel_path_list_string = self.list_to_string(self.jewel_path_list)
        subprocess_return = subprocess.Popen(f'rsync -aAXn --out-format="%n" {jewel_path_list_string} '
                                             '/home/gruppe/backupTest/fullBackup',
                                             shell=True, cwd='/home/gruppe/backupTest',
                                             stdout=subprocess.PIPE)
        output = subprocess_return.stdout.read()
        output = output.decode('utf-8')
        output_array = output.splitlines()
        print(output_array)

        # Jewel = das hier will ich Backupen
        # ID, comment, datetime, jewel pfad
        # jewel = Jewel(1, "comment 1.jewel", date.today(), self.filepath)

        
        for line in output_array:     
                    
            if line.endswith('/'):
                self.current_source_path = line

                #check wether path is now the jewel
                for jewel_path in self.jewel_path_list:

                    if jewel_path.rsplit('/', 1)[1] == line.strip("/"):
                        jewel = Jewel(0, None, date.today(),self.filepath + '/' + line, platform.node())
                        break

            else:
                file_object = info_handler.get_metadata(self.filepath + '/' + line)
                # Erstellt Array erstes element vor letztem Slash, zweites Element nach dem Slash
                file_name = line.rsplit('/', 1)[1]
                blob = Blob(0, 0, file_object.f_hash, file_object.name, file_object.f_size,
                            self.current_date_time, file_object.modify, file_object.modify, 0, file_name,
                            self.current_source_path, self.new_backup_location)
                file = File(0, [blob], file_object.birth)
                datenbank = Datenbank()
                result = datenbank.add_to_database(jewel, file, platform.node())
                print(result)

    def list_to_string(self, string_list):
        formatted_string = " ".join(string_list)
        return formatted_string
