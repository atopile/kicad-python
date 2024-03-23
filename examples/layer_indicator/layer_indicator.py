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

from typing import cast

from kipy import KiCad
from kipy.geometry import Vector2
from kipy.board import BoardLayer, BoardLayerClass
from kipy.board_types import Text, FootprintInstance


if __name__=='__main__':
    kicad = KiCad()
    board = kicad.get_board()
    stackup = board.get_stackup()
    defaults = board.get_graphics_defaults()[BoardLayerClass.BLC_COPPER]

    sizing_text = Text()
    sizing_text.layer = BoardLayer.BL_F_Cu
    sizing_text.position = Vector2.from_xy(0, 0)
    sizing_text.text = "0"
    sizing_text.attributes = defaults.text

    char_width = board.get_text_extents(sizing_text).size.x

    copper_layers = [layer for layer in stackup.layers
                     if layer.layer <= BoardLayer.BL_B_Cu
                     and layer.layer >= BoardLayer.BL_F_Cu]
    
    fpi = FootprintInstance()
    fpi.layer = BoardLayer.BL_F_Cu
    fpi.reference_field.text.text = "STACKUP1"
    fpi.reference_field.text.attributes = defaults.text
    fpi.reference_field.text.attributes.visible = False
    fpi.value_field.text.attributes = defaults.text
    fpi.value_field.text.attributes.visible = False
    fpi.attributes.not_in_schematic = True
    fpi.attributes.exclude_from_bill_of_materials = True
    fpi.attributes.exclude_from_position_files = True
    fp = fpi.definition

    offset = 0
    layer_idx = 1
    for copper_layer in copper_layers:
        layer_text = Text()
        layer_text.layer = copper_layer.layer
        layer_text.text = "%d" % layer_idx
        layer_text.position = Vector2.from_xy(offset, 0)
        layer_text.attributes = defaults.text
        layer_text.attributes.visible = True
        fp.add_item(layer_text)

        padding = 1 if layer_idx == 9 else 0.5
        item_width = int((len(layer_text.text) + padding) * char_width)

        offset += item_width
        layer_idx += 1

    created = [cast(FootprintInstance, i) for i in board.create_items(fpi)]

    if len(created) == 1:
        board.interactive_move(created[0].id)
