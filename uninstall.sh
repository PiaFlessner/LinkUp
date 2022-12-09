#!/bin/bash
rm -rf .venv
sed -i '1d' $(pwd)/execute.py
rm /usr/local/bin/backupper
