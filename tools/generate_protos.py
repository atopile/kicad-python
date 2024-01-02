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
import fnmatch
import os
import platform
import subprocess


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", default="kicad/api/proto")
    parser.add_argument("--output", default="kipy")
    parser.add_argument("--protoc", help="Path to protoc",
                        default="protoc.exe" if platform.system() == "Windows" else "protoc")
    parser.add_argument("--protol", help="Path to protoletariat",
                        default="protol.exe" if platform.system() == "Windows" else "protol")

    args = parser.parse_args()

    output_path = os.path.abspath(args.output)
    input_path = os.path.abspath(args.input)

    proto_sources = []

    for root, _, files in os.walk(input_path):
        for item in fnmatch.filter(files, "*.proto"):
            proto_sources.append(os.path.join(input_path, str(root), item))

    print("Generating Python classes from protobuf files...")
    subprocess.run([args.protoc,
           "--python_out=" + output_path,
           "--proto_path=" + input_path,
           *proto_sources])

    print("Post-processing with protoletariat...")
    subprocess.run([args.protol,
           "--dont-create-package",
           "--in-place",
           "--exclude-google-imports",
           "--python-out", output_path,
           "protoc",
           "--proto-path", input_path,
           *proto_sources])

