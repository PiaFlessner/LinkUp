# Projektgruppe

This program is able to backup whole directories as well as restore them and error check them.
Also there are functions to display the database and the inherited files.

# Installation

1. Ensure to put the whole archive, were you want it to be. For example in /opt/.
2. Open the terminal in the project directory (IMPORTANT).
3. Make sure, that the installation.sh is executable:
```
chmod +x installation.sh
```
4. Now execute the "installation.sh" with sudo rights:
```
sudo ./installation.sh
```

Now the programm can be executed from everywhere. It can be called by:
```
backupper [ærguments]
```

## Problems
1. Symlink could not be created (file is already existing)
If this is not caused, because the program is already installed, then you may have to rename the program.
This is done by renaming the symlink name (backupper) in the installation.sh to another name.
CAUTION: this name will be the calling name. Renaming it, means, that all calling examples in the following are renamed to the choosen name.`

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
execute.py backup
```

## Restore Section

Restore is needed to restore files or jewels. The files will be restored in the restore path defined in the config.json.

### commands
To restore a Jewel or a File just use the matching flag following by the id of the File or Jewel.
-F for Files
-J for Jewels

The ID of Files are text based.
The ID of Jewels are number based.

The Datetime format is expected to be in ISO-Format (yyyy-mm-dd-MM-ss)
If the user only provides the day, the program will restore the last trending backup of this day.

```
execute.py restore -F|-J [id] [datetime]
```

## Show Section

```
execute.py show -F|-J|-B [id]
```
TODO




## Projekt importieren
### Section 1 - Personal Access Token generieren 
1. Auf euer Profilbild oben rechts gehen
2. Edit profile auswählen
3. Rechts auf Access Tokens klicken
4. Dem Token einen Namen geben
5. Das Ablaufdatum auf irgendwann nächstes Jahr setzen
6. Unter Select scopes write_repository auswählen
7. Unten auf Create personal access token klicken
8. Access Token unbedingt irgendwo lokal auf eurem Rechner speichern

### Section 2 - Repository klonen
1. Das Repository Projektgruppe auswählen
2. Auf Clone klicken (der farbige Button rechts)
3. Unter Open in your IDE -> Visual Studio Code (HTTPS) auswählen
4. In Visual Studio Code einen Ordner auswählen in dem das Projekt leben soll
5. Euren Nutzernamen eingeben (Findet ihr wieder oben rechts auf GitLab, steht unter eurem Bild hinter dem @)
6. Das Passwort eingeben (das Passwort ist in diesem Fall der Personal Access Token aus Schritt 1)

### Section 3 - Das Projekt initialisieren (noch nicht nötig da wir bis jetzt keine Dependencies haben)
Alle Befehle werden in der Konsole im Projektverzeichnis eingegeben.
1. virtualenv env
2. source env/bin/activate
3. pip install -r requirements.txt
4. Zum Beenden der virtualenv: deactivate

### Section 4 - Dependencies installieren
1. source env/bin/activate
2. pip install [options] [package name]
3. pip freeze > requirements.txt
4. deactivate

### Section 5 - Mit SSH verbinden
In der Konsole:
1. ssh-keygen -t ed25519
2. Jetzt werdet ihr nach einigen Parametern gefragt, drückt einfach Enter bis ihr durch seid
3. Navigiert in das Verzeichnis, in dem der Key gespeichert wurde mit cd /home/__Nutzername__/.ssh
4. cat id_ed25519.pub
5. Kopiert die gesamte Ausgabe des cat Befehls

Auf der Gitlab Seite:
1. Geht auf euer Bild und dann *preferences*
2. An der Seite steht ein Reiter *SSH Keys*
3. Fügt dort unter Key die Ausgabe von cat ein
4. Drückt auf *Add key*
