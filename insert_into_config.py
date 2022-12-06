import json
import platform
import sys

json_file_name = "config.json"

def write_json(table_name, key, value, filename='config.json'):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[table_name][key] = value
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

list=[]
list.append("./unitTestFiles/jewel")
list.append("./unitTestFiles/jewel2")
#print(list)

table_name='jewel_sources' 
key=platform.node()
data=list
write_json(table_name, key, data)

table_name='destination'
key=platform.node()
data2="/home/gruppe/Schreibtisch/backupLocation"
write_json(table_name,key, data2)

table_name='restore_destination'
key=platform.node()
data3="/home/gruppe/Schreibtisch/Restore"
write_json(table_name,key, data3)

print("done with insert_into_config.py")