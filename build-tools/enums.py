# This program source code file is part of KiCad, a free EDA CAD application.
#
# Copyright (C) 2024 KiCad Developers
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
from jinja2 import Template
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", default="kicad-build/api/enums.json")
    parser.add_argument("--output", default="kipy/enums/_enums.py")
    parser.add_argument("--template", default="build-tools/enums_template.py")

    args = parser.parse_args()

    with open(args.input, 'r') as f:
        enums = json.load(f)

    with open(args.template) as f:
        template = Template(f.read())

    with open(args.output, 'w') as f:
        f.write(template.render(enums=enums))
