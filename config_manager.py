### Initializing configuration ###


from pathlib import Path
import os, shutil, importlib.util

# TESTING OPTION TO ALWAYS SOURCE FROM DEFAULT
USE_DEFAULT_CONFIG = False

def get_config_path():
    if os.name == "nt": # windows
        config_directory = Path(os.environ["APPDATA"]) / "reed" / "config.py"
    elif os.name == "posix": # unix-based
        config_directory = Path.home() / ".config" / "reed" / "config.py"
    
    # Override config path and use default
    if USE_DEFAULT_CONFIG:
        return Path("default_config.py")
    
    return config_directory

def initialize_config():
    # get path
    config_path = get_config_path()

    # If using real config then create it if the dir doesnt exist
    if not USE_DEFAULT_CONFIG:
        config_path.parent.mkdir(parents=True, exist_ok=True)

    # fill config file
    try:
        with open(config_path, "x") as main_config, open ("default_config.py", "r") as default_config:
            for line in default_config:
                main_config.write(line)
    
    except FileExistsError:
        pass
    
    # load and return module data
    return load_config(config_path)

def load_config(config_path):
    # load config into local module
    module_spec = importlib.util.spec_from_file_location("config", config_path)

    config = importlib.util.module_from_spec(module_spec)

    module_spec.loader.exec_module(config)

    return config
