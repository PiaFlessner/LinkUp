import os
from datenbank import Datenbank
import subprocess
from datetime import datetime as date
import info_handler
import platform


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

    def restore_jewel(self, jewel_id: int, date_time: str):
        count = 0
        db_object = Datenbank()
        date_time = date.fromisoformat(date_time)
        jewel = db_object.get_restore_Jewel(date_time, jewel_id)
        restore_destination_paths = self.restore_directory_structure(jewel)
        for file in jewel.res_file:
            subprocess.run(f'rsync -aAXv {file.backup_location} {restore_destination_paths[count]} ',
                           shell=True)
            count += 1

    def restore_file(self, file_id: str, date_time: str):
        db_object = Datenbank()
        date_time = date.fromisoformat(date_time)
        jewel = db_object.get_restore_File(date_time, file_id)
        restore_destination_paths = self.restore_directory_structure(jewel)
        print(restore_destination_paths[0])
        subprocess.run(f'rsync -aAXv {jewel.res_file[0].backup_location} {restore_destination_paths[0]} ', shell=True)
