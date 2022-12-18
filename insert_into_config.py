import json
import platform
import sys

json_file_name = "config.json"
def insert_for_test_backup():
    list = []
    list.append("/unitTestFiles/jewel")
    list.append("/unitTestFiles/jewel2")
    list.append("/unitTestFiles/jewel3")


    table_name = 'jewel_sources'
    key = "testCases"
    data = list
    write_json(table_name, key, data)

    table_name = 'destination'
    data2 = "unitTestFiles/backupLocation"
    write_json(table_name, key, data2)

    table_name = 'restore_destination'
    data3 = "unitTestFiles/restoreLocation"
    write_json(table_name, key, data3)

    # print("done with insert_into_config.py")


def write_json(table_name, key, value, filename=json_file_name):
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[table_name][key] = value
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)
        file.truncate()
