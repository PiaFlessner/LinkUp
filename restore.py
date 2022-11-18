import os

class Restore:

    def restore_directory_structure(self,jewel_origin_name, file_origin_name, restore_destination):
        # creates the path, where the restored file is going to be
        # jewel_origin_name --> String ; absolute path for the jewel which contains this file
        # file_origin_name --> String ; absolute path for this file
        # restore_destination --> String ; restore destination directory from the JSON config file

        relative_file_path = "/"

        # this crops the absolue paths to a relative path for the restore directory
        # the String paths are converted to a list
        jewel_origin_name = os.path.normpath(jewel_origin_name)
        jewel_origin_name = jewel_origin_name.split(os.sep)

        file_origin_name = os.path.normpath(file_origin_name)
        file_origin_name = file_origin_name.split(os.sep)
        file_origin_name.pop()  # the last element from the file path list, is the file itself. pop() removes the last element

        # prints to see lists from the String Paths
        #print(jewel_origin_name)
        #print(file_origin_name)

        # the file path is reduced to the point, where the jewel starts
        # the remaining file path is collected in relative_file_path for creating/checking the path
        for i in (range(len(jewel_origin_name)-1)):
            file_origin_name.remove(file_origin_name[0])
        for i in range(len(file_origin_name)):
            relative_file_path = relative_file_path + file_origin_name[i] + "/"

        # print to see the relative path for the path, this path will be made in the restore destination directory
        #print(relative_file_path)

        # check if the restore destination directory for this file already exists
        # create restore destination directory for this file, if it doesn't exists
        if not os.path.exists(restore_destination+relative_file_path):
            os.makedirs(restore_destination+relative_file_path)
        
        # these are a few asserts for testing
        # the asserts must be commented
        #assert False == os.path.exists(restore_destination)
        #assert False == os.path.exists(restore_destination+relative_file_path)
        