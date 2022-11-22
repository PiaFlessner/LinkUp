import argparse
from json import JSONDecodeError
import sys
from backup import Backup
from show_tables import ShowTables
import info_handler as ih
import platform

# Hier startet das Programm
if __name__ == "__main__":

    # get Table Functions
    sT = ShowTables()
    parser = argparse.ArgumentParser(description="Dies ist eine Beschreibung des Programms",
                                     epilog="Dies ist der Epilog")
    # command: python3 execute.py show (user enters display of tables section)
    subparser = parser.add_subparsers(dest='command')
    showTables = subparser.add_parser('show', help="Get into show section of program. Eg. show File Table.")
    backup = subparser.add_parser('backup', help="Get into backup section of program.")

    # user can choose either of one commands now
    group = showTables.add_mutually_exclusive_group()
    # command: python3 execute.py show -J
    group.add_argument('-J', '--showJewel', action='store_true', help='Show Jewels')
    # command: python3 execute.py show -F
    group.add_argument('-F', '--showFile', action='store_true', help='Show Files')
    # command: python3 execute.py show -sF
    group.add_argument('-sF', '--showSkippedFile', action='store_true', help='Show skipped Files')
    # command: python3 execute.py show -B
    group.add_argument('-B', '--showBlob', action='store_true', help='Show Blobs')
    # command: python3 execute.py show -[J F sf B] 123hi
    showTables.add_argument('id', type=str, nargs='?')
    # command: python3 execute.py show -[J F sf B] ? -[v vv]
    showTables.add_argument('-v', '--verbose', action='store_true')
    showTables.add_argument('-vv', '--verboseverbose', action='store_true')
    paths = parser.add_mutually_exclusive_group()

    ##idea collection
    # command: python3 execute.py restore
    restoreSection = subparser.add_parser('restore', help="Get into restore section of program.")
    group = restoreSection.add_mutually_exclusive_group()
    # command: python3 execute.py restore -F 12hi
    group.add_argument('-F', '--restoreFile', action='store_true', help='Restore certain File')
    # command: python3 execute.py restore -J 12hi
    group.add_argument('-J', '--restoreJewel', action='store_true', help='Restore certain Jewel')
    # needed Id to restore
    restoreSection.add_argument('id', type=str)

    # makes args accessable
    args = parser.parse_args()

    ######################user chooses the show section
    if args.command == "show":

        ##########user chooses show jewel
        if args.showJewel:
            verbose_level = 0
            if args.verbose:
                verbose_level = 1
            elif args.verboseverbose:
                verbose_level = 2
            if args.id is not None:
                sT.show_jewel_via_id(args.id, verbose_level)
            else:
                sT.show_all_jewels(verbose_level)


        ##########user chooses show File
        elif args.showFile:
            verbose_level = 0
            if args.verbose:
                verbose_level = 1
            elif args.verboseverbose:
                verbose_level = 2
            if args.id is not None:
                sT.show_file_via_id(args.id, verbose_level)
            else:
                sT.show_all_files(verbose_level)


        ##########user chooses show skipped File
        elif args.showSkippedFile:
            verbose_level = 0
            if args.verbose:
                verbose_level = 1
            elif args.verboseverbose:
                verbose_level = 2
            if args.id is not None:
                sT.show_skipped_file_via_id(args.id, verbose_level)
            else:
                sT.show_all_skipped_Files(verbose_level)


        ##########user chooses show Blob
        elif args.showBlob:
            verbose_level = 0
            if args.verbose:
                verbose_level = 1
            elif args.verboseverbose:
                verbose_level = 2
            if args.id is not None:
                sT.show_blob_via_id(args.id, verbose_level)
            else:
                sT.show_all_blobs(verbose_level)


        ##########user chooses nothing
        else:
            print("No action choosed.")
    elif args.command == "restore":
        if args.restoreFile:
            pass
        elif args.restoreJewel:
            pass
    if args.command == "backup":
        config = ih.get_json_info()
        backup = Backup(config["jewel_sources"][platform.node()], config["destination"][platform.node()])
        backup.initialize_backup()
