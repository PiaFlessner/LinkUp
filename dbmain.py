from array import array
from datenbank import *
from datetime import date

jewel = Jewel(1, None, date.today(), "test")
jewel2 = Jewel(1, None, date.today(), "hi")
jewel3 = Jewel(1,"3. Jewel", date.today(), "3.")

blob1 = Blob(1, 1, "dhdhsd", "Hallo", 3433, date.today(), date.today(), date.today(), date.today(), 1)
blob1v2 = Blob(1, 1, "dhdhdsd", "Hallo", 3433, date.today(), date.today(), date.today(), date.today(), 1)
blob2 = Blob(1, 1, "asdasd", "Hallo", 3433, date.today(), date.today(), date.today(), date.today(), 2)

blobs_arr1 = [blob1]
blobs_arr2 = [blob1v2]
blobs_arr1v2 = [blob2]

file1 = File(1, "shdhsdd", "hallo", "helloworld.txt", blobs_arr1)
file2 = File(2, "shdhsdd", "hallo", "helloworld.txt", blobs_arr2)
file1v2 = File(1, "shdhsdd", "hallo", "helloworld.txt", blobs_arr1v2)


daten = Datenbank()

#Test ob File und backups doppelt hinzugefügt werden.
#hinzufügen von jewel
daten.addToDataBase(jewel,file1)
#hinzufügen von  neuen jewel mit gleicher file
daten.addToDataBase(jewel2,file1)
#hinzufügen von alten jewel mit alter file, aber neuem backup (zu erkennen am veränderten Hash)
daten.addToDataBase(jewel,file1v2)
 
