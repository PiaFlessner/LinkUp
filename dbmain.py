from datenbank import *
from datetime import datetime as date

jewel = Jewel(1, None, date.today(), "test")
jewel2 = Jewel(1, None, date.today(), "hi")
jewel3 = Jewel(1,"3. Jewel", date.today(), "3.")

blob1 = Blob(0,0,999999,"hs99999",700,date.today(),date.today(),555,0,"Blob1File1.txt", "Desktop","HDD")
blob1v2 = Blob(0,0,999998,"hs99998",700,date.today(),date.today(),666,0,"Blob1File1.txt", "Desktop","HDD")
blob1v3 = Blob(0,0,999998,"hs99997",700,date.today(),date.today(),777,0,"Blob2File1.txt", "Desktop","HDD")

blob2 = Blob(0,0,5677777,"hs88777",100,date.today(),date.today(),date.today(),0,"Blob2File2.txt", "Desktop","HDD")


blobs_arr1 = [blob1]
blobs_arr2 = [blob2]
blobs_arr1v2 = [blob1v2]
blobs_arr1v3 = [blob1v3]

file1 = File(0,blobs_arr1,"444")
file2 = File(0,blobs_arr2, "555")
file1v2 = File(0,blobs_arr1v2, "444")
file1v3 = File(0,blobs_arr1v3, "444")


daten = Datenbank()
#%%
#Test ob File und backups doppelt hinzugefügt werden.
#hinzufügen von jewel
#daten.addToDataBase(jewel,file1)
result = daten.addToDataBase(jewel2, file1)
print(result)
result = daten.addToDataBase(jewel2, file1v2)
print(result)
result = daten.addToDataBase(jewel, file1v3)
print(result)
result = daten.addToDataBase(jewel2, file1v3)
print(result)
result = daten.addToDataBase(jewel, file2)
print(result)
result = daten.addToDataBase(jewel2, file1v3)
print(result)
#hinzufügen von  neuen jewel mit gleicher file
#daten.addToDataBase(jewel2,file1)
#hinzufügen von alten jewel mit alter file, aber neuem backup (zu erkennen am veränderten Hash)
#daten.addToDataBase(jewel,file1v2)
 
