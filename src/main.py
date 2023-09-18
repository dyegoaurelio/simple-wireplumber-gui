# main.py
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

import sys
import argparse


def run_app():
    """The application's entry point."""
    from .app import SimpleWireplumberGuiApplication

    app = SimpleWireplumberGuiApplication()
    return app.run(sys.argv)


def clear_settings():
    print("clearing settings")


def main(version):
    parser = argparse.ArgumentParser(description="Simple Wireplumber GUI")

    parser.add_argument("--clear-settings", action="store_true", help="Clear settings")

    args = parser.parse_args(sys.argv[1:])

    if args.clear_settings:
        return clear_settings()
    else:
        return run_app()
