#!/usr/bin/env bash

mkdir ./jewel/original1
mkdir ./jewel/original1/original2
mkdir ./jewel/original1/original2/original3
mkdir ./jewel/original1/original2/original3/original4
mkdir ./jewel/original1/original2/original3/original4/original5

mkdir ./jewel2/link1
mkdir ./jewel2/link1/link2
mkdir ./jewel2/link1/link2/link3
mkdir ./jewel2/link1/link2/link3/link4
mkdir ./jewel2/link1/link2/link3/link4/link5

touch ./jewel/original1/original1
touch ./jewel/original1/original2/original2
touch ./jewel/original1/original2/original3/original3
touch ./jewel/original1/original2/original3/original4/original4
touch ./jewel/original1/original2/original3/original4/original5/original5

echo "Datei 1" >> ./jewel/original1/original1
echo "Datei 2" >> ./jewel/original1/original2/original2
echo "Datei 3" >> ./jewel/original1/original2/original3/original3
echo "Datei 4" >> ./jewel/original1/original2/original3/original4/original4
echo "Datei 5" >> ./jewel/original1/original2/original3/original4/original5/original5

ln ./jewel/original1/original1 ./jewel2/link1/hardlink1
ln ./jewel/original1/original2/original2 ./jewel2/link1/link2/hardlink2
ln ./jewel/original1/original2/original3/original3 ./jewel2/link1/link2/link3/hardlink3
ln ./jewel/original1/original2/original3/original4/original4 ./jewel2/link1/link2/link3/link4/hardlink4
ln ./jewel/original1/original2/original3/original4/original5/original5 ./jewel2/link1/link2/link3/link4/link5/hardlink5

ln -s ./jewel/original1/original1 ./jewel2/link1/softlink1
ln -s ./jewel/original1/original2/original2 ./jewel2/link1/link2/softlink2
ln -s ./jewel/original1/original2/original3/original3 ./jewel2/link1/link2/link3/softlink3
ln -s ./jewel/original1/original2/original3/original4/original4 ./jewel2/link1/link2/link3/link4/softlink4
ln -s ./jewel/original1/original2/original3/original4/original5/original5 ./jewel2/link1/link2/link3/link4/link5/softlink5