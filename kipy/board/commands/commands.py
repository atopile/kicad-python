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

from ... import _client
from .board_management_pb2 import *
from .board_objects_pb2 import *

def get_tracks():
    r = TRACKS_RESPONSE()
    if _client.send(GET_TRACKS(), r):
        return r.tracks
    raise IOError

def create_track(track):
    reply = TRACK_RESPONSE()
    request = CREATE_TRACK()
    request.track.CopyFrom(track)
    if _client.send(request, reply):
        return reply.track
    raise IOError

def update_track(track):
    reply = TRACK_RESPONSE()
    request = UPDATE_TRACK()
    request.id.value = track.id.value
    request.track.CopyFrom(track)
    if _client.send(request, reply):
        return reply.track
    raise IOError