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

from typing import Optional
import math
from kipy.proto.common import types
from kipy.wrapper import Wrapper

class Vector2(Wrapper):
    """Wraps a kiapi.common.types.Vector2, aka VECTOR2I"""
    def __init__(self, proto: Optional[types.Vector2]):
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
    
    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

class Box2:
    def __init__(self, pos_proto: types.Vector2, size_proto: types.Vector2):
        self._pos_proto = pos_proto
        self._size_proto = size_proto

    @property
    def pos(self) -> Vector2:
        return Vector2(self._pos_proto)
    
    @property
    def size(self) -> Vector2:
        return Vector2(self._size_proto)