import datetime
from datenbank import *
from datetime import datetime as date
import platform


restoreDay = date(2022,11,21,17,45)
daten = Datenbank()

jewel = daten.get_restore_Jewel(restoreDay,1)
print(f"{jewel}: restore destination: {jewel.restore_destination}, jewel source: {jewel.jewel_source}\n")

file = daten.get_restore_File(restoreDay, "gruppe-VirtualBox/home/gruppe/backupTest/jewels/dritte_datei")
print(f"{file}\n")
 
