import json
import os

home_folder = os.environ.get("HOME")
xdg_config = os.environ.get("XDG_CONFIG_HOME")

CLEAR_DEVICE_DESC_STR = "__CLEAR_DEVICE_DESC_STR__"

# Define the path where the configuration data will be stored
CONFIG_PATH = f"{xdg_config}/simple-wireplumber-gui/config.json"
WIREPLUMBER_CONFIG_FOLDER = f"{home_folder}/.config/wireplumber"

WIREPLUMBER_RENAME_DEVICE_CONF_PATH = (
    f"{WIREPLUMBER_CONFIG_FOLDER}/wireplumber.conf.d/52-SWG-rename-devices.conf"
)

CONFIGURATION_PATHS = (
    CONFIG_PATH,
    WIREPLUMBER_RENAME_DEVICE_CONF_PATH,
)


rule_template = """  {{
    matches = [
      {{
        device.name = "{device_name}"
      }}
    ]
    actions = {{
      update-props = {{
{properties}      }}
    }}
  }},"""

property_template = '        {key} = "{value}"\n'


def sanitize(i: str):
    return i.replace('"', "")


def _apply_new_device_description(data: dict | None):
    if data is None:
        return

    os.makedirs(os.path.dirname(WIREPLUMBER_RENAME_DEVICE_CONF_PATH), exist_ok=True)

    alsa_rules = []
    bluez_rules = []

    for name, item_data in data.items():
        properties_data = item_data.get("properties_data")
        monitor = item_data.get("monitor")

        if properties_data.get(CLEAR_DEVICE_DESC_STR, None) is not None:
            continue

        properties = ""
        for key, value in properties_data.items():
            properties += property_template.format(key=key, value=value)

        rule = rule_template.format(device_name=name, properties=properties)

        if monitor == "bluez":
            bluez_rules.append(rule)
        else:
            alsa_rules.append(rule)

    conf_lines = []

    if alsa_rules:
        conf_lines.append("monitor.alsa.rules = [\n" + "\n".join(alsa_rules) + "\n]\n")

    if bluez_rules:
        conf_lines.append("monitor.bluez.rules = [\n" + "\n".join(bluez_rules) + "\n]")

    with open(WIREPLUMBER_RENAME_DEVICE_CONF_PATH, "w") as f:
        f.write("\n".join(conf_lines))


def _save_config(data):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    _apply_new_device_description(data.get("devices_new_description", None))
    with open(CONFIG_PATH, "w") as config_file:
        json.dump(data, config_file)


def load_config():
    try:
        with open(CONFIG_PATH, "r") as config_file:
            config_data = json.load(config_file)
        return config_data
    except FileNotFoundError:
        print(f"Config file '{CONFIG_PATH}' not found. Returning an empty dictionary.")
        return {}


def add_device_device_new_description(device, new_description: str | None):
    current_config = load_config()
    current_new_descriptions = current_config.get("devices_new_description", {})

    _new_description = (
        new_description if new_description is not None else CLEAR_DEVICE_DESC_STR
    )

    new_properties = {
        "device.description": sanitize(_new_description),
        "device.nick": sanitize(_new_description),
    }

    if new_description is None:
        new_properties[CLEAR_DEVICE_DESC_STR] = device.description

    current_new_descriptions[device.name] = {
        "properties_data": new_properties,
        "monitor": device.monitor,
    }

    current_config["devices_new_description"] = current_new_descriptions

    _save_config(current_config)


def safe_delete_files(file_paths):
    for path in file_paths:
        print(f"\nDeleting '{path}'")
        try:
            if os.path.isfile(path):
                os.remove(path)
            else:
                print(f"Skipping {path}: Not a file")
        except Exception as e:
            print(f"Error deleting {path}: {str(e)}")


def delete_all_config_files():
    return safe_delete_files(CONFIGURATION_PATHS)
