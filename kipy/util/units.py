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

def from_mm(mm):
    """
    KiCad uses several internal unit systems, but for the IPC API, all distance units are defined as
    64-bit nanometers
    :param mm: a quantity in millimeters
    :return: the quantity in KiCad API units
    """
    return int(mm * 1_000_000)

def to_mm(iu):
    """
    See from_mm
    """
    return float(iu) / 1_000_000