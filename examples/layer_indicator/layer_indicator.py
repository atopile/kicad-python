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
from kipy.proto.board.board_commands_pb2 import (
    InteractiveMoveItems
)
from kipy.proto.board.board_pb2 import BoardLayerClass

from google.protobuf.any_pb2 import Any
from google.protobuf.empty_pb2 import Empty


if __name__=='__main__':
    kicad = KiCad()
    board = kicad.get_board()
    stackup = board.get_stackup()
    defaults = board.get_graphics_defaults()[BoardLayerClass.BLC_COPPER]

    sizing_pcb_text = Text()
    sizing_text = sizing_pcb_text.text
    sizing_text.layer.id = PCB_LAYER_ID.F_Cu
    sizing_text.position.x_nm = 0
    sizing_text.position.y_nm = 0
    sizing_text.text = "0"
    sizing_text.attributes.CopyFrom(defaults.text)

    char_width = board.get_text_extents(sizing_pcb_text).size.x

    copper_layers = [layer for layer in stackup.layers
                     if layer.layer.id <= PCB_LAYER_ID.B_Cu
                     and layer.layer.id >= PCB_LAYER_ID.F_Cu]
    
    fpi = FootprintInstance()
    fpi.reference_field.text.text.text = "STACKUP1"
    fpi.reference_field.text.text.attributes.CopyFrom(defaults.text)
    fpi.reference_field.text.text.attributes.visible = False
    fpi.value_field.text.text.attributes.CopyFrom(defaults.text)
    fpi.value_field.text.text.attributes.visible = False
    fpi.attributes.not_in_schematic = True
    fpi.attributes.exclude_from_bill_of_materials = True
    fpi.attributes.exclude_from_position_files = True
    fp = fpi.definition

    offset = 0
    layer_idx = 1
    for copper_layer in copper_layers:
        f = Text()
        innerText = f.text
        innerText.layer.id = copper_layer.layer.id
        innerText.text = "%d" % layer_idx
        innerText.locked = True
        innerText.position.x_nm = offset
        innerText.position.y_nm = 0
        innerText.attributes.CopyFrom(defaults.text)
        innerText.attributes.visible = True
        fmsg = Any()
        fmsg.Pack(f)
        fp.items.append(fmsg)

        padding = 1 if layer_idx == 9 else 0.5
        item_width = int((len(innerText.text) + padding) * char_width)

        offset += item_width
        layer_idx += 1

    created = board.create_items(fpi)

    if len(created) == 1:
        created_fp = FootprintInstance()
        created[0].item.Unpack(created_fp)

        cmd = InteractiveMoveItems()
        cmd.board.CopyFrom(board._doc)
        cmd.items.append(created_fp.id)
        board._kicad.send(cmd, Empty)
