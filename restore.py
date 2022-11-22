import os
from resFile import resFile
from resJewel import resJewel


class Restore:

    def restore_directory_structure(self, jewel):
        # creates the path, where the restored file is going to be
        # relative_path --> String ; contains the relative path, for this file, which will be restored in restore_destination
        #                            the relative path starts from the jewel directory
        # jewel_origin_path --> String, List ; absolute path for the jewel which contains this file
        # file_origin_path --> String, List ; absolute path for this file
        # restore_destination --> String ; restore destination directory from the JSON config file

        relative_file_path = ""
        file_origin_path = ""
        jewel_origin_path = jewel.jewel_source
        restore_destination = jewel.restore_destination

        # the String paths for jewel and file are converted to a list
        jewel_origin_path = os.path.normpath(jewel_origin_path)
        jewel_origin_path = jewel_origin_path.split(os.sep)

        for file in jewel.res_file:
            relative_file_path = "/"

            file_origin_path = os.path.normpath(file.origin_location)
            file_origin_path = file_origin_path.split(os.sep)
            file_origin_path.pop()  # the last element from the file path list, is the file itself. pop() removes the last element

            # the file path is reduced to the point, where the jewel starts
            # the remaining file path is collected in relative_file_path for creating/checking the path
            for i in (range(len(jewel_origin_path)-1)):
                file_origin_path.remove(file_origin_path[0])
            for i in range(len(file_origin_path)):
                relative_file_path = relative_file_path + file_origin_path[i] + "/"

            # print to see the relative path for the path, this path will be created in the restore destination directory
            #print(relative_file_path)

            # check if the restore destination directory for this file already exists
            # create restore destination directory for this file, if it doesn't exists
            if not os.path.exists(restore_destination+relative_file_path):
                os.makedirs(restore_destination+relative_file_path)
        
            # these are a few asserts for testing
            #assert True == os.path.exists(restore_destination)
            #assert True == os.path.exists(restore_destination+relative_file_path)
            