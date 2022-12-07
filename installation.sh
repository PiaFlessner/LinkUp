#!/bin/bash

#python3 -m venv .venv_deploy
#source .venv_deploy/bin/activate
#.venv_deploy/bin/pip install -r requirements.txt
sed -i "1i #!$(pwd)/.venv_deploy/bin/python3" $(pwd)/execute.py
chmod +x $(pwd)/execute.py
ln -s $(pwd)/execute.py /usr/local/bin/backupper
