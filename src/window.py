# window.py
#
# Copyright 2023 dyego
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk
from .pipewire import (
    active_input_devices,
    disabled_input_devices,
    Device,
    active_output_devices,
    disabled_output_devices,
)


@Gtk.Template(resource_path="/org/gnome/Example/gtk/edit-device-modal.ui")
class EditDeviceModal(Adw.Window):
    __gtype_name__ = "EditDeviceModal"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class InputRow(Adw.ActionRow):
    __gtype_name__ = "WirepluberInputRow"
    _edit_device_modal: EditDeviceModal

    def __init__(self, device: Device, **kwargs):
        super().__init__(title=device.name, **kwargs)

        edit_btn = Gtk.Button(
            icon_name="document-edit", tooltip_text="Rename this device"
        )
        edit_btn.connect("clicked", lambda _: self.show_edit_modal())
        self.add_suffix(edit_btn)
        self.add_suffix(
            Gtk.ToggleButton(
                icon_name="edit-delete",
                tooltip_text="Hide this device",
                active=device.hidden,
            )
        )

    def show_edit_modal(self):
        try:
            self._edit_device_modal
        except AttributeError:
            self._edit_device_modal = EditDeviceModal()
        
        self._edit_device_modal.present()


@Gtk.Template(resource_path="/org/gnome/Example/window.ui")
class SimpleWireplumberGuiWindow(Adw.PreferencesWindow):
    __gtype_name__ = "SimpleWireplumberGuiWindow"

    input_active = Gtk.Template.Child()
    input_disabled = Gtk.Template.Child()

    output_active = Gtk.Template.Child()
    output_disabled = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_input_devices()
        self.add_output_devices()

    def add_input_devices(self):
        for d in active_input_devices:
            row = InputRow(d)
            self.input_active.add(row)

        for d in disabled_input_devices:
            row = InputRow(d)
            self.input_disabled.add(row)

    def add_output_devices(self):
        for d in active_output_devices:
            row = InputRow(d)
            self.output_active.add(row)

        for d in disabled_output_devices:
            row = InputRow(d)
            self.output_disabled.add(row)
