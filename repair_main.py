from datenbank import Datenbank
from repair import Repair

repair=Repair()
daten = Datenbank()
blobs = daten.get_all_Blobs()
for i in range(len(blobs)):
    repair.create_repair_data(blobs[i])
    
for i in range(len(blobs)):
    repair.repair_file(blobs[i])