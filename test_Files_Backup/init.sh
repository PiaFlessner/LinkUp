#!/usr/bin/env bash

cd test_Files_Backup/
mkdir ./jewel/Bad_Names_Dir
mkdir ./jewel/c++_Dir
mkdir ./jewel2/JDK_Dir
touch ./jewel2/test.txt
echo "test" >> ./jewel2/test.txt

tar -xf Bad_Names.tar.gz -C ./jewel/Bad_Names_Dir
#tar -xf C++_lib.tar.gz -C ./jewel/c++_Dir
#tar -xf JDK.tar.gz -C ./jewel2/JDK_Dir

#find ./jewel -exec touch {} \;
#find ./jewel2 -exec touch {} \;
