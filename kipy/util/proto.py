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

from google.protobuf.any_pb2 import Any
from google.protobuf.message import Message

from kipy.proto.board import board_types_pb2

def pack_any(object: Message) -> Any:
    a = Any()
    a.Pack(object)
    return a

_any_urls = {
    "type.googleapis.com/kiapi.board.types.Track": board_types_pb2.Track,
    "type.googleapis.com/kiapi.board.types.Arc": board_types_pb2.Arc,
    "type.googleapis.com/kiapi.board.types.Via": board_types_pb2.Via,
    "type.googleapis.com/kiapi.board.types.Text": board_types_pb2.Text,
    "type.googleapis.com/kiapi.board.types.TextBox": board_types_pb2.TextBox,
    "type.googleapis.com/kiapi.board.types.GraphicShape": board_types_pb2.GraphicShape,
    "type.googleapis.com/kiapi.board.types.Pad": board_types_pb2.Pad,
    "type.googleapis.com/kiapi.board.types.Zone": board_types_pb2.Zone,
    "type.googleapis.com/kiapi.board.types.Dimension": board_types_pb2.Dimension,
    "type.googleapis.com/kiapi.board.types.ReferenceImage": board_types_pb2.ReferenceImage,
    "type.googleapis.com/kiapi.board.types.Group": board_types_pb2.Group,
    "type.googleapis.com/kiapi.board.types.Field": board_types_pb2.Field,
    "type.googleapis.com/kiapi.board.types.FootprintInstance": board_types_pb2.FootprintInstance,
    "type.googleapis.com/kiapi.board.types.Footprint3DModel": board_types_pb2.Footprint3DModel
}

def unpack_any(object: Any) -> Message:
    if len(object.type_url) == 0:
        raise ValueError("Can't unpack empty Any protobuf message")

    type = _any_urls.get(object.type_url, None)
    if type is None:
        raise NotImplementedError(f"{object.type_url} can't be unpacked")

    concrete = type()
    object.Unpack(concrete)
    return concrete
