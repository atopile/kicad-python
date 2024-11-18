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

from typing import Optional
from kipy.proto.common import types
from kipy.proto.common.types.base_types_pb2 import KIID, LockedState
from kipy.geometry import Vector2
from kipy.wrapper import Wrapper

class Commit:
    def __init__(self, id: KIID):
        self._id = id

    @property
    def id(self) -> KIID:
        return self._id

class Color(Wrapper):
    def __init__(self, proto: Optional[types.Color] = None,
                    proto_ref: Optional[types.Color] = None):
        self._proto = proto_ref if proto_ref is not None else types.Color()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def red(self) -> float:
        return self._proto.r

    @red.setter
    def red(self, red: float):
        self._proto.r = red

    @property
    def green(self) -> float:
        return self._proto.g

    @green.setter
    def green(self, green: float):
        self._proto.g = green

    @property
    def blue(self) -> float:
        return self._proto.b

    @blue.setter
    def blue(self, blue: float):
        self._proto.b = blue

    @property
    def alpha(self) -> float:
        return self._proto.a

    @alpha.setter
    def alpha(self, alpha: float):
        self._proto.a = alpha

class TextAttributes(Wrapper):
    def __init__(self, proto: Optional[types.TextAttributes] = None,
                 proto_ref: Optional[types.TextAttributes] = None):
        self._proto = proto_ref if proto_ref is not None else types.TextAttributes()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def visible(self) -> bool:
        return self._proto.visible

    @visible.setter
    def visible(self, visible: bool):
        self._proto.visible = visible

class LibraryIdentifier(Wrapper):
    """A KiCad library identifier (LIB_ID), consisting of a library nickname and entry name"""
    def __init__(self, proto: Optional[types.LibraryIdentifier] = None,
                 proto_ref: Optional[types.LibraryIdentifier] = None):
        self._proto = proto_ref if proto_ref is not None else types.LibraryIdentifier()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def library(self) -> str:
        return self._proto.library_nickname

    @library.setter
    def library(self, library: str):
        self._proto.library_nickname = library

    @property
    def name(self) -> str:
        return self._proto.entry_name

    @name.setter
    def name(self, name: str):
        self._proto.entry_name = name

    def __str__(self) -> str:
        return f"{self.library}:{self.name}"

class StrokeAttributes(Wrapper):
    def __init__(self, proto: Optional[types.StrokeAttributes] = None,
                proto_ref: Optional[types.StrokeAttributes] = None):
        self._proto = proto_ref if proto_ref is not None else types.StrokeAttributes()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def color(self) -> Color:
        """The stroke color.  Only supported in schematic graphics."""
        return Color(proto_ref=self._proto.color)

    @color.setter
    def color(self, color: Color):
        self._proto.color.CopyFrom(color.proto)

    @property
    def width(self) -> int:
        """The stroke line width in nanometers"""
        return self._proto.width.value_nm

    @width.setter
    def width(self, width: int):
        self._proto.width.value_nm = width

    @property
    def style(self) -> types.StrokeLineStyle.ValueType:
        return self._proto.style

    @style.setter
    def style(self, style: types.StrokeLineStyle.ValueType):
        self._proto.style = style

class GraphicFillAttributes(Wrapper):
    def __init__(self, proto: Optional[types.GraphicFillAttributes] = None,
            proto_ref: Optional[types.GraphicFillAttributes] = None):
        self._proto = proto_ref if proto_ref is not None else types.GraphicFillAttributes()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def filled(self) -> bool:
        return self._proto.fill_type == types.GraphicFillType.GFT_FILLED

    @filled.setter
    def filled(self, fill: bool):
        self._proto.fill_type = (
            types.GraphicFillType.GFT_FILLED if fill else types.GraphicFillType.GFT_UNFILLED
        )

    @property
    def color(self) -> Color:
        """The fill color.  Only supported in schematic graphics."""
        return Color(proto_ref=self._proto.color)

    @color.setter
    def color(self, color: Color):
        self._proto.color.CopyFrom(color.proto)

class GraphicAttributes(Wrapper):
    def __init__(self, proto: Optional[types.GraphicAttributes] = None,
            proto_ref: Optional[types.GraphicAttributes] = None):
        self._proto = proto_ref if proto_ref is not None else types.GraphicAttributes()

        if proto is not None:
            self._proto.CopyFrom(proto)

        self._stroke = StrokeAttributes(proto_ref=self._proto.stroke)
        self._fill = GraphicFillAttributes(proto_ref=self._proto.fill)

    @property
    def stroke(self) -> StrokeAttributes:
        return self._stroke

    @property
    def fill(self) -> GraphicFillAttributes:
        return self._fill

class Text(Wrapper):
    """Common text properties (wrapper for KiCad's EDA_TEXT) shared between board and schematic"""
    def __init__(self, proto: Optional[types.Text] = None,
                 proto_ref: Optional[types.Text] = None):
        self._proto = proto_ref if proto_ref is not None else types.Text()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def id(self) -> KIID:
        return self._proto.id

    @property
    def position(self) -> Vector2:
        return Vector2(self._proto.position)

    @position.setter
    def position(self, pos: Vector2):
        self._proto.position.CopyFrom(pos.proto)

    @property
    def locked(self) -> bool:
        return self._proto.locked == LockedState.LS_LOCKED

    @locked.setter
    def locked(self, locked: bool):
        self._proto.locked = {
            True: LockedState.LS_LOCKED,
            False: LockedState.LS_UNLOCKED,
        }.get(locked, LockedState.LS_UNLOCKED)

    @property
    def value(self) -> str:
        return self._proto.text

    @value.setter
    def value(self, text: str):
        self._proto.text = text

    @property
    def attributes(self) -> TextAttributes:
        return TextAttributes(proto_ref=self._proto.attributes)

    @attributes.setter
    def attributes(self, attributes: TextAttributes):
        self._proto.attributes.CopyFrom(attributes.proto)
