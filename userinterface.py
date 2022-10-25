from datenbank import *
import argparse
import datetime
import sys
from rich.console import Console
from rich.table import Table


def show_all_jewels():
    daten = Datenbank()
    jewels = daten.get_all_Jewels()
    console = Console()

    if jewels is not None:
        table = Table(title="All jewels")
        table.add_column("Jewel ID", justify="left", style="black", no_wrap=True)
        table.add_column("Comment", justify="left", style="black", no_wrap=True)
        table.add_column("Monitoring startdate", justify="left", style="black", no_wrap=True)
        table.add_column("Source of the jewel", justify="left", style="black", no_wrap=True)

        for jewel in jewels:
            table.add_row(str(jewel.id), str(jewel.comment), str(jewel.monitoring_Startdate), str(jewel.jewelSource))
        
        console.print("\n")
        console.print(table)

    else: 
        console.print("\nNo jewels have been created by the user yet")
    


def show_all_files():
    daten = Datenbank()
    files = daten.get_all_Files()
    console = Console()

    if files is not None:
        table = Table(title="All Files")
        table.add_column("File ID", justify="left", style="black", no_wrap=True)
        table.add_column("Number of BackUps", justify="left", style="black", no_wrap=True)
        table.add_column("File birth", justify="left", style="black", no_wrap=True)

        for file in files:
            table.add_row(str(file.id), str(len(file.blobs)), str(file.birth))
        console.print("\n")
        console.print(table)
        
    else: 
        console.print("\nNo files have been created by the user yet")


def show_all_blobs():
    daten = Datenbank()
    blobs = daten.get_all_Blobs()
    console = Console()

    if blobs is not None:
        table = Table(title="All Blobs")
        table.add_column("Blob ID", justify="left", style="black", no_wrap=False)
        table.add_column("File version", justify="left", style="black", no_wrap= False)
        table.add_column("Hash", justify="left", style="black", no_wrap= False)
        table.add_column("Name", justify="left", style="black", no_wrap= False)
        table.add_column("File size", justify="left", style="black", no_wrap= False)
        table.add_column("Creationdate", justify="left", style="black", no_wrap=False)
        table.add_column("Change", justify="left", style="black", no_wrap= False)
        table.add_column("Modify", justify="left", style="black", no_wrap= False)
        table.add_column("File ID", justify="left", style="black", no_wrap=False)
        table.add_column("Origin name", justify="left", style="black", no_wrap= False)
        table.add_column("Source path", justify="left", style="black", no_wrap=False)
        table.add_column("Store destination", justify="left", style="black", no_wrap=False)

        for blob in blobs:
            table.add_row(str(blob.id), str(blob.number), str(blob.hash), str(blob.name), str(blob.fileSize), str(blob.creationDate),
           str(blob.change), str(blob.modify), str(blob.iD_File), str(blob.origin_name), str(blob.source_path), str(blob.store_destination))
        console.print("\n")
        console.print(table)

    else: console.print("\nNo blobs have been created by the user yet")

def show_jewel_via_id(id):
    daten = Datenbank()
    jewel = daten.get_Jewel_via_id(id)
    text = "Jewel: " + str(id)
    console = Console() 

    if jewel is not None:
        table = Table(title= text)
        table.add_column("Jewel ID", justify="left", style="black", no_wrap=True)
        table.add_column("Comment", justify="left", style="black", no_wrap=True)
        table.add_column("Monitoring startdate", justify="left", style="black", no_wrap=True)
        table.add_column("Source of the jewel", justify="left", style="black", no_wrap=True)
        table.add_row(str(jewel.id), str(jewel.comment), str(jewel.monitoring_Startdate), str(jewel.jewelSource))
        filetable = Table(title= "Files of the jewel " + str(id))
        files = daten.get_Files_via_jewel_id(id)
        filetable.add_column("File ID", justify="left", style="black", no_wrap=True)
        filetable.add_column("Number of BackUps", justify="left", style="black", no_wrap=True)
        filetable.add_column("File birth", justify="left", style="black", no_wrap=True)

        for file in files:
            filetable.add_row(str(file.id), str(len(file.blobs)), str(file.birth))

        console.print("\n")
        console.print(table)
        console.print("\n")
        console.print(filetable)


    else: console.print("\nThere is no jewel with the id " + str(id))


def show_file_via_id (id):
    daten = Datenbank()
    file = daten.get_File_via_id(id)
    text = "File: " + str(id)
    console = Console()

    if file is not None:
        table = Table(title= text)
        table.add_column("File ID", justify="left", style="black", no_wrap=True)
        table.add_column("Number of BackUps", justify="left", style="black", no_wrap=True)
        table.add_column("File birth", justify="left", style="black", no_wrap=True)
        table.add_row(str(file.id), str(len(file.blobs)), str(file.birth))
        console.print("\n")
        console.print(table)

        blobtable = Table(title= "Blobs of the file " + str(id))
        blobtable.add_column("Blob ID", justify="left", style="black", no_wrap=False)
        blobtable.add_column("File version", justify="left", style="black", no_wrap= False)
        blobtable.add_column("Hash", justify="left", style="black", no_wrap= False)
        blobtable.add_column("Name", justify="left", style="black", no_wrap= False)
        blobtable.add_column("File size", justify="left", style="black", no_wrap= False)
        blobtable.add_column("Creationdate", justify="left", style="black", no_wrap= False)
        blobtable.add_column("Change", justify="left", style="black", no_wrap= False)
        blobtable.add_column("Modify", justify="left", style="black", no_wrap= False)
        blobtable.add_column("File ID", justify="left", style="black", no_wrap= False)
        blobtable.add_column("Origin name", justify="left", style="black", no_wrap=False)
        blobtable.add_column("Source path", justify="left", style="black", no_wrap=False)
        blobtable.add_column("Store destination", justify="left", style="black", no_wrap=False)

        for blob in file.blobs:
            blobtable.add_row(str(blob.id), str(blob.number), str(blob.hash), str(blob.name), str(blob.fileSize), str(blob.creationDate),
            str(blob.change), str(blob.modify), str(blob.iD_File), str(blob.origin_name), str(blob.source_path), str(blob.store_destination) )
        
        console.print("\n")
        console.print(blobtable)

    else: console.print("\nThere is no file with the id " + str(id))



def show_blob_via_id (id):
     daten = Datenbank()
     blob = daten.get_Blob_via_id(id)
     text = "Blob: " + str(id)
     console = Console()

     if blob is not None:
        table = Table(title=text)
        table.add_column("Blob ID", justify="left", style="black", no_wrap=True)
        table.add_column("File version", justify="left", style="black", no_wrap=True)
        table.add_column("Hash", justify="left", style="black", no_wrap=True)
        table.add_column("Name", justify="left", style="black", no_wrap=True)
        table.add_column("File size", justify="left", style="black", no_wrap=True)
        table.add_column("Creationdate", justify="left", style="black", no_wrap=True)
        table.add_column("Change", justify="left", style="black", no_wrap=True)
        table.add_column("Modify", justify="left", style="black", no_wrap=True)
        table.add_column("File ID", justify="left", style="black", no_wrap=True)
        table.add_column("Origin name", justify="left", style="black", no_wrap=True)
        table.add_column("Source path", justify="left", style="black", no_wrap=True)
        table.add_column("Store destination", justify="left", style="black", no_wrap=True)
        table.add_row(str(blob.id), str(blob.number), str(blob.hash), str(blob.name), str(blob.fileSize), str(blob.creationDate),
        str(blob.change), str(blob.modify), str(blob.iD_File), str(blob.origin_name), str(blob.source_path), str(blob.store_destination) )
        console.print("\n")
        console.print(table)
     else:  
        console.print("\nThere is no blob with the id " + str(id))


# Hier startet das Programm
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Dies ist eine Beschreibung des Programms",
                                     epilog="Dies ist der Epilog")
    parser.add_argument('-sJ', type=str, help='Show Jewels')
    parser.add_argument('-sF', type=str, help='Show Files')
    parser.add_argument('-sB', type=str, help='Show Blobs')

    arglist = sys.argv
    if len(arglist) != 1:
        if len(arglist) == 2: 
            if arglist[1] == '-sJ' : show_all_jewels()
            if arglist[1] == '-sF' : show_all_files()
            if arglist[1] == '-sB': show_all_blobs()
        else: 
            # Prüft, ob das dritte Argument eine Zahl ist
            if (any(char.isdigit() for char in arglist[2])):
                number = int(arglist[2])
                if arglist[1] == '-sJ' : show_jewel_via_id(number)
                if arglist[1] == '-sF' : show_file_via_id(number)
                if arglist[1] == '-sB': show_blob_via_id(number)


    
