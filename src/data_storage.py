import json
import os

current_user = os.popen("echo $USER").read().strip()

# Define the path where the configuration data will be stored
CONFIG_PATH = f"/home/{current_user}/config/simple-wireplumber-gui/config.json"


def _save_config(data):
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


def add_device_device_new_description(device_name: str, new_description: str):
    current_config = load_config()
    current_new_descriptions = current_config.get("devices_new_description", {})

    current_new_descriptions[device_name] = {"device.description": new_description}

    current_config["devices_new_description"] = current_new_descriptions

    _save_config(current_config)
