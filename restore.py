import os
from datenbank import Datenbank
import subprocess
from datetime import datetime as date
import info_handler
import platform
from repair import Repair
from resFile import resFile
import datetime
from pathlib import Path


class Restore:
    config = info_handler.get_json_info()

    def __init__(self, platform_node=platform.node()):
        self.platform_node = platform_node

    def restore_directory_structure(self, jewel):
        # creates the path, where the restored file is going to be
        # relative_path --> String ;    contains the relative path, for this file,
        #                               which will be restored in restore_destination
        #                               the relative path starts from the jewel directory
        # jewel_origin_path --> String, List ; absolute path for the jewel which contains this file
        # file_origin_path --> String, List ; absolute path for this file
        # restore_destination --> String ; restore destination directory from the JSON config file

        jewel_origin_path = jewel.jewel_source
        restore_destination = self.config['restore_destination'][self.platform_node]

        # the String paths for jewel and file are converted to a list
        jewel_origin_path = os.path.normpath(jewel_origin_path)
        jewel_origin_path = jewel_origin_path.split(os.sep)
        restore_directory_list = []

        for file in jewel.res_file:
            relative_file_path = "/"

            file_origin_path = os.path.normpath(file.origin_location)
            file_origin_path = file_origin_path.split(os.sep)
            file_origin_path.pop()  # the last element from the file path list, is the file itself. pop() removes
            # the last element

            # the file path is reduced to the point, where the jewel starts
            # the remaining file path is collected in relative_file_path for creating/checking the path
            for i in (range(len(jewel_origin_path) - 1)):
                file_origin_path.remove(file_origin_path[0])
            for i in range(len(file_origin_path)):
                relative_file_path = relative_file_path + file_origin_path[i] + "/"

            # print to see the relative path for the path, this path will be created in the restore
            # destination directory
            # print(relative_file_path)

            # check if the restore destination directory for this file already exists
            # create restore destination directory for this file, if it doesn't exists
            if not os.path.exists(restore_destination + relative_file_path):
                os.makedirs(restore_destination + relative_file_path)

            # these are a few asserts for testing
            # assert True == os.path.exists(restore_destination)
            # assert True == os.path.exists(restore_destination+relative_file_path)
            restore_directory_list.append(restore_destination + relative_file_path)

        return restore_directory_list


    def restore_jewel(self, jewel_id: int,  date_time: datetime):
        count = 0
        db_object = Datenbank()
        #date_time = date.fromisoformat(date_time)
        jewel = db_object.get_restore_Jewel(date_time, jewel_id)

        if jewel != None:
            restore_destination_paths = self.restore_directory_structure(jewel)
        else:
            print(f'\nError: jewel with ID "{jewel_id}" not found for time: {date_time}')
            exit()
        files_in_destination = []
        files_in_backup = []
        files_size = 0
        size_completed = []
        for file in jewel.res_file:
            self.repair_file_if_necessary(file)
            try:
                handle_output = subprocess.run(f'rsync -aAXlv "{file.backup_location}" "{restore_destination_paths[count]}"',
                            shell=True, stdout=subprocess.PIPE)
            except:
                print(f'Error: rsync couldn\'t be executed\n'
                      f'used option: aAXlv\n'
                      f'backup path: {file.backup_location}\n'
                      f'destination path: {restore_destination_paths[count]}\n')
                exit()
            # which files got restored
            for (restore_destination_paths[count], dir_names, file_names) in os.walk(restore_destination_paths[count]):
                files_in_destination.extend(file_names)
            if restore_destination_paths[count] not in size_completed:
                size_completed.append(restore_destination_paths[count])
                files_size += sum(f.stat().st_size for f in Path(restore_destination_paths[count]).glob('**/*') if f.is_file())
            # which files should have been restored
            file_path = '/'.join(str(file.backup_location).split('/')[:-1])
            for (file_path, dir_names, file_names) in os.walk(file_path):
                files_in_backup.extend(file_names)
            count += 1
        # differences
        difference = list(set(files_in_backup) - set(files_in_destination))

        files_size_unit = 'bytes'
        unit_list = ['bytes', 'kilobytes', 'megabytes', 'gigabytes']
        for i in range(len(unit_list) - 1, 0, -1):
            if (files_size / pow(1000, i)) >= 1:
                    files_size = round((files_size / pow(1000, i)), 2)
                    files_size_unit = unit_list[i]

        print(f'\nRESTORE DETAILS\n'
              f'├─ jewel id:\t\t{jewel_id}\n'
              f'└─ amount of files:\t{len(set(files_in_destination))}\n'
              f'   └─ size of files:\t{files_size} {files_size_unit}')
        
        if len(difference) != 0:
            print(f'\nWarning: {len(difference)} files couldn\'t be restored\n'
                  f'Missing files: {difference}\n')


    def restore_file(self, file_id: str, date_time: datetime):
        db_object = Datenbank()
        #date_time = date.fromisoformat(date_time)
        jewel = db_object.get_restore_File(date_time, file_id)
        if jewel != None:
            self.repair_file_if_necessary(jewel.res_file[0])
        else:
            print(f'\nError: file with name "{file_id}" not found for time: {date_time}')
            exit()
        restore_destination_paths = self.restore_directory_structure(jewel)
        files_in_destination = []
        try:
            handle_output = subprocess.run(f'rsync -aAXlv "{jewel.res_file[0].backup_location}" "{restore_destination_paths[0]}"', shell=True, stdout=subprocess.PIPE)
        except:
            print(f'\nError: rsync couldn\'t be executed\n'
                f'used option: aAXlv\n'
                f'backup path: {jewel.res_file[0].backup_location}\n'
                f'destination path: {restore_destination_paths[0]}')
            exit()

        # which files got restored
        for (restore_destination_paths[0], dir_names, file_names) in os.walk(restore_destination_paths[0]):
            files_in_destination.extend(file_names)
        # which files should get restored
        file_path = jewel.res_file[0].backup_location.split('/')[-1]
        file_in_backup = [file_path]
        # differences
        difference = list(set(file_in_backup) - set(files_in_destination))
        
        if len(difference) != 0:
            print(f'\nWarning: {len(difference)} file(s) couldn\'t be restored\n'
                  f'Missing file(s): {difference}\n')
        else:
            file_size = os.stat(jewel.res_file[0].backup_location).st_size
            file_size_unit = 'bytes'
            unit_list = ['bytes', 'kilobytes', 'megabytes', 'gigabytes']
            for i in range(len(unit_list) - 1, 0, -1):
                if (file_size / pow(1000, i)) >= 1:
                        file_size = round((file_size / pow(1000, i)), 2)
                        file_size_unit = unit_list[i]

            print(f'\nRESTORE DETAILS\n'
              f'├─ file name:\t\t{file_id}\n'
              f'└─ size of file:\t{file_size} {file_size_unit}')


    def repair_file_if_necessary(self, res_file : resFile, verbosity :bool=False) -> None:
        repair=Repair()
        if repair.check_if_file_is_broken(res_file):
            if(res_file.reed_solomon_path != 'None'):
                repair.repair_file(res_file)
                print("File "+res_file.backup_location+" was repaired")
            else:
                print("""- File is broken, but there is no redundancy information for this file so it can't be repaired.\nsourcepath= """+res_file.backup_location)

