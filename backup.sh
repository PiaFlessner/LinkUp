#!/bin/bash

current_path="$PWD"
mkdir $current_path/$1
rsync -av --progress  $current_path/test.txt $current_path/$1