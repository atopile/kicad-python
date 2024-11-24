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

# Re-exported protobuf enum types
from kipy.proto.common.types.enums_pb2 import (  # noqa
    HorizontalAlignment,
    VerticalAlignment,
)

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

    @property
    def font_name(self) -> str:
        return self._proto.font_name

    @font_name.setter
    def font_name(self, font_name: str):
        self._proto.font_name = font_name

    @property
    def angle(self) -> types.Angle:
        return self._proto.angle

    @angle.setter
    def angle(self, angle: types.Angle):
        self._proto.angle.CopyFrom(angle)

    @property
    def line_spacing(self) -> float:
        return self._proto.line_spacing

    @line_spacing.setter
    def line_spacing(self, line_spacing: float):
        self._proto.line_spacing = line_spacing

    @property
    def stroke_width(self) -> types.Distance:
        return self._proto.stroke_width

    @stroke_width.setter
    def stroke_width(self, stroke_width: types.Distance):
        self._proto.stroke_width.CopyFrom(stroke_width)

    @property
    def italic(self) -> bool:
        return self._proto.italic

    @italic.setter
    def italic(self, italic: bool):
        self._proto.italic = italic

    @property
    def bold(self) -> bool:
        return self._proto.bold

    @bold.setter
    def bold(self, bold: bool):
        self._proto.bold = bold

    @property
    def underlined(self) -> bool:
        return self._proto.underlined

    @underlined.setter
    def underlined(self, underlined: bool):
        self._proto.underlined = underlined

    @property
    def mirrored(self) -> bool:
        return self._proto.mirrored

    @mirrored.setter
    def mirrored(self, mirrored: bool):
        self._proto.mirrored = mirrored

    @property
    def multiline(self) -> bool:
        return self._proto.multiline

    @multiline.setter
    def multiline(self, multiline: bool):
        self._proto.multiline = multiline

    @property
    def keep_upright(self) -> bool:
        return self._proto.keep_upright

    @keep_upright.setter
    def keep_upright(self, keep_upright: bool):
        self._proto.keep_upright = keep_upright

    @property
    def size(self) -> Vector2:
        return Vector2(self._proto.size)

    @size.setter
    def size(self, size: Vector2):
        self._proto.size.CopyFrom(size.proto)

    @property
    def horizontal_alignment(self) -> types.HorizontalAlignment.ValueType:
        return self._proto.horizontal_alignment

    @horizontal_alignment.setter
    def horizontal_alignment(self, alignment: types.HorizontalAlignment.ValueType):
        self._proto.horizontal_alignment = alignment

    @property
    def vertical_alignment(self) -> types.VerticalAlignment.ValueType:
        return self._proto.vertical_alignment

    @vertical_alignment.setter
    def vertical_alignment(self, alignment: types.VerticalAlignment.ValueType):
        self._proto.vertical_alignment = alignment

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

class TextBox(Wrapper):
    def __init__(self, proto: Optional[types.TextBox] = None,
                    proto_ref: Optional[types.TextBox] = None):
        self._proto = proto_ref if proto_ref is not None else types.TextBox()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def id(self) -> KIID:
        return self._proto.id

    @property
    def top_left(self) -> Vector2:
        return Vector2(self._proto.top_left)

    @top_left.setter
    def top_left(self, pos: Vector2):
        self._proto.top_left.CopyFrom(pos.proto)

    @property
    def bottom_right(self) -> Vector2:
        return Vector2(self._proto.bottom_right)

    @bottom_right.setter
    def bottom_right(self, pos: Vector2):
        self._proto.bottom_right.CopyFrom(pos.proto)

    @property
    def attributes(self) -> TextAttributes:
        return TextAttributes(proto_ref=self._proto.attributes)

    @attributes.setter
    def attributes(self, attributes: TextAttributes):
        self._proto.attributes.CopyFrom(attributes.proto)

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
    def text(self) -> str:
        return self._proto.text

    @text.setter
    def text(self, text: str):
        self._proto.text = text
class TitleBlockInfo(Wrapper):
    def __init__(self, proto: Optional[types.TitleBlockInfo] = None,
                    proto_ref: Optional[types.TitleBlockInfo] = None):
        self._proto = proto_ref if proto_ref is not None else types.TitleBlockInfo()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def title(self) -> str:
        return self._proto.title

    @title.setter
    def title(self, title: str):
        self._proto.title = title

    @property
    def date(self) -> str:
        return self._proto.date

    @date.setter
    def date(self, date: str):
        self._proto.date = date

    @property
    def revision(self) -> str:
        return self._proto.revision

    @revision.setter
    def revision(self, revision: str):
        self._proto.revision = revision

    @property
    def company(self) -> str:
        return self._proto.company

    @company.setter
    def company(self, company: str):
        self._proto.company = company

    @property
    def comments(self) -> dict[int, str]:
        return {
            1: self._proto.comment1,
            2: self._proto.comment2,
            3: self._proto.comment3,
            4: self._proto.comment4,
            5: self._proto.comment5,
            6: self._proto.comment6,
            7: self._proto.comment7,
            8: self._proto.comment8,
            9: self._proto.comment9
        }

    @comments.setter
    def comments(self, comments: dict[int, str]):
        if 1 in comments:
            self._proto.comment1 = comments[1]
        if 2 in comments:
            self._proto.comment2 = comments[2]
        if 3 in comments:
            self._proto.comment3 = comments[3]
        if 4 in comments:
            self._proto.comment4 = comments[4]
        if 5 in comments:
            self._proto.comment5 = comments[5]
        if 6 in comments:
            self._proto.comment6 = comments[6]
        if 7 in comments:
            self._proto.comment7 = comments[7]
        if 8 in comments:
            self._proto.comment8 = comments[8]
        if 9 in comments:
            self._proto.comment9 = comments[9]
