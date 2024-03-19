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

import os
import subprocess

from tools.generate_enums import generate_enums
from tools.generate_protos import generate_protos


if __name__ == "__main__":
    print("Ensuring KiCad git repository is ready...")
    subprocess.run(["git", "submodule", "update", "--init"])

    print("Building KiCad enum extraction tool...")

    try:
        os.mkdir("kicad-build")
    except FileExistsError:
        pass
    
    kicad_workdir = os.path.join(os.getcwd(), "kicad-build")
    try:
        subprocess.run(["cmake", "-G", "Ninja",
                        "-DKICAD_IPC_API=ON",
                        "-DKICAD_BUILD_ENUM_EXPORTER=ON",
                        "../kicad"],
                        cwd=kicad_workdir)
        subprocess.run(["ninja", "enum_definitions"], cwd=kicad_workdir)
    except (ChildProcessError, FileNotFoundError):
        print("Warning: could not generate KiCad enum definitions")

    if os.path.exists("kicad-build/api/enums.json"):
        print("Generating Python enum classes...")
        generate_enums("kicad-build/api/enums.json",
                    "kipy/enums/_enums.py",
                    "tools/enums_template.py")
    else:
        print("Warning: enum definitons file is missing")
    
    print("Generating protobuf wrappers...")
    proto_in = os.path.join(os.getcwd(), "kicad/api/proto")
    proto_out = os.path.join(os.getcwd(), "kipy/proto")
    generate_protos(proto_in, proto_out)
