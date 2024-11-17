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

from math import pi
from typing import Dict, Sequence, Optional, Union
from google.protobuf.message import Message
from google.protobuf.any_pb2 import Any

from kipy.proto.common.types import KIID
from kipy.proto.common.types.base_types_pb2 import LockedState, PolygonWithHoles
from kipy.proto.board import board_types_pb2
from kipy.common_types import GraphicAttributes, TextAttributes, LibraryIdentifier
from kipy.geometry import Box2, Vector2
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

class ArcTrack(BoardItem):
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

class Shape(BoardItem):
    """Represents a graphic shape on a board or footprint"""
    def __init__(self, proto: Optional[board_types_pb2.GraphicShape] = None):
        self._proto = board_types_pb2.GraphicShape()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def id(self) -> KIID:
        return self._proto.id

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
    def layer(self) -> board_types_pb2.BoardLayer.ValueType:
        return self._proto.layer

    @layer.setter
    def layer(self, layer: board_types_pb2.BoardLayer.ValueType):
        self._proto.layer = layer

    @property
    def net(self) -> Net:
        return Net(self._proto.net)

    @net.setter
    def net(self, net: Net):
        self._proto.net.CopyFrom(net.proto)

    @property
    def attributes(self) -> GraphicAttributes:
        return GraphicAttributes(proto_ref=self._proto.attributes)

    @attributes.setter
    def attributes(self, attributes: GraphicAttributes):
        self._proto.attributes.CopyFrom(attributes.proto)

    def bounding_box(self) -> Box2:
        raise NotImplementedError(f"bounding_box() not implemented for {type(self).__name__}")

class Segment(Shape):
    """Represents a graphic line segment (not a track) on a board or footprint"""
    def __init__(self, proto: Optional[board_types_pb2.GraphicShape] = None):
        self._proto = board_types_pb2.GraphicShape()

        if proto is not None:
            self._proto.CopyFrom(proto)

        assert(self._proto.WhichOneof('geometry') == 'segment')

    @property
    def start(self) -> Vector2:
        return Vector2(self._proto.segment.start)

    @start.setter
    def start(self, point: Vector2):
        self._proto.segment.start.CopyFrom(point.proto)

    @property
    def end(self) -> Vector2:
        return Vector2(self._proto.segment.end)

    @end.setter
    def end(self, point: Vector2):
        self._proto.segment.end.CopyFrom(point.proto)

    def bounding_box(self) -> Box2:
        """Calculates the bounding box of the segment"""
        box = Box2()
        box.merge(self.start)
        box.merge(self.end)
        return box

class Arc(Shape):
    """Represents a graphic arc (not a track) on a board or footprint"""
    def __init__(self, proto: Optional[board_types_pb2.GraphicShape] = None):
        self._proto = board_types_pb2.GraphicShape()

        if proto is not None:
            self._proto.CopyFrom(proto)

        assert(self._proto.WhichOneof('geometry') == 'arc')

    @property
    def start(self) -> Vector2:
        return Vector2(self._proto.arc.start)

    @start.setter
    def start(self, point: Vector2):
        self._proto.arc.start.CopyFrom(point.proto)

    @property
    def mid(self) -> Vector2:
        return Vector2(self._proto.arc.mid)

    @mid.setter
    def mid(self, point: Vector2):
        self._proto.arc.mid.CopyFrom(point.proto)

    @property
    def end(self) -> Vector2:
        return Vector2(self._proto.arc.end)

    @end.setter
    def end(self, point: Vector2):
        self._proto.arc.end.CopyFrom(point.proto)

    def center(self) -> Optional[Vector2]:
        """
        Calculates the center of the arc.  Uses a different algorithm than KiCad so may have
        slightly different results.  The KiCad API preserves the start, middle, and end points of
        the arc, so any other properties such as the center point and angles must be calculated

        :return: The center of the arc, or None if the arc is degenerate
        """
        if self.start == self.end:
            return (self.start + self.mid) * 0.5

        def perpendicular_bisector(p1: Vector2, p2: Vector2):
            mid_point = (p1 + p2) * 0.5
            direction = p2 - p1
            perpendicular_direction = Vector2.from_xy(-direction.y, direction.x)
            return mid_point, perpendicular_direction

        mid1, dir1 = perpendicular_bisector(self.start, self.mid)
        mid2, dir2 = perpendicular_bisector(self.mid, self.end)

        det = dir1.x * dir2.y - dir1.y * dir2.x

        if det == 0:
            return None

        # Intersect the two perpendicular bisectors to find the center
        t = (mid2.x - mid1.x) * dir2.y - (mid2.y - mid1.y) * dir2.x / det
        center = mid1 + dir1 * t

        return center

    def radius(self) -> float:
        """
        Calculates the radius of the arc.  Uses a different algorithm than KiCad so may have
        slightly different results.  The KiCad API preserves the start, middle, and end points of
        the arc, so any other properties such as the center point and angles must be calculated

        :return: The radius of the arc, or 0 if the arc is degenerate
        """
        center = self.center()
        if center is None:
            return 0

        return (self.start - center).length()

    def start_angle(self) -> Optional[float]:
        center = self.center()
        if center is None:
            return None

        return (self.start - center).angle()

    def end_angle(self) -> Optional[float]:
        center = self.center()
        if center is None:
            return None

        angle = (self.end - center).angle()

        start_angle = self.start_angle()
        assert(start_angle is not None)

        if angle == self.start_angle():
            angle += 2 * pi

        while angle < start_angle:
            angle += 2 * pi

        return angle

    def bounding_box(self) -> Box2:
        box = Box2()
        box.merge(self.start)
        box.merge(self.end)
        box.merge(self.mid)
        return box

class Circle(Shape):
    """Represents a graphic circle on a board or footprint"""
    def __init__(self, proto: Optional[board_types_pb2.GraphicShape] = None):
        self._proto = board_types_pb2.GraphicShape()

        if proto is not None:
            self._proto.CopyFrom(proto)

        assert(self._proto.WhichOneof('geometry') == 'circle')

    @property
    def center(self) -> Vector2:
        return Vector2(self._proto.circle.center)

    @center.setter
    def center(self, point: Vector2):
        self._proto.circle.center.CopyFrom(point.proto)

    @property
    def radius_point(self) -> Vector2:
        return Vector2(self._proto.circle.radius_point)

    @radius_point.setter
    def radius_point(self, radius_point: Vector2):
        self._proto.circle.radius_point.CopyFrom(radius_point.proto)

    def radius(self) -> float:
        """Calculates the radius of the circle"""
        return (self.radius_point - self.center).length()

    def bounding_box(self) -> Box2:
        """Calculates the bounding box of the circle"""
        box = Box2()
        box.merge(self.center)
        box.inflate(int(self.radius() + 0.5))
        return box

class Rectangle(Shape):
    """Represents a graphic rectangle on a board or footprint"""
    def __init__(self, proto: Optional[board_types_pb2.GraphicShape] = None):
        self._proto = board_types_pb2.GraphicShape()

        if proto is not None:
            self._proto.CopyFrom(proto)

        assert(self._proto.WhichOneof('geometry') == 'rectangle')

    @property
    def top_left(self) -> Vector2:
        return Vector2(self._proto.rectangle.top_left)

    @top_left.setter
    def top_left(self, point: Vector2):
        self._proto.rectangle.top_left.CopyFrom(point.proto)

    @property
    def bottom_right(self) -> Vector2:
        return Vector2(self._proto.rectangle.bottom_right)

    @bottom_right.setter
    def bottom_right(self, point: Vector2):
        self._proto.rectangle.bottom_right.CopyFrom(point.proto)

    def bounding_box(self) -> Box2:
        """Calculates the bounding box of the rectangle"""
        return Box2.from_pos_size(self.top_left, self.bottom_right - self.top_left)

class Polygon(Shape):
    """Represents a graphic polygon on a board or footprint"""
    def __init__(self, proto: Optional[board_types_pb2.GraphicShape] = None):
        self._proto = board_types_pb2.GraphicShape()

        if proto is not None:
            self._proto.CopyFrom(proto)

        assert(self._proto.WhichOneof('geometry') == 'polygon')

    @property
    def polygons(self) -> Sequence[PolygonWithHoles]:
        return self._proto.polygon.polygons

    @polygons.setter
    def polygons(self, polygons: Sequence[PolygonWithHoles]):
        del self._proto.polygon.polygons[:]
        self._proto.polygon.polygons.extend(polygons)

    def bounding_box(self) -> Box2:
        """Calculates the bounding box of the polygon"""
        box = Box2()
        for polygon in self.polygons:
            for node in polygon.outline.nodes:
                if node.arc:
                    box.merge(Vector2(node.arc.start))
                    box.merge(Vector2(node.arc.end))
                else:
                    box.merge(Vector2(node.point))
        return box

class Bezier(Shape):
    """Represents a graphic bezier curve on a board or footprint"""
    def __init__(self, proto: Optional[board_types_pb2.GraphicShape] = None):
        self._proto = board_types_pb2.GraphicShape()

        if proto is not None:
            self._proto.CopyFrom(proto)

        assert(self._proto.WhichOneof('geometry') == 'bezier')

    @property
    def start(self) -> Vector2:
        return Vector2(self._proto.bezier.start)

    @start.setter
    def start(self, point: Vector2):
        self._proto.bezier.start.CopyFrom(point.proto)

    @property
    def control1(self) -> Vector2:
        return Vector2(self._proto.bezier.control1)

    @control1.setter
    def control1(self, point: Vector2):
        self._proto.bezier.control1.CopyFrom(point.proto)

    @property
    def control2(self) -> Vector2:
        return Vector2(self._proto.bezier.control2)

    @control2.setter
    def control2(self, point: Vector2):
        self._proto.bezier.control2.CopyFrom(point.proto)

    @property
    def end(self) -> Vector2:
        return Vector2(self._proto.bezier.end)

    @end.setter
    def end(self, point: Vector2):
        self._proto.bezier.end.CopyFrom(point.proto)

    def bounding_box(self) -> Box2:
        # TODO: maybe bring in a library for Bezier curve math so we can generate an
        # bounding box from the curve approximation like KiCad does?
        raise NotImplementedError()

def to_concrete_shape(
    shape: Shape,
) -> Union[Segment, Arc, Circle, Rectangle, Polygon, Bezier, None]:
    cls = {
        'segment': Segment,
        'arc': Arc,
        'circle': Circle,
        'rectangle': Rectangle,
        'polygon': Polygon,
        'bezier': Bezier,
        None: None
    }.get(shape._proto.WhichOneof('geometry'), None)

    return cls(shape._proto) if cls is not None else None

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
    def id(self) -> LibraryIdentifier:
        return LibraryIdentifier(proto_ref=self._proto.id)

    @id.setter
    def id(self, attributes: LibraryIdentifier):
        self._proto.id.CopyFrom(attributes.proto)

    @property
    def items(self) -> Sequence[Wrapper]:
        return [unwrap(item) for item in self._proto.items]

    def pads(self) -> Sequence[Pad]:
        return [item for item in self.items if isinstance(item, Pad)]

    def shapes(self) -> Sequence[Shape]:
        return [item for item in self.items if isinstance(item, Shape)]

    def texts(self) -> Sequence[Text]:
        return [item for item in self.items if isinstance(item, Text)]

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
        """The layer on which the footprint is placed (BoardLayer.BL_F_Cu or BoardLayer.BL_B_Cu)"""
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
    board_types_pb2.GraphicShape: Shape,
    board_types_pb2.Field: Field,
}

def unwrap(message: Any) -> Wrapper:
    concrete = unpack_any(message)
    wrapper = _proto_to_object.get(type(concrete), None)
    assert(wrapper is not None)
    return wrapper(concrete)
