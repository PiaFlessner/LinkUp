import datetime
from datenbank import *
from datetime import datetime as date
import platform

samedate0 = date(2013,1,1,0,0,0)
samedate1 = date(2013,2,1,0,0,0)
samedate2 = date(2013,3,1,0,0,0)

jewel = Jewel(1, "1. Jewel", date.today(), "test")
jewel2 = Jewel(1, "2. Jewel", date.today(), "hi")
jewel3 = Jewel(1,"3. Jewel", date.today(), "3.")


blob1 = Blob(0,0,999999,"hs99999",700,samedate0,samedate0,samedate0,0,"Blob1File1.txt", "Desktop","HDD")
blob1v2 = Blob(0,0,999998,"hs99998",700,samedate0,samedate0,samedate1,0,"Blob1File1.txt", "Desktop","HDD")
blob1v3 = Blob(0,0,999998,"hs99997",700,samedate0,samedate0,samedate2,0,"Blob2File1.txt", "Desktop","HDD")

blob2 = Blob(0,0,5677777,"hs88777",100,samedate0,samedate0,samedate0,0,"Blob2File2.txt", "Desktop","HDD")


blobs_arr1 = [blob1]
blobs_arr2 = [blob2]
blobs_arr1v2 = [blob1v2]
blobs_arr1v3 = [blob1v3]


file1 = File(0,blobs_arr1,samedate1)
file2 = File(0,blobs_arr2, samedate2)
file1v2 = File(0,blobs_arr1v2, samedate1)
file1v3 = File(0,blobs_arr1v3, samedate1)


daten = Datenbank()
#%%
#Test ob File und backups doppelt hinzugefügt werden.
#hinzufügen von jewel
result = daten.add_to_database(jewel2, file1, platform.node()) #true expected (first run)
print(result)
result = daten.add_to_database(jewel2, file1v2, platform.node()) #true expected (first run)
print(result)
result = daten.add_to_database(jewel, file1v3, platform.node()) #true expected (first run)
print(result)
result = daten.add_to_database(jewel2, file1v3, platform.node()) #false expected (first run)
print(result)
result = daten.add_to_database(jewel, file2, platform.node()) #true expected (first run)
print(result)
result = daten.add_to_database(jewel2, file1v3, platform.node()) #false expected (first run)
print(result)

 
