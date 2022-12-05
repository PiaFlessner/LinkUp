import datetime
from datenbank import *
from datetime import datetime as date
import platform


restoreDay = date(2022,11,21,17,45)
daten = Datenbank()

blobs = daten.get_all_blobs_for_repair()
print(blobs[0])