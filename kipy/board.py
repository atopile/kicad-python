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

from typing import List, Dict, Union, Iterable, Sequence, cast
from google.protobuf.empty_pb2 import Empty

from kipy.board_types import (
    Arc,
    FootprintInstance,
    Net,
    Pad,
    Text,
    Track,
    Via,
    unwrap
)
from kipy.client import KiCadClient
from kipy.common_types import TextAttributes
from kipy.enums import KICAD_T
from kipy.geometry import Box2
from kipy.util import pack_any, make_item_type
from kipy.wrapper import Wrapper

from kipy.proto.common.types import DocumentSpecifier, KIID
from kipy.proto.common.commands.editor_commands_pb2 import (
    CreateItems, CreateItemsResponse,
    GetItems, GetItemsResponse,
    BoundingBoxResponse
)
from kipy.proto.board import board_pb2
from kipy.proto.board import board_commands_pb2

# Re-exported protobuf enum types
from kipy.proto.board.board_pb2 import (    # noqa
    BoardLayerClass 
)

class BoardLayerGraphicsDefaults(Wrapper):
    """Wraps a kiapi.board.types.BoardLayerGraphicsDefaults object"""
    def __init__(self, proto: board_pb2.BoardLayerGraphicsDefaults = board_pb2.BoardLayerGraphicsDefaults()):
        self._proto = proto

    @property
    def text(self) -> TextAttributes:
        return TextAttributes(self._proto.text)
        
class Board:
    def __init__(self, kicad: KiCadClient, document: DocumentSpecifier):
        self._kicad = kicad
        self._doc = document

    @property
    def document(self) -> DocumentSpecifier:
        return self._doc

    @property
    def name(self) -> str:
        """Returns the file name of the board"""
        return self._doc.board_filename
    
    def save(self):
        pass

    def save_as(self, filename: str):
        pass
    
    def create_items(self, items: Union[Wrapper, Iterable[Wrapper]]) -> List[Wrapper]:
        command = CreateItems()
        command.header.document.CopyFrom(self._doc)

        if isinstance(items, Wrapper):
            command.items.append(pack_any(items.proto))
        else:
            command.items.extend([pack_any(i.proto) for i in items])

        return [
            unwrap(result.item)
            for result in self._kicad.send(command, CreateItemsResponse).created_items
        ]

    def get_items(self, type_filter: Union[KICAD_T, List[KICAD_T]]) -> Sequence[Wrapper]:
        """Retrieves items from the board, optionally filtering to a single or set of types"""
        command = GetItems()
        command.header.document.CopyFrom(self._doc)

        if isinstance(type_filter, KICAD_T):
            command.types.add(type=type_filter)
        else:
            command.types.extend([make_item_type(t) for t in type_filter])

        return [unwrap(item) for item in self._kicad.send(command, GetItemsResponse).items]

    def get_tracks(self) -> Sequence[Union[Track, Arc]]:
        return [
            cast(Track, item) if isinstance(item, Track) else cast(Arc, item)
            for item in self.get_items(
                type_filter=[KICAD_T.PCB_TRACE_T, KICAD_T.PCB_ARC_T]
            )
        ]

    def get_vias(self) -> Sequence[Via]:
        return [cast(Via, item) for item in self.get_items(type_filter=[KICAD_T.PCB_VIA_T])]
    
    def get_pads(self) -> Sequence[Pad]:
        return [cast(Pad, item) for item in self.get_items(type_filter=[KICAD_T.PCB_PAD_T])]
    
    def get_footprints(self) -> Sequence[FootprintInstance]:
        return [
            cast(FootprintInstance, item)
            for item in self.get_items(type_filter=[KICAD_T.PCB_FOOTPRINT_T])
        ]
    
    def update_items(self):
        pass

    def remove_items(self, items: Union[Wrapper, Sequence[Wrapper]]):
        pass

    def get_nets(self, netclass_filter: Union[str, Sequence[str], None]) -> Sequence[Net]:
        return []

    def get_selection(self) -> Sequence[Wrapper]:
        return []

    def add_to_selection(self, items):
        pass

    def remove_from_selection(self, items):
        pass

    def clear_selection(self):
        pass

    def get_stackup(self) -> board_pb2.BoardStackup:
        command = board_commands_pb2.GetBoardStackup()
        command.board.CopyFrom(self._doc)
        return self._kicad.send(command, board_commands_pb2.BoardStackupResponse).stackup
    
    def get_graphics_defaults(self) -> Dict[int, BoardLayerGraphicsDefaults]:
        cmd = board_commands_pb2.GetGraphicsDefaults()
        cmd.board.CopyFrom(self._doc)
        reply = self._kicad.send(cmd, board_commands_pb2.GraphicsDefaultsResponse)
        return {
            board_pb2.BoardLayerClass.BLC_SILKSCREEN:  BoardLayerGraphicsDefaults(reply.defaults.layers[0]),
            board_pb2.BoardLayerClass.BLC_COPPER:      BoardLayerGraphicsDefaults(reply.defaults.layers[1]),
            board_pb2.BoardLayerClass.BLC_EDGES:       BoardLayerGraphicsDefaults(reply.defaults.layers[2]),
            board_pb2.BoardLayerClass.BLC_COURTYARD:   BoardLayerGraphicsDefaults(reply.defaults.layers[3]),
            board_pb2.BoardLayerClass.BLC_FABRICATION: BoardLayerGraphicsDefaults(reply.defaults.layers[4]),
            board_pb2.BoardLayerClass.BLC_OTHER:       BoardLayerGraphicsDefaults(reply.defaults.layers[5])
        }
    
    def get_text_extents(self, text: Text) -> Box2:
        cmd = board_commands_pb2.GetTextExtents()
        cmd.text.CopyFrom(text.proto)
        reply = self._kicad.send(cmd, BoundingBoxResponse)
        return Box2(reply.position, reply.size)
    
    def interactive_move(self, items: Union[KIID, Iterable[KIID]]):
        cmd = board_commands_pb2.InteractiveMoveItems()
        cmd.board.CopyFrom(self._doc)

        if isinstance(items, KIID):
            cmd.items.append(items)
        else:
            cmd.items.extend(items)

        self._kicad.send(cmd, Empty)

    def refill_zones(self):
        pass
