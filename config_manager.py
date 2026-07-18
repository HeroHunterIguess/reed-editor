### Initializing default config ###

from pathlib import Path
import os, shutil, importlib.util

def get_config_path():
    if os.name == "nt": # windows
        config_directory = Path(os.environ["APPDATA"]) / "reed" / "config.py"
    elif os.name == "posix": # unix-based
        config_directory = Path.home() / ".config" / "reed" / "config.py"
    
    return config_directory

def initialize_config():
    # get path
    config_path = get_config_path()

    # fill config file
    try:
        with open(config_path, "x") as main_config, open ("default_config.py", "r") as default_config:
            for line in default_config:
                main_config.write(line)
        
        # load config after file is created
        load_config(config_path)
    
    except FileExistsError:
        load_config(config_path)

def load_config(config_path):
    # load config into local easy to access file
    try:
        with open(config_path, "r") as remote_config, open("config.py", "w") as local_config:
            for line in remote_config:
                local_config.write(line)
    
    # create local config if it doesnt exist
    except FileNotFoundError:
        with open(config_path, "r") as remote_config, open("config.py", "x") as local_config:
            for line in remote_config:
                local_config.write(line)
