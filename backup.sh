#!/bin/bash

destina="$PWD"
mkdir $destina/$1
rsync -av --progress  $destina/test.txt $destina/$1