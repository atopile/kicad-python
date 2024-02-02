#!/usr/bin/env python3

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

from kipy import KiCad
from kipy.enums import PCB_LAYER_ID
from kipy.proto.board.board_types_pb2 import FootprintInstance, Text
from kipy.util import from_mm
from google.protobuf.any_pb2 import Any


if __name__=='__main__':
    kicad = KiCad()
    board = kicad.get_board()
    stackup = board.get_stackup()   

    copper_layers = [layer for layer in stackup.layers
                     if layer.layer.layer_id <= PCB_LAYER_ID.B_Cu
                     and layer.layer.layer_id >= PCB_LAYER_ID.F_Cu]
    
    fpi = FootprintInstance()
    fp = fpi.definition

    offset = 0
    layer_idx = 1
    for copper_layer in copper_layers:
        f = Text()
        f.layer.layer_id = copper_layer.layer.layer_id
        f.text = "%d" % layer_idx
        f.position.x_nm = offset
        f.position.y_nm = 0
        fmsg = Any()
        fmsg.Pack(f)
        fp.items.append(fmsg)
        offset += from_mm(1.5)
        layer_idx += 1

    board.create_items(fpi)