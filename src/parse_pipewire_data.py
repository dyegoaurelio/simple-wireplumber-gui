from typing import Dict, List
from .pipewire import get_pipewire_devices_data, Device
from .data_storage import load_config, CLEAR_DEVICE_DESC_STR

physical_devices_unchanged: List[Device] = []
physical_devices_successfully_changed: List[Device] = []
physical_devices_waiting_reboot: List[Device] = []


def update_physical_devices_lists():
    physical_devices_waiting_reboot.clear()
    physical_devices_successfully_changed.clear()
    physical_devices_unchanged.clear()

    physical_devices = list(
        map(
            lambda d: Device(
                id=d["object.serial"],
                name=d.get("device.name", ""),
                description=d.get("device.description", ""),
                nick=d.get("device.nick", ""),
                monitor=d.get("device.name", "alsa").split("_")[0],
                hidden=False,
                raw_data=d,
            ),
            get_pipewire_devices_data(),
        )
    )

    current_config = load_config()
    devices_new_description: Dict[str, str] = current_config.get(
        "devices_new_description", {}
    )

    for d in physical_devices:
        device_config = devices_new_description.get(d.name, {}).get(
            "properties_data", None
        )
        if device_config is None:
            physical_devices_unchanged.append(d)
        else:
            if device_config.get(CLEAR_DEVICE_DESC_STR, None) is None:
                d.assigned_description = device_config.get("device.description", "")
            else:
                # this means that the device was marked to be cleared
                # and is waiting for a reboot to clear the description
                # or has rebooted and cleared
                d.assigned_description = None
                if device_config.get(CLEAR_DEVICE_DESC_STR, None) != d.description:
                    physical_devices_unchanged.append(d)
                    continue

                d.description = device_config.get(CLEAR_DEVICE_DESC_STR, "")

            if d.assigned_description == d.description:
                physical_devices_successfully_changed.append(d)
            else:
                physical_devices_waiting_reboot.append(d)
