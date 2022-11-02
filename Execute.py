import argparse
import ShowTables as sT

# Hier startet das Programm
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Dies ist eine Beschreibung des Programms",
                                     epilog="Dies ist der Epilog")
    parser.add_argument('-sJ', '--showJewel', type=str, nargs='?', action='store', default= 'all', help='Show Jewels')
    parser.add_argument('-sF', '--showFile', type=str, nargs='?', action='store',  default= 'all',help='Show Files')
    parser.add_argument('-ssF', '--showSkippedFile', type=str, nargs='?', action='store',  default= 'all',help='Show skipped Files')
    parser.add_argument('-sB', '--showBlob',  type=str, nargs='?', action='store', default= 'all', help='Show Blobs')

   #makes args acessable
    args = parser.parse_args()

    if args.showJewel is not None:
        if args.showJewel == 'all':
            sT.show_all_jewels()
        else:
            sT.show_jewel_via_id(args.showJewel)

    if args.showFile is not None:
        if args.showFile == 'all':
            sT.show_all_files()
        else:
            sT.show_file_via_id(args.showFile)

    if args.showSkippedFile is not None:
        if args.showSkippedFile == 'all':
            sT.show_all_skipped_Files()
        else:
            sT.show_skipped_file_via_id(args.showSkippedFile)

    if args.showBlob is not None:
        if args.showBlob == 'all':
            sT.show_all_blobs()
        else:
            sT.show_blob_via_id(args.showBlob)

