from dataclasses import dataclass
from typing import List

@dataclass
class Device:
    id : str
    hidden: bool
    name: str

input_devices: List[Device] = [
    Device('dev-1', False, 'Device 1'),
    Device('dev-2', False, 'Device 2'),
    Device('dev-3', True, 'Device 3'),
    Device('dev-4', False, 'Device 4'),
    Device('dev-5', True, 'Device 5'),
]

active_input_devices = filter(lambda d : not d.hidden, input_devices )
disabled_input_devices = filter(lambda d : d.hidden, input_devices )