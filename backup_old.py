import platform
import subprocess
import os
import hashlib
import sys
from time import sleep
from datenbank import Blob, Datenbank
from datenbank import Jewel
from datenbank import File
import file as mirco_file
import argparse
from datetime import datetime as date

# Hier startet das Programm
if __name__ == "__main__":

    # Initialisierung des Parsers
    parser = argparse.ArgumentParser(description="Dies ist eine Beschreibung des Programms",
                                     epilog="Dies ist der Epilog")

    # Zuweisung von möglichen arguments
    parser.add_argument('-f', type=str, help='File input')
    parser.add_argument('-d', type=str, help='Directory input')

    # Arguments einlesen und in Liste schreiben
    args = parser.parse_args()
    arglist = sys.argv

    if len(arglist) > 1:
        # Ermitteln des aktuellen Datums um den Ordner des neusten Backups festzulegen
        current_date_time = date.now()
        current_date_time_formatted = date.now().strftime("%d-%m-%Y-%H-%M")
        new_backup_location = f"backup-{current_date_time_formatted}"

        f"diff-{date.now().strftime('%d-%m-%Y-%H-%M')}"

        # TODO: Sources aus der Datenbank holen in Form einer Liste
        source_list = ["jewels", "jewels2"]
        source_string = list_to_string(source_list)

        # TODO: Mirco Argument System ueberarbeiten
        if arglist[1] == '-f':
            pass
        elif arglist[1] == '-d':
            # home/ole/backupTest
            filepath = arglist[2]
            fullBackup = filepath + '/fullBackup'
            pathExists = os.path.exists(fullBackup)
            if pathExists:
                print("Path exists, creating differential backup?")
                # Create differential backup
                # rsync -aAXv --delete --compare-dest=/home/ole/backupTest/fullBackup jewels backup.0
                # TODO: remove n Flag
                subprocessReturn = subprocess.Popen(f"rsync -aAX --out-format='%n' "
                                                    f"--compare-dest=/home/ole/backupTest/fullBackup {source_string} "
                                                    f"{new_backup_location}",
                                                    shell=True, cwd=filepath,
                                                    stdout=subprocess.PIPE)
                output = subprocessReturn.stdout.read()
                output = output.decode('utf-8')
                outputArray = output.splitlines()
                current_source_path = None
                print("--------------------------------")
                # Jewel = das hier will ich Backupen
                jewel = Jewel(1, "comment 1.jewel", date.today(), filepath)

                for line in outputArray:
                    if line.endswith('/'):
                        current_source_path = line
                        # print(line)
                    else:
                        file_object = get_metadata(filepath + '/' + line)
                        # Erstellt Array erstes element vor letztem Slash, zweites Element nach dem Slash
                        file_name = line.rsplit('/', 1)[1]
                        blob = Blob(0, 0, file_object.f_hash, file_object.name, file_object.f_size,
                                    current_date_time, file_object.modify, file_object.modify, 0, file_name,
                                    current_source_path, new_backup_location)
                        file = File(0, [blob], file_object.birth)
                        datenbank = Datenbank()
                        result = datenbank.add_to_database(jewel, file, platform.node())
                        print(result)
                        pass
                print("--------------------------------")

            else:

                # print (outputArray)
                del outputArray[0]  # nicht schön aber selten
                del outputArray[0]
                del outputArray[-1]
                del outputArray[-1]
                del outputArray[-1]
                print("--------------------------------")
                # Jewel = das hier will ich Backupen
                jewel = Jewel(0, None, date.today(), filepath)

                for line in outputArray:
                    if line.endswith('/'):
                        current_source_path = line
                        # print(line)
                    else:
                        file_object = get_metadata(filepath + '/' + line)
                        # Erstellt Array erstes element vor letztem Slash, zweites Element nach dem Slash
                        file_name = line.rsplit('/', 1)[1]
                        blob = Blob(0, 0, file_object.f_hash, file_object.name, file_object.f_size,
                                    current_date_time, file_object.modify, file_object.modify, 0, file_name,
                                    current_source_path, new_backup_location)
                        file = File(0, [blob], file_object.birth)
                        datenbank = Datenbank()
                        result = datenbank.add_to_database(jewel, file, platform.node())
                        print(result)
                        pass

                print("")
                os.mkdir(fullBackup)
                sleep(1)

                subprocess.Popen('rsync -aAX /home/gruppe/backupTest/jewels '' /home/gruppe/backupTest/fullBackup',
                                 shell=True, cwd='/home/gruppe/backupTest',
                                 stdout=subprocess.PIPE)
                # TODO sanity checks "ohne ende"
        else:
            print("error: unknown option")
    else:
        print("error: no argument")
