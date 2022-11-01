import tomli

with open("/home/fatih/projektBackup/myToml.toml", "rb") as f:
    toml_dict = tomli.load(f)
print(toml_dict["first"]["path"])
print(toml_dict["second"]["path2"])
print(toml_dict["data"])
print(toml_dict)

