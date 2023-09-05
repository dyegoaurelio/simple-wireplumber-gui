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
from .pipewire import active_input_devices

@Gtk.Template(resource_path="/org/gnome/Example/window.ui")
class SimpleWireplumberGuiWindow(Adw.PreferencesWindow):
    __gtype_name__ = "SimpleWireplumberGuiWindow"

    input_active = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_input_devices()

    def add_input_devices(self):
        for d in active_input_devices:
            row = Adw.ActionRow(title=d.name)
            self.input_active.add(row)
