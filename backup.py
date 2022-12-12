from json.decoder import JSONDecodeError
import os
import subprocess
import platform
from datetime import datetime as date
from hardlink_info import HardlinkInfo
import info_handler
from datenbank import Blob, Datenbank, File, Jewel
from pathlib import Path
import time



class Backup:


    def __init__(self, jewel_path_list, destination, testcase=False):
        self.start_time = time.time()
        print("--- %s seconds ---" % (time.time() - self.start_time))
        self.jewel_path_list = jewel_path_list
        self.destination = destination
        self.db = Datenbank(testcase)
        # time.sleep(5)
        self.device_name = platform.node()
        if (testcase):
            self.device_name = "testCases"
        self.fullbackup_name = "fullBackup" + self.device_name
        self.current_date_time = date.now()
        self.current_date_time_formatted = self.current_date_time.strftime("%Y-%m-%d-%H-%M-%s")
        self.new_backup_location = f"backup-{self.current_date_time_formatted}"
        self.current_source_path = None


    def initialize_backup(self, verbose_level):

        start_time = time.time()

        self.check_packages(['rsync', 'openssl'])

        #Checks and deletes the first backup when it runned not through and start from scratch again. 
        if os.path.exists("db.log"):
           file = open("db.log", "r")
           log_lines= file.readlines()
           file.close()
           if len(log_lines) > 1:  
               if log_lines[1].rstrip() == self.fullbackup_name:   
                    info_handler.check_db_hash(self.destination, self.fullbackup_name)
                    os.remove(self.destination + "/" + "tmp.db") 
        print("1--- %s seconds ---" % (time.time() - start_time))
        # to minimize work, first check if these paths even exists, then continue
        tmp = self.filter_non_existing_paths(self.jewel_path_list)
        print("2--- %s seconds ---" % (time.time() - start_time))
        diff_backup_sources = self.db.check_which_jewel_sources_exist(tmp, self.device_name)
        print("3--- %s seconds ---" % (time.time() - start_time))
        # filter out everything, that is in diff_backup already
        full_backup_sources = [e for e in tmp if e not in diff_backup_sources]
        print("4--- %s seconds ---" % (time.time() - start_time))

        # execute,when not empty
        if diff_backup_sources:
            self.execute_backup(diff_backup_sources, verbose_level, start_time)
        print("5--- %s seconds ---" % (time.time() - start_time))
        # execute, when not empty
        if full_backup_sources:
            self.execute_fullbackup(full_backup_sources, verbose_level, start_time)
        print("6--- %s seconds ---" % (time.time() - start_time))    


    def execute_backup(self, jewel_sources, verbose_level, start_time):
        
        differential_backup_name = f"diff-{self.current_date_time_formatted}"
        backup_sources_for_r_sync = " ".join(jewel_sources)

        
        info_handler.check_db_hash(self.destination, differential_backup_name)

        subprocess_return_verbose = self.call_rsync_differential('aAXlnvv', backup_sources_for_r_sync, differential_backup_name)

        subprocess_return = self.call_rsync_differential('aAXln', backup_sources_for_r_sync, differential_backup_name)

        output_array = subprocess_return.splitlines()
        insert_results = self.read_files_and_jewel_from_rsync_output(output_array, jewel_sources,
                                                                     f"{self.destination}/{differential_backup_name}",
                                                                     self.destination + "/" + self.fullbackup_name)

        self.call_rsync_differential('aAX', backup_sources_for_r_sync, differential_backup_name)

        for hardlink_info in insert_results:
            self.set_hardlink(hardlink_info)

        info_handler.update_db_hash(self.destination, differential_backup_name)
        self.print_feedback(verbose_level, differential_backup_name, 'differential', subprocess_return_verbose, start_time)

       


    def execute_fullbackup(self, jewel_sources, verbose_level, start_time):

       
        info_handler.check_db_hash(self.destination, self.fullbackup_name)
        print("6--- %s seconds ---" % (time.time() - start_time))

        jewel_path_list_string = self.list_to_string(jewel_sources)
        output = self.call_rsync_full('aAX', jewel_path_list_string)
        output_array = output.splitlines()
        print("7--- %s seconds ---" % (time.time() - start_time))
        insert_results = self.read_files_and_jewel_from_rsync_output(output_array, jewel_sources,
                                                    f"{self.destination}/{self.fullbackup_name}",
                                                    self.destination + "/" + self.fullbackup_name)
        print("8--- %s seconds ---" % (time.time() - start_time))
        subprocess_return_verbose = self.call_rsync_full('aAXlnvv', jewel_path_list_string)
        print("9--- %s seconds ---" % (time.time() - start_time))
        for hardlink_info in insert_results:
            self.set_hardlink(hardlink_info)
        print("10--- %s seconds ---" % (time.time() - start_time))
        info_handler.update_db_hash(self.destination, self.fullbackup_name)
        self.print_feedback(verbose_level, self.fullbackup_name, 'full', subprocess_return_verbose, start_time)



    def list_to_string(self, string_list) -> str:
        formatted_string = " ".join(string_list)
        return formatted_string


    def filter_non_existing_paths(self, paths) -> list[str]:
        for jewel_path in paths:
            if not (os.path.exists(jewel_path)):
                paths.remove(jewel_path)
        return paths


    def read_files_and_jewel_from_rsync_output(self, output_array, jewel_sources, store_destination_body,
                                               fullbackup_store_destination_body) -> list[str | bool]:
        result = []
        if output_array == []:
            print("result ist leer")
            exit
        print("7.1--- %s seconds ---" % (time.time() - self.start_time))
        index = 0
        date_today=date.today()
        for line in output_array:
            # print("7.2--- %s seconds ---" % (time.time() - self.start_time))
            #print(line)
            # needed, since sometimes the first line ist not the jewel path,
            #happens only, if subfolder content changed
            if index == 0 or line.endswith('/'):
                # better solution? the for is needed in both cases, but each case need another prep work
                if index == 0:
                    self.current_source_path = os.path.dirname(line)+ "/"
                if line.endswith('/'):
                    self.current_source_path = line

                # check whether path is now the jewel
                for jewel_path in jewel_sources: # TODO get rid of this nested loop
                 
                    # stripping and splitting is needed, since comparison does not work otherwise
                    if jewel_path.rsplit('/', 1)[1].strip("/") == line.strip("/"):
                        jewel = Jewel(0, None, date_today, jewel_path, self.device_name,
                                      f'{fullbackup_store_destination_body}/{line.strip("/")}')
                        break
                    # if top layer of jewel was not changed, the jewel would not be in line.strip... so we need to split and get the first folder
                    elif jewel_path.rsplit('/', 1)[1].strip("/") == line.split("/")[0]:
                        print("ello?!")
                        jewel = Jewel(0, None, date_today, jewel_path, self.device_name,
                                      f'{fullbackup_store_destination_body}/{line.strip("/")}')
                        break

            else:
                # get only the working dir without the jewel(because line inherits the jewel)
                working_dir = jewel_path.rsplit('/', 1)[0]
                file_object = info_handler.get_metadata(working_dir + '/' + line)
                # Erstellt Array erstes element vor letztem Slash, zweites Element nach dem Slash
                file_name = line.rsplit('/', 1)[1]
                # print("7.5--- %s seconds ---" % (time.time() - self.start_time))
                blob = Blob(0, 0, file_object.f_hash, (f'{self.db._encode_base64(file_name)}_{file_object.f_hash}'),
                            file_object.f_size,
                            self.current_date_time, file_object.modify, 0, file_name,
                            working_dir + "/" + line, f'{store_destination_body}/{line}')

                file = File(0, [blob], file_object.birth)
                # print("7.6--- %s seconds ---" % (time.time() - self.start_time))
                db_answer = self.db.add_to_database(jewel, file, self.device_name)
                # print("7.7--- %s seconds ---" % (time.time() - self.start_time))

                if db_answer is not True:
                    result.append(HardlinkInfo(db_answer[0].id, db_answer[0].store_destination, blob.store_destination, self.current_date_time,blob.origin_name, working_dir + "/" + line, jewel.id, db_answer[1]))
            index = index +1
        print("7.9--- %s seconds ---" % (time.time() - self.start_time))
        self.db._commit_db()
        return result


    # Description:  Generate a String of excluded files which are handed over ,to the rsync command.
    # Input:        None
    # Output:       String containing the rsync option "--exclude" and the name of the excluded 
    #               files. Example: "--exclude "file1" --exclude "file2" ... --exclude "fileN""
    def excluding_data(self):
        config = info_handler.get_json_info(self.device_name)
        return_list = []
        for element in config['blacklist']['directories'] + config['blacklist']['files']:
            return_list.append(f'--exclude "{element}"')
        for extension in config['blacklist']['extensions']:
            return_list.append(f'--exclude *"{extension}"')
        return ' '.join(return_list)


    def set_hardlink(self, hl_info:HardlinkInfo ):
        d_path = os.path.dirname(os.path.abspath(hl_info.destination_path))
        try:
            os.listdir(d_path)
            #subprocess.run(f'ls "{d_path}"', shell=True)
        except:
            print(f'Error: ls couldn\'t be executed\n'
                  f'path: {d_path}\n')
            exit()
        os.remove(hl_info.destination_path)
        try:
            os.link(hl_info.link_path,hl_info.destination_path)
            #subprocess.run(f'ln "{hl_info.link_path}" "{hl_info.destination_path}"', shell=True)
        except:
            print(f'Error: ln couldn\'t be executed\n'
                  f'origin path: {hl_info.link_path}\n'
                  f'destination path: {hl_info.destination_path}\n')
            exit()
        if not hl_info.old_hardlink_existing:
            self.db.protocol_hardlink(hl_info, self.device_name)


    def print_feedback(self, verbose_level: int, backup_name: str, backup_type: str, subprocess_return_verbose: str, start_time: time):
        if backup_type == 'full':
            backup_path = f'{self.destination}/{self.fullbackup_name}'
        else:
            backup_path = f'{self.destination}/{backup_name}'

        files_amount = sum([len(files) for r, d, files in os.walk(backup_path)])
        files_size = sum(f.stat().st_size for f in Path(backup_path).glob('**/*') if f.is_file())
        
        backup_version = len(next(os.walk(self.destination))[1])

        config = info_handler.get_json_info(self.device_name)
        input_paths = config['jewel_sources'][self.device_name]
        excluded_amount = 0
        excluded_size = 0
        for line in subprocess_return_verbose.splitlines():
            if '[sender] hiding file' in line:
                excluded_file = line.split(' ')[3].split('/')[-1]
                excluded_amount += 1
                for input_path in reversed(input_paths):
                    try:
                        excluded_size += os.stat(f'{input_path}/{excluded_file}').st_size
                    except:
                        pass
            elif '[sender] hiding directory' in line:
                excluded_directory = ''.join(line.split(' ')[3].split('/')[1:])
                for input_path in reversed(input_paths):
                    try:
                        excluded_amount += sum([len(files) for r, d, files in os.walk(f'{input_path}/{excluded_directory}')])
                    except:
                        pass
                for input_path in reversed(input_paths):
                    try:
                        for path, dirs, files in os.walk(f'{input_path}/{excluded_directory}'):
                            for f in files:
                                fp = os.path.join(path, f)
                                excluded_size += os.path.getsize(fp)
                    except:
                        pass

        total_amount = sum([len(files) for r, d, files in os.walk(self.destination) if 'datenbank.db' not in files])
        total_size = sum(f.stat().st_size for f in Path(self.destination).glob('**/*') if f.is_file() and f.name != 'datenbank.db')

        database_size = os.stat(f'{self.destination}/datenbank.db').st_size
        print(self.destination)
        print(database_size)

        files_size_unit = 'bytes'
        excluded_size_unit = 'bytes'
        total_size_unit = 'bytes'
        database_size_unit = 'bytes'
        unit_list = ['bytes', 'kilobytes', 'megabytes', 'gigabytes']
        for i in range(len(unit_list) - 1, 0, -1):
            if (files_size / pow(1000, i)) >= 1:
                files_size = round((files_size / pow(1000, i)), 2)
                files_size_unit = unit_list[i]
            if (excluded_size / pow(1000, i)) >= 1:
                excluded_size = round((excluded_size / pow(1000, i)), 2)
                excluded_size_unit = unit_list[i]
            if (total_size / pow(1000, i)) >= 1:
                total_size = round((total_size / pow(1000, i)), 2)
                total_size_unit = unit_list[i]
            if (database_size / pow(1000, i)) >= 1:
                database_size = round((database_size / pow(1000, i)), 2)
                database_size_unit = unit_list[i]

        if verbose_level == 0:
            print(f'\nCURRENT BACKUP DETAILS\n'
                  f'├── backup name:\t\t\t{backup_name}\n'
                  f'├── number of files:\t\t\t{files_amount}\n'
                  f'│   └── size of files:\t\t\t{files_size} {files_size_unit}\n'
                  f'└── time elapsed:\t\t\t{round((time.time() - start_time), 2)} seconds\n')

            if backup_type == 'differential':
                print(f'\nOVERALL BACKUP DETAILS\n'
                      f'└── number of files:\t\t\t{total_amount}\n'
                      f'    └── size of files:\t\t\t{total_size} {total_size_unit}\n')
        
        elif verbose_level == 1:
            print(f'\nCURRENT BACKUP DETAILS\n'
                  f'├── backup name:\t\t\t{backup_name}\n'
                  f'├── backup type:\t\t\t{backup_type}\n'
                  f'├── backup version:\t\t\t{backup_version}\n'
                  f'├── number of files:\t\t\t{files_amount}\n'
                  f'│   └── size of files:\t\t\t{files_size} {files_size_unit}\n'
                  f'├── number of exluded files:\t\t{excluded_amount}\n'
                  f'│   └── size of excluded files:\t\t{excluded_size} {excluded_size_unit}\n'
                  f'└── time elapsed:\t\t\t{round((time.time() - start_time), 2)} seconds\n')

            if backup_type == 'differential':
                print(f'\nOVERALL BACKUP DETAILS\n'
                    f'├── number of files:\t\t\t{total_amount}\n'
                    f'│   └── size of files:\t\t\t{total_size} {total_size_unit}\n'
                    f'└── size of database:\t\t\t{database_size} {database_size_unit}\n')

    def call_rsync_differential(self, options: str, backup_sources_for_r_sync: str, backup_name: str):
        try:
            subprocess_output = subprocess.Popen(f"rsync -{options} {self.excluding_data()} --out-format='%n' "
                                                f"--compare-dest={self.destination}/{self.fullbackup_name} {backup_sources_for_r_sync} "
                                                f"{self.destination}/{backup_name}",
                                                shell=True,
                                                stdout=subprocess.PIPE)
            print("wait_decode_subprocess")
            output=[]
            for line in subprocess_output.stdout:
                output.append(line)
            return_value=''.join([x.decode('utf-8') for x in output])
            subprocess_output.stdout.close()
            subprocess_output.wait()
            return return_value
        except:
            print(f'Error: rsync couldn\'t be executed\n'
                  f'used option: {options}\n'
                  f'fullbackup path: {self.destination}/{self.fullbackup_name}\n'
                  f'destination path: {self.destination}/{backup_name}\n')
            exit()
    def call_rsync_full(self, options: str, jewel_path_list_string: str):
        try:
            subprocess_output = subprocess.Popen(f'rsync -{options} {self.excluding_data()} --out-format="%n" '
                                                f'{jewel_path_list_string} '
                                                f'{self.destination}/{self.fullbackup_name}',
                                                shell=True,
                                                stdout=subprocess.PIPE)
            print("wait_decode_subprocess")
            output=[]
            for line in subprocess_output.stdout:
                output.append(line)
            return_value=''.join([x.decode('utf-8') for x in output])
            subprocess_output.stdout.close()
            subprocess_output.wait()
            return return_value
        except:
            print(f'Error: rsync couldn\'t be executed\n'
                  f'used option: {options}\n'
                  f'jewel path: {jewel_path_list_string}\n'
                  f'destination path: {self.destination}/{self.fullbackup_name}\n')
            exit()

    def check_packages(self, required_packages: list):
        subprocess_output = ''
        for package in required_packages:
            try:
                subprocess_output = subprocess.Popen(f'dpkg -s {package}', shell=True, stdout=subprocess.PIPE)
                if 'Status: install ok installed' not in self.wait_decode_subprocess(subprocess_output):
                    print(f'Error: package "{package}" not installed')
                    exit()
            except:
                pass
