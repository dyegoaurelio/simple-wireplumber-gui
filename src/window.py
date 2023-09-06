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

from .parse_pipewire_data import (
    physical_devices_unchanged,
    physical_devices_waiting_reboot,
    physical_devices_successfully_changed,
    update_physical_devices_lists,
)

from .data_storage import add_device_device_new_description


@Gtk.Template(resource_path="/org/gnome/Example/gtk/edit-device-modal.ui")
class EditDeviceModal(Adw.Window):
    __gtype_name__ = "EditDeviceModal"
    device_name: Gtk.Label = Gtk.Template.Child()
    send_btn: Gtk.Button = Gtk.Template.Child()
    clear_btn: Gtk.Button = Gtk.Template.Child()
    new_description: Adw.EntryRow = Gtk.Template.Child()

    def __init__(self, device: Device, **kwargs):
        super().__init__(**kwargs)

        self.device_name.set_label(device.name)
        self.send_btn.connect("clicked", self.save_data)
        self.clear_btn.connect("clicked", self.save_data, True)
        if not device.assigned_description is None:
            self.new_description.set_text(device.assigned_description)
        else:
            self.new_description.set_text(device.description)

    def save_data(self, widget, none_desc=False):
        if not none_desc:
            new_desc = self.new_description.get_text()
            if len(new_desc) == 0:
                return
        else:
            new_desc = None

        add_device_device_new_description(self.device_name.get_label(), new_desc)
        self.destroy()
        self.activate_action("app.refresh_app")


class InputRow(Adw.ActionRow):
    __gtype_name__ = "WirepluberInputRow"
    device: Device

    def __init__(self, device: Device, **kwargs):
        self.device = device
        super().__init__(
            title=device.assigned_description or device.description, **kwargs
        )

        edit_btn = Gtk.Button(
            icon_name="document-edit", tooltip_text="Rename this device"
        )
        edit_btn.connect("clicked", lambda _: self.show_edit_modal())
        self.add_suffix(edit_btn)
        # self.add_suffix(
        #     Gtk.ToggleButton(
        #         icon_name="edit-delete",
        #         tooltip_text="Hide this device",
        #         active=device.hidden,
        #     )
        # )

    def show_edit_modal(self):
        _modal = EditDeviceModal(self.device)
        _modal.set_application(Gtk.Application.get_default())
        _modal.present()


@Gtk.Template(resource_path="/org/gnome/Example/window.ui")
class SimpleWireplumberGuiWindow(Adw.PreferencesWindow):
    __gtype_name__ = "SimpleWireplumberGuiWindow"

    input_active = Gtk.Template.Child()
    input_disabled = Gtk.Template.Child()

    output_active = Gtk.Template.Child()
    output_disabled = Gtk.Template.Child()

    physical_unchanged: Adw.PreferencesGroup = Gtk.Template.Child()
    physical_waiting_reboot: Adw.PreferencesGroup = Gtk.Template.Child()
    physical_successfully_changed: Adw.PreferencesGroup = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_input_devices()
        self.add_output_devices()
        self.add_physical_devices()

    def add_physical_devices(self):
        update_physical_devices_lists()

        def add_list(_group: Adw.PreferencesGroup, _list: list):
            if len(_list) == 0:
                _group.hide()
            else:
                _group.show()
                for d in _list:
                    row = InputRow(d)
                    _group.add(row)

        add_list(self.physical_unchanged, physical_devices_unchanged)
        add_list(self.physical_waiting_reboot, physical_devices_waiting_reboot)
        add_list(
            self.physical_successfully_changed, physical_devices_successfully_changed
        )

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
