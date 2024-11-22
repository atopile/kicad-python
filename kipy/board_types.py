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

from typing import Dict, Sequence, Optional, Union
from google.protobuf.message import Message
from google.protobuf.any_pb2 import Any

from kipy.proto.common.types import KIID
from kipy.proto.common.types.base_types_pb2 import LockedState
from kipy.proto.board import board_types_pb2
from kipy.common_types import GraphicAttributes, Text, LibraryIdentifier
from kipy.geometry import (
    Angle,
    Box2,
    Vector2,
    PolygonWithHoles,
    arc_center,
    arc_radius,
    arc_start_angle,
    arc_end_angle,
)
from kipy.util import unpack_any
from kipy.wrapper import Item, Wrapper

# Re-exported protobuf enum types
from kipy.proto.board.board_types_pb2 import ( #noqa
    BoardLayer,
    ChamferedRectCorners,
    DrillShape,
    PadType,
    PadStackShape,
    SolderMaskMode,
    SolderPasteMode,
    UnconnectedLayerRemoval,
    ZoneConnectionStyle,
    ViaType
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
    def layer(self) -> BoardLayer.ValueType:
        return self._proto.layer

    @layer.setter
    def layer(self, layer: BoardLayer.ValueType):
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
    def layer(self) -> BoardLayer.ValueType:
        return self._proto.layer

    @layer.setter
    def layer(self, layer: BoardLayer.ValueType):
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

    def center(self) -> Optional[Vector2]:
        """
        Calculates the center of the arc.  Uses a different algorithm than KiCad so may have
        slightly different results.  The KiCad API preserves the start, middle, and end points of
        the arc, so any other properties such as the center point and angles must be calculated

        :return: The center of the arc, or None if the arc is degenerate
        """
        # TODO we may want to add an API call to get KiCad to calculate this for us,
        # for situations where matching KiCad's behavior exactly is important
        return arc_center(self.start, self.mid, self.end)

    def radius(self) -> float:
        """
        Calculates the radius of the arc.  Uses a different algorithm than KiCad so may have
        slightly different results.  The KiCad API preserves the start, middle, and end points of
        the arc, so any other properties such as the center point and angles must be calculated

        :return: The radius of the arc, or 0 if the arc is degenerate
        """
        # TODO we may want to add an API call to get KiCad to calculate this for us,
        # for situations where matching KiCad's behavior exactly is important
        return arc_radius(self.start, self.mid, self.end)

    def start_angle(self) -> Optional[float]:
        return arc_start_angle(self.start, self.mid, self.end)

    def end_angle(self) -> Optional[float]:
        return arc_end_angle(self.start, self.mid, self.end)

    def bounding_box(self) -> Box2:
        box = Box2()
        box.merge(self.start)
        box.merge(self.end)
        box.merge(self.mid)
        return box

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
    def layer(self) -> BoardLayer.ValueType:
        return self._proto.layer

    @layer.setter
    def layer(self, layer: BoardLayer.ValueType):
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
        # TODO we may want to add an API call to get KiCad to calculate this for us,
        # for situations where matching KiCad's behavior exactly is important
        return arc_center(self.start, self.mid, self.end)

    def radius(self) -> float:
        """
        Calculates the radius of the arc.  Uses a different algorithm than KiCad so may have
        slightly different results.  The KiCad API preserves the start, middle, and end points of
        the arc, so any other properties such as the center point and angles must be calculated

        :return: The radius of the arc, or 0 if the arc is degenerate
        """
        # TODO we may want to add an API call to get KiCad to calculate this for us,
        # for situations where matching KiCad's behavior exactly is important
        return arc_radius(self.start, self.mid, self.end)

    def start_angle(self) -> Optional[float]:
        return arc_start_angle(self.start, self.mid, self.end)

    def end_angle(self) -> Optional[float]:
        return arc_end_angle(self.start, self.mid, self.end)

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
        return [PolygonWithHoles(proto_ref=p) for p in self._proto.polygon.polygons]

    def bounding_box(self) -> Box2:
        """Calculates the bounding box of the polygon"""
        box = None
        for polygon in self.polygons:
            if box is None:
                box = polygon.bounding_box()
            else:
                box.merge(polygon.bounding_box())
        return box if box is not None else Box2()

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

class BoardText(BoardItem):
    """Represents a free text object, or the text component of a field"""
    def __init__(self, proto: Optional[board_types_pb2.Text] = None,
                 proto_ref: Optional[board_types_pb2.Text] = None):
        self._proto = proto_ref if proto_ref is not None else board_types_pb2.Text()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def layer(self) -> BoardLayer.ValueType:
        return self._proto.layer

    @layer.setter
    def layer(self, layer: BoardLayer.ValueType):
        self._proto.layer = layer

    @property
    def text(self) -> Text:
        return Text(proto_ref=self._proto.text)

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
    def layer(self) -> BoardLayer.ValueType:
        return self._proto.text.layer

    @property
    def board_text(self) -> BoardText:
        return BoardText(proto_ref=self._proto.text)

    @property
    def text(self) -> Text:
        return Text(proto_ref=self._proto.text.text)

class ZoneConnectionSettings(Wrapper):
    def __init__(self, proto: Optional[board_types_pb2.ZoneConnectionSettings] = None,
                 proto_ref: Optional[board_types_pb2.ZoneConnectionSettings] = None):
        self._proto = (
            proto_ref
            if proto_ref is not None
            else board_types_pb2.ZoneConnectionSettings()
        )

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def zone_connection(self) -> ZoneConnectionStyle.ValueType:
        return self._proto.zone_connection

    @zone_connection.setter
    def zone_connection(self, zone_connection: ZoneConnectionStyle.ValueType):
        self._proto.zone_connection = zone_connection

    @property
    def thermal_spokes(self) -> board_types_pb2.ThermalSpokeSettings:
        return self._proto.thermal_spokes

class SolderMaskOverrides(Wrapper):
    def __init__(self, proto: Optional[board_types_pb2.SolderMaskOverrides] = None,
                 proto_ref: Optional[board_types_pb2.SolderMaskOverrides] = None):
        self._proto = proto_ref if proto_ref is not None else board_types_pb2.SolderMaskOverrides()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def solder_mask_margin(self) -> int:
        return self._proto.solder_mask_margin.value_nm

    @solder_mask_margin.setter
    def solder_mask_margin(self, margin_nm: int):
        self._proto.solder_mask_margin.value_nm = margin_nm

class SolderPasteOverrides(Wrapper):
    def __init__(self, proto: Optional[board_types_pb2.SolderPasteOverrides] = None,
                 proto_ref: Optional[board_types_pb2.SolderPasteOverrides] = None):
        self._proto = proto_ref if proto_ref is not None else board_types_pb2.SolderPasteOverrides()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def solder_paste_margin(self) -> int:
        return self._proto.solder_paste_margin.value_nm

    @solder_paste_margin.setter
    def solder_paste_margin(self, margin_nm: int):
        self._proto.solder_paste_margin.value_nm = margin_nm

    @property
    def solder_paste_margin_ratio(self) -> float:
        return self._proto.solder_paste_margin_ratio.value

    @solder_paste_margin_ratio.setter
    def solder_paste_margin_ratio(self, ratio: float):
        self._proto.solder_paste_margin_ratio.value = ratio

class PadStackLayer(Wrapper):
    def __init__(self, proto: Optional[board_types_pb2.PadStackLayer] = None,
                 proto_ref: Optional[board_types_pb2.PadStackLayer] = None):
        self._proto = proto_ref if proto_ref is not None else board_types_pb2.PadStackLayer()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def layer(self) -> BoardLayer.ValueType:
        return self._proto.layer

    @layer.setter
    def layer(self, layer: BoardLayer.ValueType):
        self._proto.layer = layer

    @property
    def shape(self) -> PadStackShape.ValueType:
        return self._proto.shape

    @shape.setter
    def shape(self, shape: PadStackShape.ValueType):
        self._proto.shape = shape

    @property
    def size(self) -> Vector2:
        return Vector2(self._proto.size)

    @size.setter
    def size(self, size: Vector2):
        self._proto.size.CopyFrom(size.proto)

    @property
    def offset(self) -> Vector2:
        return Vector2(self._proto.offset)

    @offset.setter
    def offset(self, offset: Vector2):
        self._proto.offset.CopyFrom(offset.proto)

    @property
    def corner_rounding_ratio(self) -> float:
        return self._proto.corner_rounding_ratio

    @corner_rounding_ratio.setter
    def corner_rounding_ratio(self, ratio: float):
        self._proto.corner_rounding_ratio = ratio

    @property
    def chamfer_ratio(self) -> float:
        return self._proto.chamfer_ratio

    @chamfer_ratio.setter
    def chamfer_ratio(self, ratio: float):
        self._proto.chamfer_ratio = ratio

    @property
    def chamfered_corners(self) -> board_types_pb2.ChamferedRectCorners:
        return self._proto.chamfered_corners

    @property
    def trapezoid_delta(self) -> Vector2:
        return Vector2(self._proto.trapezoid_delta)

    @trapezoid_delta.setter
    def trapezoid_delta(self, delta: Vector2):
        self._proto.trapezoid_delta.CopyFrom(delta.proto)

    @property
    def custom_shapes(self) -> Sequence[Shape]:
        return [
            item
            for item in (
                to_concrete_shape(Shape(shape)) for shape in self._proto.custom_shapes
            )
            if item is not None
        ]

    @custom_shapes.setter
    def custom_shapes(self, shapes: Sequence[Shape]):
        del self._proto.custom_shapes[:]
        self._proto.custom_shapes.extend([shape.proto for shape in shapes])

    @property
    def custom_anchor_shape(self) -> PadStackShape.ValueType:
        return self._proto.custom_anchor_shape

    @custom_anchor_shape.setter
    def custom_anchor_shape(self, shape: PadStackShape.ValueType):
        self._proto.custom_anchor_shape = shape

    @property
    def zone_settings(self) -> board_types_pb2.ZoneConnectionSettings:
        return self._proto.zone_settings

    @zone_settings.setter
    def zone_settings(self, settings: board_types_pb2.ZoneConnectionSettings):
        self._proto.zone_settings.CopyFrom(settings)

class DrillProperties(Wrapper):
    def __init__(self, proto: Optional[board_types_pb2.DrillProperties] = None,
                 proto_ref: Optional[board_types_pb2.DrillProperties] = None):
        self._proto = proto_ref if proto_ref is not None else board_types_pb2.DrillProperties()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def start_layer(self) -> BoardLayer.ValueType:
        return self._proto.start_layer

    @start_layer.setter
    def start_layer(self, layer: BoardLayer.ValueType):
        self._proto.start_layer = layer

    @property
    def end_layer(self) -> BoardLayer.ValueType:
        return self._proto.end_layer

    @end_layer.setter
    def end_layer(self, layer: BoardLayer.ValueType):
        self._proto.end_layer = layer

    @property
    def diameter(self) -> Vector2:
        """The drill diameter, which may also be a milled slot with different X and Y dimensions"""
        return Vector2(self._proto.diameter)

    @diameter.setter
    def diameter(self, diameter: Vector2):
        self._proto.diameter.CopyFrom(diameter.proto)

    @property
    def shape(self) -> board_types_pb2.DrillShape.ValueType:
        return self._proto.shape

    @shape.setter
    def shape(self, shape: board_types_pb2.DrillShape.ValueType):
        self._proto.shape = shape


class PadStackOuterLayer(Wrapper):
    def __init__(self, proto: Optional[board_types_pb2.PadStackOuterLayer] = None,
                 proto_ref: Optional[board_types_pb2.PadStackOuterLayer] = None):
        self._proto = proto_ref if proto_ref is not None else board_types_pb2.PadStackOuterLayer()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def solder_mask_mode(self) -> board_types_pb2.SolderMaskMode.ValueType:
        return self._proto.solder_mask_mode

    @solder_mask_mode.setter
    def solder_mask_mode(self, mode: board_types_pb2.SolderMaskMode.ValueType):
        self._proto.solder_mask_mode = mode

    @property
    def solder_paste_mode(self) -> board_types_pb2.SolderPasteMode.ValueType:
        return self._proto.solder_paste_mode

    @solder_paste_mode.setter
    def solder_paste_mode(self, mode: board_types_pb2.SolderPasteMode.ValueType):
        self._proto.solder_paste_mode = mode

    @property
    def solder_mask_settings(self) -> SolderMaskOverrides:
        return SolderMaskOverrides(proto_ref=self._proto.solder_mask_settings)

    @solder_mask_settings.setter
    def solder_mask_settings(self, settings: SolderMaskOverrides):
        self._proto.solder_mask_settings.CopyFrom(settings.proto)

    @property
    def solder_paste_settings(self) -> SolderPasteOverrides:
        return SolderPasteOverrides(proto_ref=self._proto.solder_paste_settings)

    @solder_paste_settings.setter
    def solder_paste_settings(self, settings: SolderPasteOverrides):
        self._proto.solder_paste_settings.CopyFrom(settings.proto)

class PadStack(BoardItem):
    def __init__(self, proto: Optional[board_types_pb2.PadStack] = None,
                 proto_ref: Optional[board_types_pb2.PadStack] = None):
        self._proto = proto_ref if proto_ref is not None else board_types_pb2.PadStack()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def type(self) -> board_types_pb2.PadStackType.ValueType:
        return self._proto.type

    @type.setter
    def type(self, type: board_types_pb2.PadStackType.ValueType):
        self._proto.type = type

    @property
    def layers(self) -> Sequence[BoardLayer.ValueType]:
        return self._proto.layers

    @layers.setter
    def layers(self, layers: Sequence[BoardLayer.ValueType]):
        del self._proto.layers[:]
        self._proto.layers.extend(layers)

    @property
    def drill(self) -> DrillProperties:
        return DrillProperties(proto_ref=self._proto.drill)

    @property
    def unconnected_layer_removal(self) -> UnconnectedLayerRemoval.ValueType:
        return self._proto.unconnected_layer_removal

    @unconnected_layer_removal.setter
    def unconnected_layer_removal(self, removal: UnconnectedLayerRemoval.ValueType):
        self._proto.unconnected_layer_removal = removal

    @property
    def copper_layers(self) -> list[PadStackLayer]:
        return [PadStackLayer(proto_ref=p) for p in self._proto.copper_layers]

    def copper_layer(self, layer: BoardLayer.ValueType) -> Optional[PadStackLayer]:
        for copper_layer in self.copper_layers:
            if copper_layer.layer == layer:
                return copper_layer
        return None

    @property
    def angle(self) -> Angle:
        return Angle(self._proto.angle)

    @angle.setter
    def angle(self, angle: Angle):
        self._proto.angle.CopyFrom(angle.proto)

    @property
    def front_outer_layers(self) -> PadStackOuterLayer:
        return PadStackOuterLayer(proto_ref=self._proto.front_outer_layers)

    @property
    def back_outer_layers(self) -> PadStackOuterLayer:
        return PadStackOuterLayer(proto_ref=self._proto.back_outer_layers)

    @property
    def zone_settings(self) -> ZoneConnectionSettings:
        return ZoneConnectionSettings(proto_ref=self._proto.zone_settings)

    def is_masked(self, layer: BoardLayer.ValueType = BoardLayer.BL_UNDEFINED) -> bool:
        """
        Returns true if the padstack is masked on the given copper layer, or on either layer if
        layer is BL_UNDEFINED.
        """
        if layer == BoardLayer.BL_UNDEFINED:
            return (
            self.front_outer_layers.solder_mask_mode == SolderMaskMode.SMM_MASKED or
            self.back_outer_layers.solder_mask_mode == SolderMaskMode.SMM_MASKED
            )
        elif layer == BoardLayer.BL_F_Cu:
            return self.front_outer_layers.solder_mask_mode == SolderMaskMode.SMM_MASKED
        elif layer == BoardLayer.BL_B_Cu:
            return self.back_outer_layers.solder_mask_mode == SolderMaskMode.SMM_MASKED
        return False

class Pad(BoardItem):
    def __init__(self, proto: Optional[board_types_pb2.Pad] = None):
        self._proto = board_types_pb2.Pad()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def id(self) -> KIID:
        return self._proto.id

    @property
    def number(self) -> str:
        return self._proto.number

    @number.setter
    def number(self, number: str):
        self._proto.number = number

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

    @property
    def padstack(self) -> PadStack:
        return PadStack(proto_ref=self._proto.pad_stack)

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

    @property
    def locked(self) -> bool:
        return self._proto.locked == LockedState.LS_LOCKED

    @locked.setter
    def locked(self, locked: bool):
        self._proto.locked = LockedState.LS_LOCKED if locked else LockedState.LS_UNLOCKED

    @property
    def type(self) -> ViaType.ValueType:
        return self._proto.type

    @type.setter
    def type(self, type: ViaType.ValueType):
        self._proto.type = type

    @property
    def padstack(self) -> PadStack:
        return PadStack(proto_ref=self._proto.pad_stack)

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
        """Returns all pads in the footprint"""
        return [item for item in self.items if isinstance(item, Pad)]

    def shapes(self) -> Sequence[Shape]:
        """Returns all graphic shapes in the footprint"""
        return [
            item
            for item in (
                to_concrete_shape(shape)
                for shape in [
                    item
                    for item in self.items
                    if isinstance(item, Shape)
                ]
            )
            if item is not None
        ]

    def texts(self) -> Sequence[Text]:
        """Returns al free text objects in the footprint"""
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
    def position(self) -> Vector2:
        return Vector2(self._proto.position)

    @position.setter
    def position(self, position: Vector2):
        self._proto.position.CopyFrom(position.proto)

    @property
    def orientation(self) -> Angle:
        return Angle(self._proto.orientation)

    @orientation.setter
    def orientation(self, orientation: Angle):
        self._proto.orientation.CopyFrom(orientation.proto)

    @property
    def layer(self) -> BoardLayer.ValueType:
        """The layer on which the footprint is placed (BoardLayer.BL_F_Cu or BoardLayer.BL_B_Cu)"""
        return self._proto.layer

    @layer.setter
    def layer(self, layer: BoardLayer.ValueType):
        self._proto.layer = layer

    @property
    def locked(self) -> bool:
        return self._proto.locked == LockedState.LS_LOCKED

    @locked.setter
    def locked(self, locked: bool):
        self._proto.locked = LockedState.LS_LOCKED if locked else LockedState.LS_UNLOCKED

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
    def datasheet_field(self) -> Field:
        return Field(proto_ref=self._proto.datasheet_field)

    @property
    def description_field(self) -> Field:
        return Field(proto_ref=self._proto.description_field)

    @property
    def attributes(self) -> FootprintAttributes:
        return FootprintAttributes(proto_ref=self._proto.attributes)

_proto_to_object: Dict[type[Message], type[Wrapper]] = {
    board_types_pb2.Arc: Arc,
    board_types_pb2.FootprintInstance: FootprintInstance,
    board_types_pb2.Net: Net,
    board_types_pb2.Pad: Pad,
    board_types_pb2.Text: BoardText,
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
