
from array import array
from datenbank import *
from datetime import date

jewel = Jewel(1, None, date.today(), "test")
jewel2 = Jewel(1, None, date.today(), "hi")

backup1 = BackUp(1, 1, "dhdhsd", "Hallo", 3433, date.today(),23422, date.today(), date.today(), date.today(), 1)
backup2 = BackUp(2, 1, "dhdhsd", "Hallo", 3433, date.today(),23422, date.today(), date.today(), date.today(), 1)

backups_arr1 = [backup1]
backups_arr2 = [backup2]

file1 = File(1, "shdhsdd", "hallo", "helloworld.txt", backups_arr1)
file2 = File(2, "shdhsdd", "hallo", "helloworld.txt", backups_arr2)


daten = Datenbank()

def addToDataBase(jewel, file):
    jewel_id = daten.addJewel(jewel)
    file1_id = daten.addFile(file)
    daten.addJewelFileAssignment(jewel_id,file1_id)
    daten.addBackUp(file)
    
    #gibt es schon backups
    #nummer des letzten backups holen
    #backup mit letzem backup vergleichen
    #wenn gleich, nicht einfügen, wenn ungleich einfügen
    #neues backup inserten, mit erhöhter number
    

addToDataBase(jewel,file1)
#addToDataBase(jewel2,file1)



##daten.addBUFile(backfile1)
#daten.addBUFile(backfile2)

#daten.addBackUp(backup1)
#daten.addBackUp(backup2)

#backup1.set_number(4)
#backup1.set_iD_File(2)
#daten.updateBackUp(backup1)
#daten.addJewel(jewel)
#jewel.set_comment("Hallo")
#daten.updateJewel(jewel)
 
