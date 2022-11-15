import shutil
import os

class TreeTraversal:
    def __init__(self, dirName): # Initialisierung der Variablen
        self.dirName = dirName
        self.fileAndDirList = []


    def getAllFiles(self):
        for root, dirs, files in os.walk(self.dirName): # "Walked" über das Verzeichnis und fügt in
            for file in files:                          # jeder Ebene die Dateien in eine Liste und gibt sie zurück
                self.fileAndDirList.append(os.path.join(root,file))
            for dir in dirs:
                self.fileAndDirList.append(os.path.join(root, dir))    
        print(self.fileAndDirList)
        return self.fileAndDirList
    
    
    # Parameter: Gewünschten files in Liste, Ordner, Dateien löschen mit gewünschten start Zeichen, Dateien löschen mit gewünschten ende Zeichen
    def deleteFiles(self, toDeleteFiles : list, directorys : list, start : str, end : str): 
        if not os.path.exists("/home/fatih/backupDestination"): # shutil kann keine Kopie erstellen wenn das Verzeichnis bereits existiert
            shutil.copytree(self.dirName, "/home/fatih/backupDestination") # bevor wir Daten löschen wird das Verzeichnis Kopiert

        for root, dirs, files in os.walk("/home/fatih/backupDestination"): # Verzeichnis wird Traversiert und anhand Argumenten die Daten entfernt
            for file in files:
                if (file.startswith(start) or file.endswith(end)) or file in toDeleteFiles:
                    os.remove(os.path.join(root, file))
                
            for dir in dirs:    
                if dir in directorys:
                    os.rmdir(os.path.join(root, dir))
        
    # Ausgabe des Target Verzeichnis ohne Gelöschter Files             
    def printTree(self):
        for root, dirs, files in os.walk(self.dirName): # Traversieren des Verzeichnise
            path = root.split(os.sep)[1:]   # Liste mit den Ordnern des Root Path
            print("path: ", path)
            print((len(path) - 1) * '---', os.path.basename(root)) # Ausgabe Name des Root Ordner
            for file in files:
                print(len(path) * '---', file) # Ausgabe der Dateien

# Übergabe der Argumente
# t = TreeTraversal("/home/fatih/projektBackup/testdir")
# print("#################")
# t.printTree()
# print("#################")
# t.getAllFiles()
# print("#################")
# t.deleteFiles(["file1", "topSecret.txt"], ["meinOrdner", "Ordner"], "start", "4")



