#!/usr/bin/env bash

cd test_Files_Backup/

mkdir jewel
mkdir jewel2
mkdir jewel3
mkdir ./jewel/Bad_Names_Dir
mkdir ./jewel/c++_Dir
mkdir ./jewel2/JDK_Dir

touch ./jewel/test.txt
touch ./jewel2/test1.txt
touch ./jewel3/test2.txt
echo "test" >> ./jewel/test.txt
echo "test" >> ./jewel2/test1.txt
echo "test" >> ./jewel3/test2.txt

cp -r ./special_Files/ jewel3
#tar -xf Bad_Names.tar.gz -C ./jewel/Bad_Names_Dir


find ./jewel3 -name "readOnly.*" -exec chmod ugo-rwx {} \;
find ./jewel3 -name "writeOnly.*" -exec chmod ugo-rwx {} \;
find ./jewel3 -name "execOnly.*" -exec chmod ugo-rwx {} \;

find ./jewel3 -name "readOnly.*" -exec chmod ugo+r {} \;
find ./jewel3 -name "writeOnly.*" -exec chmod ugo+w {} \;
find ./jewel3 -name "execOnly.*" -exec chmod ugo+x {} \;


find ./jewel3/special_Files/execOnly -type d -exec chmod ugo-rwx {} \;
find ./jewel3/special_Files/readOnly -type  d -exec chmod ugo-rwx {} \;
find ./jewel3/special_Files/writeOnly -type d -exec chmod ugo-rwx {} \;

find ./jewel3/special_Files/execOnly -type d -exec chmod ugo+x {} \;
find ./jewel3/special_Files/readOnly -type  d -exec chmod ugo+r {} \;
find ./jewel3/special_Files/writeOnly -type d -exec chmod ugo+w {} \;



# tar -xf C++_lib.tar.gz -C ./jewel/c++_Dir
# tar -xf JDK.tar.gz -C ./jewel2/JDK_Dir

#find ./jewel -exec touch {} \;
#find ./jewel2 -exec touch {} \;
