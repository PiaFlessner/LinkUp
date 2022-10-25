from datenbank import *
import argparse
import datetime
import sys
from rich.console import Console
from rich.table import Table

last_input = None

# self,id,comment, monitoring_Startdate, jewelSource):
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
        console.print(table)

    else: console.print("No jewels have been created by the user yet")
    


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
    else: console.print("No files have been created by the user yet")


def show_all_blobs():
    daten = Datenbank()
    blobs = daten.get_all_Blobs()
    console = Console()

    if blobs is not None:
        table = Table(title="All Files")
        table.add_column("File ID", justify="left", style="black", no_wrap=True)
        table.add_column("Number of BackUps", justify="left", style="black", no_wrap=True)
        table.add_column("File birth", justify="left", style="black", no_wrap=True)

    for blob in blobs:



# Hier startet das Programm
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dies ist eine Beschreibung des Programms",
                                     epilog="Dies ist der Epilog")
    parser.add_argument('-sJ', type=str, help='Show Jewels')
    parser.add_argument('-sF', type=str, help='Show Files')
    parser.add_argument('-sB', type=str, help='Show Blobs')
# -sJ 4 -sB 5 
    arglist = sys.argv
    is_number = bool(0)
    number = 0

    for arg in arglist:
         if arglist[1] == '-sJ' and last_input is None : last_input = 0
         if arglist[1] == '-sF' and last_input is None : last_input = 1
         if arglist[1] == '-sB' and last_input is None : last_input = 2

         if last_input is not None:
             is_number = any(char.isdigit() for char in arg)
             if is_number:
                print("Test")

   