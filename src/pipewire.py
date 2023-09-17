import os
import re
import subprocess
from dataclasses import dataclass
from typing import List, Dict, Optional

PATTERN_IDS = r"id (\d+), type ([\w:\/]+)"
PATTERN_DATA = r'(\w+\.\w+)\s*=\s*"([^"]+)"'


@dataclass
class Device:
    id: str
    hidden: bool
    name: str
    description: str
    nick: str
    monitor: str
    raw_data: Dict[str, str]

    assigned_description: Optional[str] = None


def parse_pw_cli_ls_data(data: str) -> Dict[str, Dict[str, str]]:
    parsed_data = {}

    last_match_character = -1
    last_match_id = None

    def append_last_id_data(current_start: int):
        if last_match_character < 0:
            return

        current_data = data[last_match_character:current_start]
        matches = re.findall(PATTERN_DATA, current_data)

        parsed_data[last_match_id].update(dict(matches))

    for match in re.finditer(PATTERN_IDS, data):
        id_, type_ = match.groups()
        parsed_data[id_] = {"type": type_}

        append_last_id_data(match.start())

        last_match_character = match.end()
        last_match_id = id_

    append_last_id_data(len(data))

    return parsed_data


def get_pipewire_objects_data():
    stream = os.popen("pw-cli list-objects")
    return parse_pw_cli_ls_data(stream.read())


def filter_pipewire_objects(value: str, key="media.class"):
    pipewire_objects = get_pipewire_objects_data()

    return filter(
        lambda obj: obj.get(key) == value,
        pipewire_objects.values(),
    )


def get_pipewire_devices_data():
    return filter_pipewire_objects("Audio/Device")


def get_pipewire_output_nodes():
    return filter_pipewire_objects("Audio/Sink")


def get_pipewire_input_nodes():
    return filter_pipewire_objects("Audio/Source")


def get_pipewire_default_devices():
    # Replace 'your_command_here' with the actual system command you want to run.
    result = subprocess.run(
        ["pw-metadata"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True,
    )
    if result.returncode == 0:
        return result.stdout
    else:
        return result.stderr
