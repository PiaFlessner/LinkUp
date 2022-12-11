#!/usr/bin/env bash

if (($# < 3))
    then
    echo "3 parameters needed"
    exit
fi
mkdir ./jewel/make_Data_Dir
for ((x=1;x<=$1;x++))
do
    if [ ! -d $x ]; then    
        mkdir ./jewel/make_Data_Dir/$x
        for ((k=1;k<=$2;k++))
        do
            dd if=/dev/random bs=$3 count=1 of=./jewel/make_Data_Dir/$x/$k.bin
        done
    else
        echo "directory $x already exists"
    fi
done 