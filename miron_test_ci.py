import os

destination="meep"
os.makedirs(destination, exist_ok=True)
if not(os.path.exists(destination)):
    print("Creating " + destination +"-destination directory failed")
    raise TypeError
else:
    print("test.py success")