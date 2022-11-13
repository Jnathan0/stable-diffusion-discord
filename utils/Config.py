import os
import json


CONFIG_DICT = {
    "BOT_TOKEN": "",
    "BACKEND_URL": "",
    "COLLAGE_FORMAT": "PNG",
    "IMAGE_SELECT_TIMEOUT": 10800,
    "CUSTOM_HEADERS": []
}


def get_config(path: str) -> dict:
    """
    get_config()
    Parameters: 
        - path: full filepath to a .json file that contains config keys and values
    Returns:
        - json.load object of config file 
        or
        - dictionary 

    Function tries to load a .json file for app config, if no file exists it then tries to use system environment variables and returns dictionary of keys,values for settings. 
    """
    try:
        if path is None:
            raise FileNotFoundError
        with open(path, 'r') as file:
            config = json.load(file)
        return config
    # If a .json file doesn't exist for settings, use sytem environment variables
    except FileNotFoundError:
        print(f"Warning no config file found at: {path}, attempting to use environment variables.")
        config = {}
        # Iterate through keys in CONFIG_DICT and set using os.getenv
        # Defaults are provided from CONFIG_DICT
        for setting in CONFIG_DICT.keys():
            if setting == 'CUSTOM_HEADERS':
                config[setting] = json.loads(os.getenv(setting.upper()))
            else:
                config[setting] = os.getenv(setting.upper(), default = CONFIG_DICT[setting])
            print(f"{setting}: {config[setting]}")
        return config