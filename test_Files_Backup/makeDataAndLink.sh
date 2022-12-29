#!/usr/bin/env bash

if (($# < 3))
    then
    echo "3 parameters needed"
    exit
fi
mkdir ./jewel2/data_And_Link_Dir
for ((x=1;x<=$1;x++))
do
    if [ ! -d $x ]; then    
        mkdir ./jewel2/data_And_Link_Dir/$x
        # mkdir ./jewel2/data_And_Link_Dir/datalink$x
        for ((k=1;k<=$2;k++))
        do
            dd if=/dev/urandom bs=$3 count=1 of=./jewel2/data_And_Link_Dir/$x/$k.bin iflag=fullblock
            #ln ./jewel2/data_And_Link_Dir/$x/$k.bin ./jewel2/data_And_Link_Dir/datalink$x/hardlink$k.bin 
            #ln -s ./jewel2/data_And_Link_Dir/$x/$k.bin ./jewel2/data_And_Link_Dir/datalink$x/softlink$k.bin
        done
    else
        echo "directory $x already exists"
    fi
done 