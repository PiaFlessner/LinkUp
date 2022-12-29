#!/usr/bin/env bash
rm -rf .venv
tail -n +2 $(pwd)/execute.py > $(pwd)/tmp.py && mv $(pwd)/tmp.py $(pwd)/execute.py
rm /usr/local/bin/linkup
