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

import platform
import pynng

from google.protobuf.message import Message

from .common.envelope_pb2 import API_REQUEST, API_RESPONSE
from .common.types.api_status_pb2 import API_STATUS


class KiCadClient:
    def __init__(self):
        self._connect()

    def _connect(self):
        uri = 'ipc://\\.\\pipe\\kicad' if platform.system() == 'Windows' else 'ipc:///tmp/kicad.sock'
        try:
            self._conn = pynng.Req0(dial=uri, send_timeout=1000, recv_timeout=1000)
        except pynng.exceptions.NNGException:
            self._conn = None

    def send(self, command: Message, response: Message = None):
        if self._conn is None:
            self._connect()
        
        envelope = API_REQUEST()
        envelope.message.Pack(command)

        try:
            self._conn.send(envelope.SerializeToString())
        except pynng.exceptions.Timeout:
            raise IOError("Timeout while sending command to KiCad")
        except pynng.exceptions.NNGException as e:
            raise e

        reply_data = self._conn.recv_msg()
        reply = API_RESPONSE()
        reply.ParseFromString(reply_data.bytes)

        if reply.status == API_STATUS.AS_OK:
            if response is not None:
                reply.message.Unpack(response)
            return True
        else:
            return False

