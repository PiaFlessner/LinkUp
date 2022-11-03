import argparse
from show_tables import ShowTables

# Hier startet das Programm
if __name__ == "__main__":

    #get Table Functions
    sT=ShowTables()
    parser = argparse.ArgumentParser(description="Dies ist eine Beschreibung des Programms",
                                     epilog="Dies ist der Epilog")
    # command: python3 Execute.py show (user enters display of tables section)                          
    subparser = parser.add_subparsers(dest='command')
    showTables = subparser.add_parser('show', help="Get into show section of program. Eg. show File Table.")

    # user can choose either of one commands now
    group = showTables.add_mutually_exclusive_group()
    #command: python3 Execute.py show -J 
    group.add_argument('-J', '--showJewel', action='store_true', help='Show Jewels')
    #command: python3 Execute.py show -F
    group.add_argument('-F', '--showFile', action='store_true', help='Show Files')
    #command: python3 Execute.py show -sF
    group.add_argument('-sF', '--showSkippedFile', action='store_true', help='Show skipped Files')
    #command: python3 Execute.py show -B
    group.add_argument('-B', '--showBlob', action='store_true', help='Show Blobs')
    #command: python3 Execute.py show -[J F sf B] 123hi
    showTables.add_argument('id', type=str, nargs='?')
    showTables.add_argument('-v', '--verbose', action='store_true')
    showTables.add_argument('-vv', '--verboseverbose', action='store_true')

    
    
    ##idea collection
    #command: python3 execute.py restore
    restoreSection = subparser.add_parser('restore', help="Get into restore section of program.")
    group = restoreSection.add_mutually_exclusive_group()
    #command: python3 execute.py restore -F 12hi
    group.add_argument('-F', '--restoreFile', action='store_true', help='Restore certain File')
    #command: python3 execute.py restore -J 12hi
    group.add_argument('-J', '--restoreJewel', action='store_true', help='Restore certain Jewel')
    #needed Id to restore
    restoreSection.add_argument('id', type=str)



   #makes args accessable
    args = parser.parse_args()

    ######################user chooses the show section
    if args.command == "show":


        ##########user chooses show jewel
        if args.showJewel:
            if args.id is not None:
                sT.show_jewel_via_id(args.id)
            else:
                sT.show_all_jewels()


        ##########user chooses show File
        elif args.showFile:
            if args.id is not None:
                sT.show_file_via_id(args.id)
            else:
                sT.show_all_files()


         ##########user chooses show skipped File       
        elif args.showSkippedFile:
            if args.id is not None:
                sT.show_skipped_file_via_id(args.id)
            else:
                sT.show_all_skipped_Files()


        ##########user chooses show Blob
        elif args.showBlob:
            if args.id is not None:
                sT.show_blob_via_id(args.id)
            else:
                sT.show_all_blobs()


        ##########user chooses nothing
        else:
            print("No action choosed.")