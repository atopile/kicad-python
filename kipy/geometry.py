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

from __future__ import annotations

from typing import Optional, Union
import math
from kipy.proto.common import types
from kipy.wrapper import Wrapper

class Vector2(Wrapper):
    """Wraps a kiapi.common.types.Vector2, aka VECTOR2I"""
    def __init__(self, proto: Optional[types.Vector2] = None):
        self._proto = types.Vector2()

        if proto is not None:
            self._proto.CopyFrom(proto)

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    @classmethod
    def from_xy(cls, x_nm: int, y_nm: int):
        """Initialize Vector2 with x and y values in nanometers"""
        proto = types.Vector2()
        proto.x_nm = x_nm
        proto.y_nm = y_nm
        return cls(proto)

    @property
    def x(self) -> int:
        return self._proto.x_nm

    @x.setter
    def x(self, val: int):
        self._proto.x_nm = val

    @property
    def y(self) -> int:
        return self._proto.y_nm

    @y.setter
    def y(self, val: int):
        self._proto.y_nm = val

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __add__(self, other: Vector2) -> Vector2:
        r = Vector2(self._proto)
        r.x += other.x
        r.y += other.y
        return r

    def __sub__(self, other: Vector2) -> Vector2:
        r = Vector2(self._proto)
        r.x -= other.x
        r.y -= other.y
        return r

    def __neg__(self) -> Vector2:
        r = Vector2(self._proto)
        r.x = -r.x
        r.y = -r.y
        return r

    def __mul__(self, scalar: float) -> Vector2:
        r = Vector2(self._proto)
        r.x = int(r.x * scalar)
        r.y = int(r.y * scalar)
        return r

    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    def angle(self) -> float:
        return math.atan2(self.y, self.x)

class Box2:
    def __init__(
        self,
        pos_proto: Optional[types.Vector2] = None,
        size_proto: Optional[types.Vector2] = None,
    ):
        self._pos_proto = types.Vector2()
        self._size_proto = types.Vector2()

        if pos_proto is not None:
            self._pos_proto.CopyFrom(pos_proto)

        if size_proto is not None:
            self._size_proto.CopyFrom(size_proto)

    @classmethod
    def from_xywh(cls, x_nm: int, y_nm: int, w_nm: int, h_nm: int):
        pos = Vector2.from_xy(x_nm, y_nm)
        size = Vector2.from_xy(w_nm, h_nm)
        return cls(pos._proto, size._proto)

    @classmethod
    def from_pos_size(cls, pos: Vector2, size: Vector2):
        return cls(pos._proto, size._proto)

    @property
    def pos(self) -> Vector2:
        return Vector2(self._pos_proto)

    @property
    def size(self) -> Vector2:
        return Vector2(self._size_proto)

    def merge(self, other: Union[Vector2, Box2]):
        if isinstance(other, Vector2):
            min_x = min(self.pos.x, other.x)
            min_y = min(self.pos.y, other.y)
            max_x = max(self.pos.x + self.size.x, other.x)
            max_y = max(self.pos.y + self.size.y, other.y)
        else:
            min_x = min(self.pos.x, other.pos.x)
            min_y = min(self.pos.y, other.pos.y)
            max_x = max(self.pos.x + self.size.x, other.pos.x + other.size.x)
            max_y = max(self.pos.y + self.size.y, other.pos.y + other.size.y)

        self._pos_proto.x_nm = min_x
        self._pos_proto.y_nm = min_y
        self._size_proto.x_nm = max_x - min_x
        self._size_proto.y_nm = max_y - min_y

    def inflate(self, amount: int):
        new_width = self.size.x + amount
        new_height = self.size.y + amount
        self._pos_proto.x_nm -= (new_width - self.size.x) // 2
        self._pos_proto.y_nm -= (new_height - self.size.y) // 2
        self._size_proto.x_nm = new_width
        self._size_proto.y_nm = new_height
