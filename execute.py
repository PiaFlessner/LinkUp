#!/home/gruppe/Schreibtisch/Projektgruppe/projektgruppe/.venv/bin/python3

import argparse
from backup import Backup
from datenbank import Datenbank
from repair import Repair
from show_tables import ShowTables
from restore import Restore
import info_handler as ih
import platform
import restore_handler
from subprocess import PIPE, Popen


class Argument:
    def __init__(self):
        """
        Summary:
        Initialize all arguments, options and parameter needed by the functions.

        Detailed description:
        Every argument/section possibly has a group of options and parameters/values.
        Allows an automatic creation of a help page for every argument.
        Every section works with these values.

        Parameter:
        None

        Return:
        None
        """

        self.parser = argparse.ArgumentParser(description='Backup files or folders. Manage these files by showing, restoring or repairing them.')
        subparser = self.parser.add_subparsers(dest='command')

        ################################################################################################################################

        # section 'show'
        show_tables = subparser.add_parser('show', help="Get into show section of program. Eg. show File Table.")
        group_show_tables = show_tables.add_mutually_exclusive_group()

        # commands for section 'show'
        group_show_tables.add_argument('-J', '--showJewel', action='store_true', help='Show Jewels')
        group_show_tables.add_argument('-F', '--showFile', action='store_true', help='Show Files')
        group_show_tables.add_argument('-sF', '--showSkippedFile', action='store_true', help='Show skipped Files')
        group_show_tables.add_argument('-B', '--showBlob', action='store_true', help='Show Blobs')

        # arguments for section 'show'
        show_tables.add_argument('id', type=str, nargs='?')
        show_tables.add_argument('-v', '--verbose', action='store_true', help="more detail")
        show_tables.add_argument('-vv', '--verboseverbose', action='store_true', help="all of the detail")

        ################################################################################################################################

        # section 'reed_solomon'
        reed_solomon = subparser.add_parser('rs', help="Get into Reed-Solomon section of program. E.g. --createall and --repairall.")
        group_reed_solomon = reed_solomon.add_mutually_exclusive_group()

        # commands for section 'reed_solomon'
        group_reed_solomon.add_argument('-ca', '--createall', action='store_true', help='Create redundancy information for everything')
        group_reed_solomon.add_argument('-c', '--createone', action='store_true', help='Create redundancy information for one file')
        group_reed_solomon.add_argument('-ra', '--repairall', action='store_true', help='Repair all files with redundancy information')
        group_reed_solomon.add_argument('-r', '--repairone', action='store_true', help='Repair one file with redundancy information')

        # arguments for section 'reed_solomon'
        reed_solomon.add_argument('id', type=str, nargs='?')
        reed_solomon.add_argument('-v', '--verbose', action='store_true', help="more detail")
        reed_solomon.add_argument('-o', '--overwrite', action='store_true', help="overwrite Files")

        ################################################################################################################################

        # section 'restore'
        restore_section = subparser.add_parser('restore', help="Get into restore section of program.")
        restore_section_group = restore_section.add_mutually_exclusive_group()

        # commands for section 'restore'
        restore_section_group.add_argument('-F', '--restoreFile', action='store_true', help='Restore certain File')
        restore_section_group.add_argument('-J', '--restoreJewel', action='store_true', help='Restore certain Jewel')

        # arguments for section 'restore'
        restore_section.add_argument('id', type=str, help="File ID in Table File")
        restore_section.add_argument('datetime', type=str, help="Date in Format: Y-m-D-H-M-S")

        ################################################################################################################################

        # section 'backup'
        backup_section = subparser.add_parser('backup', help="Get into backup section of program.")
        backup_section_group = backup_section.add_mutually_exclusive_group()

        # commands for section 'backup'
        backup_section_group.add_argument('-v', '--verbose', action='store_true', help='Backup with detailed information')

        ################################################################################################################################

        # section 'reset'
        reset_section = subparser.add_parser('reset', help="Get into reset section of program.")


    def select_action(self):
        """
        Summary:
        Function chooses the right section of the program.

        Detailed description:
        Reading the argument from the commandline.
        Choose a section according to the argument.
        User errors are handeld by the parser itself.

        Parameter:
        None

        Return:
        None
        """

        # read arguments from the commandline input
        self.args = self.parser.parse_args()
        argument = self.args.command

        if argument == 'backup':
            self.backup_section()

        # access section 'show'
        elif argument == 'show':
            self.show_section()

        # access section 'restore'
        elif argument == 'restore':
            self.restore_section()

        # access section 'reed_solomon'
        elif argument == 'rs':
            self.reed_solomon_section()

        # access section 'reset'
        elif argument == 'reset':
            self.reset_section()


    def backup_section(self):
        """
        Summary:
        Initialize a backup.

        Detailed description:
        The function checks the source and destination from the JSON file.
        An object from the class "Backup" is created with these informations.
        The restore process is performed in another function (initialize_backup).
        The user has the option to print more informations, based on the verbose_level.

        Parameter:
        None

        Return:
        None
        """

        verbose_level = 0
        if self.args.verbose == 1:
            verbose_level = 1
        config = ih.get_json_info()
        backup = Backup(config["jewel_sources"][platform.node()], config["destination"][platform.node()])
        backup.initialize_backup(verbose_level)


    def show_section(self):
        """
        Summary:
        Initialize a presentation of targeted files.

        Detailed description:
        The function checks, if a file, jewel, skipped file or blob should be shown to the user.
        Additionaly, the user can choose between showing all or single files.
        A specific target is chosen by the corresponding ID.
        The presentation process is performed in another function (show_jewel_via_id or show_all_jewels, show_file_via_id or 
        show_all_files, show_skipped_file_via_id or show_all_skipped_Files, show_blob_via_id or show_all_blobs).
        The user has the option to print more informations, based on the verbose_level.

        Parameter:
        None

        Return:
        None
        """

        sT = ShowTables()

        # user chooses show jewel
        if self.args.showJewel:
            verbose_level = 0
            if self.args.verbose:
                verbose_level = 1
            elif self.args.verboseverbose:
                verbose_level = 2
            if self.args.id is not None:
                sT.show_jewel_via_id(self.args.id, verbose_level)
            else:
                sT.show_all_jewels(verbose_level)

        # user chooses show file
        elif self.args.showFile:
            verbose_level = 0
            if self.args.verbose:
                verbose_level = 1
            elif self.args.verboseverbose:
                verbose_level = 2
            if self.args.id is not None:
                sT.show_file_via_id(self.args.id, verbose_level)
            else:
                sT.show_all_files(verbose_level)

        # user chooses show skipped file
        elif self.args.showSkippedFile:
            verbose_level = 0
            if self.args.verbose:
                verbose_level = 1
            elif self.args.verboseverbose:
                verbose_level = 2
            if self.args.id is not None:
                sT.show_skipped_file_via_id(self.args.id, verbose_level)
            else:
                sT.show_all_skipped_Files(verbose_level)

        # user chooses show blob
        elif self.args.showBlob:
            verbose_level = 0
            if self.args.verbose:
                verbose_level = 1
            elif self.args.verboseverbose:
                verbose_level = 2
            if self.args.id is not None:
                sT.show_blob_via_id(self.args.id, verbose_level)
            else:
                sT.show_all_blobs(verbose_level)

        # user chooses nothing
        else:
            print("No action selected.")


    def restore_section(self):
        """
        Summary:
        Initialize a restore process.

        Detailed description:
        The function checks, if a file or jewel sould be restored.
        A specific target is chosen by the corresponding ID.
        The restore process is performed in another function (restore_file or restore_jewel).

        Parameter:
        None

        Return:
        None
        """

        restore_object = Restore()

        if self.args.restoreFile:
            restore_object.restore_file(restore_handler.restore_options(self.args.id, self.args.datetime)[0], restore_handler.restore_options(self.args.id, self.args.datetime)[1])
            
        elif self.args.restoreJewel:
            try:
                arg_ID = int(self.args.id)
                arg_datetime = self.args.datetime
            except:
                print('\nError: given ID isn\'t an integer.')
                exit()
            
            try:
                arg_1 = int(restore_handler.restore_options(arg_ID, arg_datetime)[0])
                arg_2 = restore_handler.restore_options(arg_ID, arg_datetime)[1]
            except:
                # error print in function 'restore_options'
                exit()

            restore_object.restore_jewel(arg_1, arg_2)
        
        else:
            print("Please enter appropriate flag (-F or -J) ")

    
    def reed_solomon_section(self):
        """
        Summary:
        Initialize an integrity check / repair process for the project.

        Detailed description:
        The function checks, if all or only one files should be checked.
        If one file is chosen, use the id of the file.
        The repair process is performed in another function (create_repair_data).
        The user has the option to print more informations, based on the verbose_level.

        Parameter:
        None

        Return:
        None
        """

        verbose_level = 0
        if self.args.verbose == 1:
            verbose_level = 1
        repair = Repair()
        daten = Datenbank()
        blobs=[]
        overwrite = self.args.overwrite
        if self.args.createall:
            blobs = daten.get_all_Blobs()
            for blob in blobs:
                repair.create_repair_data(blob)
            print("Redundancy information created")
        elif self.args.createone:
            if self.args.id is not None:
                blob = daten.get_Blob_via_id(self.args.id)
                repair.create_repair_data(blob, overwrite)
                print("Redundancy information created")
            
        else:
            print("ID missing! exiting...")


    def reset_section(self):
        """
        Summary:
        Initialize a reset of the project, if the user agrees.

        Detailed description:
        If the user types "python3 execute.py reset", the program asks for a confirmation.
        The function reads a second time from the commandline.
        If the user types "I am sure", the program will continue to do a full reset (mostly for debug purpose).
        The reset process is performed in another function (reset_backup).

        Parameter:
        None

        Return:
        None
        """

        print(f'Do you really want to reset the backup for your current device: {platform.node()}?')
        print('Then please enter >I am sure< to reset your backup.')
        print('Or enter something else to cancel.')
        user_input = input()
        if user_input == 'I am sure': 
            ih.reset_backup()
        else: 
            print('The reset was canceled.')


def check_packages(required_packages: list[str]):
    """
    Summary:
    Checking required packages.

    Detailed description:
    This function takes a list of strings, which contain the name of a required package, as the input.
    For every element in this list, the function checks the availability of the package in the users operating system.
    The method of checking is the execution of the shell command "which" with the package as the parameter.
    The "which" command returns the path of the package or the message "x not found".
    Based on the return, the function returns either True (everything available) or False (something is missing).
    In addition, the user gets notified with an error message "Error: package x not found".

    Parameter:
    required_packages : list[str]
    └─ Containing names of packages.

    Return:
    complete : boolean
    └─ Is False, if a package is missing. Otherwise True.
    """

    complete = True

    for package in required_packages:
        subprocess_output = ''
        try:
            subprocess_output = Popen(f'which "{package}"', shell=True, stdout=PIPE)
        except:
            pass

        if f'{package}' not in subprocess_output.stdout.read().decode('UTF-8'):
            complete = False
            print(f'Error: package "{package}" not found')
    
    return complete


if __name__ == "__main__":
    """
    Summary:
    Initialize check and selection of action.

    Detailed description:
    The main function checks for needed packages with the function "check_packages" and continues, if everything is available .
    This requires a package_list[str], containing all needed packages (set by the developer).
    A class object "argument" is initialized, which reads the commandline input of the user.
    With these, the main function calls the function "select_action", which selects the right task.

    Parameter:
    None

    Return:
    None
    """

    package_list = [
        'rsync',
        'openssl'
    ]
    if not check_packages(package_list):
        exit()

    argument = Argument()
    argument.select_action()
