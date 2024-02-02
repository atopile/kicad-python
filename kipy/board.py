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

from typing import List
from google.protobuf.message import Message
from result import Ok, Err

from kipy.client import KiCadClient, ApiError
from kipy.proto.common.types import DocumentSpecifier
from kipy.proto.common.commands.editor_commands_pb2 import *
from kipy.proto.board.board_pb2 import BoardStackup, BoardStackupLayer
from kipy.proto.board.board_commands_pb2 import GetBoardStackup, BoardStackupResponse
from kipy.util import pack_any

class Board:
    def __init__(self, kicad: KiCadClient, document: DocumentSpecifier):
        self._kicad = kicad
        self._doc = document

    def get_name(self) -> str:
        """Returns the file name of the board"""
        return self._doc.board_filename
    
    def create_items(self, items: List[Message]) -> List[Message]:
        if type(items) is not List:
            items = [items]
        command = CreateItems()
        command.items.extend([pack_any(i) for i in items])
        command.header.document.CopyFrom(self._doc)
        match self._kicad.send(command, CreateItemsResponse):
            case Ok(response):
                return response.created_items
            case Err(e):
                raise ApiError(e)
            
    def get_stackup(self) -> BoardStackup:
        command = GetBoardStackup()
        command.board.CopyFrom(self._doc)
        match self._kicad.send(command, BoardStackupResponse):
            case Ok(response):
                return response.stackup
            case Err(e):
                raise ApiError(e)