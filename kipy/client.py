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

import pynng
from result import Ok, Err

from google.protobuf.message import Message

from .common.envelope_pb2 import ApiRequest, ApiResponse, ApiResponseStatus, ApiStatusCode

class KiCadClient:
    def __init__(self, socket_path: str):
        self._socket_path = socket_path
        self._connect()

    def _connect(self):
        self._conn = pynng.Req0(dial=self._socket_path, send_timeout=1000, recv_timeout=1000)

    def send(self, command: Message, response_type: type):
        envelope = ApiRequest()
        envelope.message.Pack(command)

        try:
            self._conn.send(envelope.SerializeToString())
        except pynng.exceptions.Timeout:
            raise IOError("Timeout while sending command to KiCad")
        except pynng.exceptions.NNGException as e:
            raise e

        reply_data = self._conn.recv_msg()
        reply = ApiResponse()
        reply.ParseFromString(reply_data.bytes)

        if reply.status.status == ApiStatusCode.AS_OK:
            response = response_type()
            reply.message.Unpack(response)
            return Ok(response)
        else:
            return Err("KiCad returned error: {}", reply.status.error_message)
