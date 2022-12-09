#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate
.venv/bin/pip install -r requirements.txt --no-index --find-links $(pwd)/lib_src/
sed -i "1i #!$(pwd)/.venv/bin/python3" $(pwd)/execute.py
chmod +x $(pwd)/execute.py
ln -s $(pwd)/execute.py /usr/local/bin/backupper
