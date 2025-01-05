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

from kipy.proto.board.board_types_pb2 import BoardLayer

def is_copper_layer(layer: BoardLayer.ValueType) -> bool:
    """Checks if the given layer is a copper layer"""
    return layer in {
        BoardLayer.BL_F_Cu,
        BoardLayer.BL_B_Cu,
        BoardLayer.BL_In1_Cu,
        BoardLayer.BL_In2_Cu,
        BoardLayer.BL_In3_Cu,
        BoardLayer.BL_In4_Cu,
        BoardLayer.BL_In5_Cu,
        BoardLayer.BL_In6_Cu,
        BoardLayer.BL_In7_Cu,
        BoardLayer.BL_In8_Cu,
        BoardLayer.BL_In9_Cu,
        BoardLayer.BL_In10_Cu,
        BoardLayer.BL_In11_Cu,
        BoardLayer.BL_In12_Cu,
        BoardLayer.BL_In13_Cu,
        BoardLayer.BL_In14_Cu,
        BoardLayer.BL_In15_Cu,
        BoardLayer.BL_In16_Cu,
        BoardLayer.BL_In17_Cu,
        BoardLayer.BL_In18_Cu,
        BoardLayer.BL_In19_Cu,
        BoardLayer.BL_In20_Cu,
        BoardLayer.BL_In21_Cu,
        BoardLayer.BL_In22_Cu,
        BoardLayer.BL_In23_Cu,
        BoardLayer.BL_In24_Cu,
        BoardLayer.BL_In25_Cu,
        BoardLayer.BL_In26_Cu,
        BoardLayer.BL_In27_Cu,
        BoardLayer.BL_In28_Cu,
        BoardLayer.BL_In29_Cu,
        BoardLayer.BL_In30_Cu
    }
