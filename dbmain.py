import datetime
from datenbank import *
from datetime import datetime as date
import platform


restoreDay = date(2022,11,18,17,45)
daten = Datenbank()

jewel = daten.get_restore_Jewel(restoreDay,1)
print(f"{jewel[1]}\n")

file = daten.get_restore_File(restoreDay, "gruppe-VirtualBox/home/gruppe/backupTest/jewels/dritte_datei")
print(f"{file}\n")
 
