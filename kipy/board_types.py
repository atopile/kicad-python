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

from typing import Dict, Sequence, Set, Optional, cast
from google.protobuf.message import Message
from google.protobuf.any_pb2 import Any

from kipy.proto.common.types import KIID
from kipy.proto.common.types.base_types_pb2 import LockedState
from kipy.proto.board import board_types_pb2
from kipy.common_types import TextAttributes
from kipy.geometry import Vector2
from kipy.util import unpack_any
from kipy.wrapper import Item, Wrapper

# Re-exported protobuf enum types
from kipy.proto.board.board_types_pb2 import ( #noqa
    PadType,
    BoardLayer
)

class BoardItem(Item):
    @property
    def id(self):
        return self.proto.id

class Net(Wrapper):
    def __init__(self, proto: Optional[board_types_pb2.Net] = None):
        self._proto = board_types_pb2.Net()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def name(self) -> str:
        return self._proto.name

    @property
    def code(self) -> int:
        return self._proto.code.value
    
    def __eq__(self, other):
        if isinstance(other, Net):
            return self.code == other.code and self.name == other.name
        return NotImplemented

class Track(BoardItem):
    """Represents a straight track segment"""
    def __init__(self, proto: Optional[board_types_pb2.Track] = None):
        self._proto = board_types_pb2.Track()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def net(self) -> Net:
        return Net(self._proto.net)
    
    @net.setter
    def net(self, net: Net):
        self._proto.net.CopyFrom(net.proto)
    
    @property
    def layer(self) -> board_types_pb2.BoardLayer.ValueType:
        return self._proto.layer
    
    @layer.setter
    def layer(self, layer: board_types_pb2.BoardLayer.ValueType):
        self._proto.layer = layer

    @property
    def start(self) -> Vector2:
        return Vector2(self._proto.start)
    
    @start.setter
    def start(self, point: Vector2):
        self._proto.start.CopyFrom(point.proto)

    @property
    def end(self) -> Vector2:
        return Vector2(self._proto.end)
    
    @end.setter
    def end(self, point: Vector2):
        self._proto.end.CopyFrom(point.proto)

    @property
    def width(self) -> int:
        return self._proto.width.value_nm
    
    @width.setter
    def width(self, width: int):
        self._proto.width.value_nm = width

    def length(self) -> float:
        """Calculates track length in nanometers"""
        return (self.end - self.start).length()

class Arc(BoardItem):
    """Represents an arc track segment"""
    def __init__(self, proto: Optional[board_types_pb2.Arc] = None):
        self._proto = board_types_pb2.Arc()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def net(self) -> Net:
        return Net(self._proto.net)
    
    @net.setter
    def net(self, net: Net):
        self._proto.net.CopyFrom(net.proto)
    
    @property
    def layer(self) -> board_types_pb2.BoardLayer.ValueType:
        return self._proto.layer
    
    @layer.setter
    def layer(self, layer: board_types_pb2.BoardLayer.ValueType):
        self._proto.layer = layer

    @property
    def start(self) -> Vector2:
        return Vector2(self._proto.start)
    
    @start.setter
    def start(self, point: Vector2):
        self._proto.start.CopyFrom(point.proto)

    @property
    def end(self) -> Vector2:
        return Vector2(self._proto.end)
    
    @end.setter
    def end(self, point: Vector2):
        self._proto.end.CopyFrom(point.proto)

    @property
    def width(self) -> int:
        return self._proto.width.value_nm
    
    @width.setter
    def width(self, width: int):
        self._proto.width.value_nm = width

    @property
    def mid(self) -> Vector2:
        return Vector2(self._proto.mid)
    
    @mid.setter
    def mid(self, point: Vector2):
        self._proto.mid.CopyFrom(point.proto)

class Via(BoardItem):
    def __init__(self, proto: Optional[board_types_pb2.Via] = None):
        self._proto = board_types_pb2.Via()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def position(self) -> Vector2:
        return Vector2(self._proto.position)
    
    @position.setter
    def position(self, position: Vector2):
        self._proto.position.CopyFrom(position.proto)

    @property
    def net(self) -> Net:
        return Net(self._proto.net)
    
    @net.setter
    def net(self, net: Net):
        self._proto.net.CopyFrom(net.proto)

    def layer_set(self) -> Set[board_types_pb2.BoardLayer.ValueType]:
        s = set()
        layer = self._proto.pad_stack.start_layer
        while layer <= self._proto.pad_stack.end_layer:
            s.add(layer)
            layer = cast(board_types_pb2.BoardLayer.ValueType, layer + 1)
        return s

class Pad(BoardItem):
    def __init__(self, proto: Optional[board_types_pb2.Pad] = None):
        self._proto = board_types_pb2.Pad()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def position(self) -> Vector2:
        return Vector2(self._proto.position)
    
    @position.setter
    def position(self, position: Vector2):
        self._proto.position.CopyFrom(position.proto)

    @property
    def net(self) -> Net:
        return Net(self._proto.net)
    
    @net.setter
    def net(self, net: Net):
        self._proto.net.CopyFrom(net.proto)

    @property
    def pad_type(self) -> PadType.ValueType:
        return self._proto.type

    def layer_set(self) -> Set[board_types_pb2.BoardLayer.ValueType]:
        s = set()
        layer = self._proto.pad_stack.start_layer
        while layer <= self._proto.pad_stack.end_layer:
            s.add(layer)
            layer = cast(board_types_pb2.BoardLayer.ValueType, layer + 1)
        return s

class Text(BoardItem):
    """Represents a free text object, or the text component of a field"""
    def __init__(self, proto: Optional[board_types_pb2.Text] = None,
                 proto_ref: Optional[board_types_pb2.Text] = None):
        self._proto = proto_ref if proto_ref is not None else board_types_pb2.Text()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def id(self) -> KIID:
        return self._proto.text.id
    
    @property
    def position(self) -> Vector2:
        return Vector2(self._proto.text.position)
    
    @position.setter
    def position(self, pos: Vector2):
        self._proto.text.position.CopyFrom(pos.proto)

    @property
    def layer(self) -> board_types_pb2.BoardLayer.ValueType:
        return self._proto.layer
    
    @layer.setter
    def layer(self, layer: board_types_pb2.BoardLayer.ValueType):
        self._proto.layer = layer

    @property
    def locked(self) -> bool:
        return self._proto.text.locked == LockedState.LS_LOCKED
    
    @locked.setter
    def locked(self, locked: bool):
        self._proto.text.locked = {
            True: LockedState.LS_LOCKED,
            False: LockedState.LS_UNLOCKED,
        }.get(locked, LockedState.LS_UNLOCKED)

    @property
    def text(self) -> str:
        return self._proto.text.text
    
    @text.setter
    def text(self, text: str):
        self._proto.text.text = text

    @property
    def attributes(self) -> TextAttributes:
        return TextAttributes(proto_ref=self._proto.text.attributes)
    
    @attributes.setter
    def attributes(self, attributes: TextAttributes):
        self._proto.text.attributes.CopyFrom(attributes.proto)


class Field(BoardItem):
    """Represents a footprint field"""
    def __init__(self, proto: Optional[board_types_pb2.Field] = None,
                 proto_ref: Optional[board_types_pb2.Field] = None):
        self._proto = proto_ref if proto_ref is not None else board_types_pb2.Field()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def field_id(self) -> int:
        return self._proto.id.id
    
    @property
    def name(self) -> str:
        return self._proto.name
    
    @property
    def text(self) -> Text:
        return Text(proto_ref=self._proto.text)
    
    @text.setter
    def text(self, text: Text):
        self._proto.text.CopyFrom(text.proto)


class FootprintAttributes(Wrapper):
    """The built-in attributes that a Footprint or FootprintInstance may have"""
    def __init__(self, proto: Optional[board_types_pb2.FootprintAttributes] = None,
                 proto_ref: Optional[board_types_pb2.FootprintAttributes] = None):
        self._proto = proto_ref if proto_ref is not None else board_types_pb2.FootprintAttributes()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def not_in_schematic(self) -> bool:
        return self._proto.not_in_schematic
    
    @not_in_schematic.setter
    def not_in_schematic(self, not_in_schematic: bool):
        self._proto.not_in_schematic = not_in_schematic

    @property
    def exclude_from_bill_of_materials(self) -> bool:
        return self._proto.exclude_from_bill_of_materials
    
    @exclude_from_bill_of_materials.setter
    def exclude_from_bill_of_materials(self, exclude: bool):
        self._proto.exclude_from_bill_of_materials = exclude

    @property
    def exclude_from_position_files(self) -> bool:
        return self._proto.exclude_from_position_files
    
    @exclude_from_position_files.setter
    def exclude_from_position_files(self, exclude: bool):
        self._proto.exclude_from_position_files = exclude

class Footprint(Wrapper):
    """Represents a library footprint"""
    def __init__(self, proto: Optional[board_types_pb2.Footprint] = None,
                 proto_ref: Optional[board_types_pb2.Footprint] = None):
        self._proto = proto_ref if proto_ref is not None else board_types_pb2.Footprint()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def items(self) -> Sequence[Wrapper]:
        return [unwrap(item) for item in self._proto.items]
    
    def add_item(self, item: Wrapper):
        any = Any()
        any.Pack(item.proto)
        self._proto.items.append(any)

class FootprintInstance(BoardItem):
    """Represents a footprint instance on a board"""
    def __init__(self, proto: Optional[board_types_pb2.FootprintInstance] = None):
        self._proto = board_types_pb2.FootprintInstance()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def id(self) -> KIID:
        return self._proto.id
    
    @property
    def layer(self) -> BoardLayer.ValueType:
        return self._proto.layer
    
    @layer.setter
    def layer(self, layer: BoardLayer.ValueType):
        self._proto.layer = layer

    @property
    def definition(self) -> Footprint:
        return Footprint(proto_ref=self._proto.definition)
    
    @property
    def reference_field(self) -> Field:
        return Field(proto_ref=self._proto.reference_field)
    
    @property
    def value_field(self) -> Field:
        return Field(proto_ref=self._proto.value_field)
    
    @property
    def attributes(self) -> FootprintAttributes:
        return FootprintAttributes(proto_ref=self._proto.attributes)
    
_proto_to_object: Dict[type[Message], type[Wrapper]] = {
    board_types_pb2.Arc: Arc,
    board_types_pb2.FootprintInstance: FootprintInstance,
    board_types_pb2.Net: Net,
    board_types_pb2.Pad: Pad,
    board_types_pb2.Text: Text,
    board_types_pb2.Track: Track,
    board_types_pb2.Via: Via,
}

def unwrap(message: Any) -> Wrapper:
    concrete = unpack_any(message)
    wrapper = _proto_to_object.get(type(concrete), None)
    assert(wrapper is not None)
    return wrapper(concrete)