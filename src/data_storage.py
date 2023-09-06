import json
import os

current_user = os.popen("echo $USER").read().strip()

CLEAR_DEVICE_DESC_STR = "__CLEAR_DEVICE_DESC_STR__"

# Define the path where the configuration data will be stored
CONFIG_PATH = f"/home/{current_user}/.config/simple-wireplumber-gui/config.json"
WIREPLUMBER_CONFIG_FOLDER = f"/home/{current_user}/.config/wireplumber"
WIREPLUMBER_DEVICE_DESCRIPTION_CONFIG_PATH = (
    f"{WIREPLUMBER_CONFIG_FOLDER}/main.lua.d/52-SWG-rename-devices.lua"
)

change_device_template = """
rule = {{
  matches = {{
    {{
      {{ "device.name", "equals", "{device_name}" }},
    }},
  }},
  apply_properties = {{
{properties}
  }},
}}

table.insert(alsa_monitor.rules,rule)

"""

property_template = '      ["{key}"] = "{value}",\n'


def sanitize(i: str):
    return i.replace('"', "")


def _apply_new_device_description(data: dict | None):
    if data is None:
        return

    os.makedirs(
        os.path.dirname(WIREPLUMBER_DEVICE_DESCRIPTION_CONFIG_PATH), exist_ok=True
    )

    script_text = ""

    for name, properties_data in data.items():
        properties = ""
        if not properties_data.get(CLEAR_DEVICE_DESC_STR, None) is None:
            continue

        for key, value in properties_data.items():
            properties += property_template.format(key=key, value=value)

        script_text += change_device_template.format(
            device_name=name, properties=properties
        )

    with open(WIREPLUMBER_DEVICE_DESCRIPTION_CONFIG_PATH, "w") as f:
        f.write(script_text)


def _save_config(data):
    """
    Save a dictionary as a JSON configuration file.

    Args:
        data (dict): The dictionary to be saved as a configuration.
    """
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    _apply_new_device_description(data.get("devices_new_description", None))
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


def add_device_device_new_description(device_name: str, new_description: str | None):
    current_config = load_config()
    current_new_descriptions = current_config.get("devices_new_description", {})

    _new_description = (
        new_description if not new_description is None else CLEAR_DEVICE_DESC_STR
    )

    new_properties = {
        "device.description": sanitize(_new_description),
        "device.nick": sanitize(_new_description),
    }

    if new_description is None:
        new_properties[CLEAR_DEVICE_DESC_STR] = CLEAR_DEVICE_DESC_STR

    current_new_descriptions[device_name] = new_properties

    current_config["devices_new_description"] = current_new_descriptions

    _save_config(current_config)
