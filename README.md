# Projektgruppe

This program is able to backup whole directories as well as restore them and error check them.
Also there are functions to display the database and the inherited files.

# Minimum Requirements
1. MacOS (v. 10) or Linux (tested on Ubuntu 22.04 and Fedora v. 37)
2. Rsync v.3.2.7
3. Python v 3.11.1

# Install

1. Ensure to put the whole archive, were you want it to be. For example in /opt/.
2. Open the terminal in the project directory (IMPORTANT -> ignoring it, will cause errors in the future).
3. Make sure, that the installation.sh is executable:
```
chmod +x install.sh
```
4. Now execute the "install.sh" with sudo rights:
```
sudo ./install.sh
```

Now the programm can be executed from everywhere. It can be called by:
```
linkup [arguments]
```

## Problems
1. Symlink could not be created (file is already existing)
If this is not caused, because the program is already installed, then you may have to rename the program.
This is done by renaming the symlink name (linkup) in the installation.sh to another name.
CAUTION: this name will be the calling name. Renaming it, means, that all calling examples in the following are renamed to the choosen name.`

# Uninstall

1. Open the terminal in the project directory (IMPORTANT -> ignoring it, will cause errors).
2. Make sure, that the uninstall.sh is executable:
```
chmod +x uninstall.sh
```
4. Now execute the "uninstall.sh" with sudo rights:
```
sudo ./uninstall.sh
```

The program is now deinstalled from the system.

# Config

The config.json is needed to run the program properly.
Mostly all properties need device names. 

## jewel_sources

Defines the jewels which will be considered in the backup.

The structure needs to be exactly like this:

```
 "jewel_sources" :
  {
    "device_name": ["absolute/jewel/path", "absolute/jewel/path2"],
  },

```

The device name describes the device on which the backup is now running.
The jewel paths need to be absolute und defines the starting points of the backup process.
IMPORTANT: the path is not allowed to end with an slash (/)!

## blacklist

the blacklist property let the user define directories, extensions and files which should not be regocnized in the whole backup process.
TODO: further informations about the usage of the properties.

```
"blacklist" :
  {
    "directories": ["folderToIgnore1", "folderToIgnore2"],
    "extensions": [".tmp", ".html"],
    "files": ["fileToIgnore1.png", "fileToIgnore2.jpg", "fileToIgnore.txt"]
  },
  
```
## destination

 Describes the destination for the backup files.

  ```
  "destination":
  {
    "device_name": "/home/gruppe/Schreibtisch/backupLocation"
  },

  ```

 The device name describes the device on which the backup is now running.
 Destination needs to be an absolute path.
 IMPORTANT: the path is not allowed to end with an slash (/)!

## restore_destination
  Describes the Restore Destination for the restoring process. All restored data will be copied there.

  ```
  "restore_destination":
  {
    "device_name": "/home/gruppe/Schreibtisch/Restore"
  }
  ```

 The device name describes the device on which the backup is now running.
 Destination needs to be an absolute path.
 IMPORTANT: the path is not allowed to end with an slash (/)!

# Running

## Backup Section

Backup is needed to start the backup process. The backup process will backup all paths which were contributed in the config.json under the jewel_sources property.
The backup will be stored in the backup path defined in the "destination" property in the config.json.

```
linkup backup
```

## Restore Section

Restore is needed to restore files or jewels. The files will be restored in the restore path defined in the config.json.

### Commands
To restore a Jewel or a File just use the matching flag following by the id of the File or Jewel.
-F for Files
-J for Jewels

The ID of Files are text based.
The ID of Jewels are number based.

The Datetime format is expected to be in ISO-Format (yyyy-mm-dd-MM-ss)
If the user only provides the day, the program will restore the last trending backup of this day.

```
linkup restore -F|-J [id] [datetime]
```

## Show Section
Jewels, files, blobs and skipped files can be displayed as tables with different verbose levels.
The higher the verbose level, the more columns are displayed.

### Commands
To show all objects use the matching flag without an id.
To show a specific object use the matching flag with the id.

-J for Jewels 
-F for Files
-B for Blobs 
-sF skipped Files

There are different verbose levels.
    without a parameter displays the most important columns.
-v  displays the columns with medium importance.
-vv displays all columns.

```
linkup show -F|-J|-B|-sF [id] [-v|-vv]
```

## Reset Section
Resets all the backups for the device on which the reset is performed.

```
linkup reset
```

#Further Problems
To create a Backup of a jewel with a file, which can only be accessed with admin rights, LinkUp must be executed with admin rights.
LinkUp cannot backup this file otherwise.


