
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
from kipy.board_types import (
    BoardLayer,
    Zone
)
from kipy.common_types import PolygonWithHoles
from kipy.geometry import PolyLine, PolyLineNode
from kipy.util import from_mm

if __name__=='__main__':
    kicad = KiCad()
    board = kicad.get_board()

    outline = PolyLine()
    outline.append(PolyLineNode.from_xy(from_mm(100), from_mm(100)))
    outline.append(PolyLineNode.from_xy(from_mm(110), from_mm(100)))
    outline.append(PolyLineNode.from_xy(from_mm(110), from_mm(110)))
    outline.append(PolyLineNode.from_xy(from_mm(100), from_mm(110)))
    outline.append(PolyLineNode.from_xy(from_mm(100), from_mm(100)))
    polygon = PolygonWithHoles()
    polygon.outline = outline
    zone = Zone()
    zone.layers = [BoardLayer.BL_F_Cu, BoardLayer.BL_B_Cu]
    zone.outline = polygon
    board.create_items(zone)
