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
from typing import TypeVar, cast

from google.protobuf.message import Message

from kipy.proto.common import ApiRequest, ApiResponse, ApiStatusCode

class ApiError(Exception):
    pass

class KiCadClient:
    def __init__(self, socket_path: str, client_name: str, kicad_token: str):
        self._socket_path = socket_path
        self._client_name = client_name
        self._kicad_token = kicad_token
        self._connect()

    def _connect(self):
        self._conn = pynng.Req0(dial=self._socket_path, send_timeout=3000, recv_timeout=3000)

    R = TypeVar('R', bound=Message)

    def send(self, command: Message, response_type: type[R]) -> R:
        envelope = ApiRequest()
        envelope.message.Pack(command)
        envelope.header.kicad_token = self._kicad_token
        envelope.header.client_name = self._client_name

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
            
            if not reply.message.Unpack(response):
                raise ApiError(
                    f"Failed to unpack {response_type.__name__} from the response to {type(command).__name__}"
                )

            if self._kicad_token == "":
                self._kicad_token = reply.header.kicad_token

            return cast(response_type, response)
        else:
            raise ApiError("KiCad returned error: {}".format(reply.status.error_message))
