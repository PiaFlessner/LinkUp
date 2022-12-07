#!/bin/bash

#python3 -m venv .venv_deploy
#source .venv_deploy/bin/activate
#.venv_deploy/bin/pip install -r requirements.txt
sed -i '1d' $(pwd)/execute.py
rm /usr/local/bin/backupper
