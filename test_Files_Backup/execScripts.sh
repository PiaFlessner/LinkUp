#!/usr/bin/env bash
cd test_Files_Backup/
./makeData.sh $1 $2 $3
./makeDataAndLink.sh $1 $2 $3
# ./makeLink.sh

# find ./jewel -exec touch {} \;
# find ./jewel2 -exec touch {} \;
# find ./backup_Location -exec touch {} \;