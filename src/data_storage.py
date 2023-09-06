import json
import os

# Define the path where the configuration data will be stored
CONFIG_PATH = "~/.config/simple-wireplumber-gui/config.json"

def save_config(data):
    """
    Save a dictionary as a JSON configuration file.
    
    Args:
        data (dict): The dictionary to be saved as a configuration.
    """
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as config_file:
        json.dump(data, config_file)

def load_config():
    """
    Load the configuration data from the JSON file.
    
    Returns:
        dict: The loaded configuration data as a dictionary.
    """
    try:
        with open(CONFIG_PATH, "r") as config_file:
            config_data = json.load(config_file)
        return config_data
    except FileNotFoundError:
        print(f"Config file '{CONFIG_PATH}' not found. Returning an empty dictionary.")
        return {}