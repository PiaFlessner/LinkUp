#!/usr/bin/env bash
pa=$(pwd)
commando="#!$pa/.venv/bin/python3"
python3 -m venv .venv
source .venv/bin/activate
.venv/bin/pip install -r requirements.txt --no-index --find-links $(pwd)/lib_src/
#sed -i "1i #!$(pwd)/.venv/bin/python3" $(pwd)/execute.py
cp execute.py execute.py.backup
echo $commando > execute.py
cat execute.py.backup | tail -n+2>> execute.py
chmod +x $(pwd)/execute.py
ln -s $(pwd)/execute.py /usr/local/bin/linkup
rm execute.py.backup