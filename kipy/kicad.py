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
import random
import string

from result import Ok, Err

from .client import KiCadClient
from .proto.common import commands

class ApiError(Exception):
    pass

def default_socket_path() -> str:
    return 'ipc://\\.\\pipe\\kicad' if platform.system() == 'Windows' else 'ipc:///tmp/kicad.sock'

def random_client_name() -> str:
    return 'anonymous-'+''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

class KiCad:
    def __init__(self, socket_path: str=default_socket_path(),
                 client_name: str=random_client_name(),
                 kicad_token: str=""):
        self._client = KiCadClient(socket_path, client_name, kicad_token)
        
    def get_version(self):
        """
        :return: the KiCad version as a string, including any package-specific info
        """
        match self._client.send(commands.GetVersion(), commands.GetVersionResponse):
            case Ok(response):
                return response.version.full_version
            case Err(e):
                raise ApiError(e)

    def run_action(self, action: str):
        """
        Runs a KiCad tool action, if it is available.
        WARNING: This is an unstable API and is not intended for use other than by API developers.
        KiCad does not guarantee the stability of action names, and running actions may have unintended
        side effects.
        :param action: the name of a KiCad TOOL_ACTION
        :return: a value from the KIAPI.COMMON.COMMANDS.RUN_ACTION_STATUS enum
        """
        r = commands.RunActionResponse()
        if self._client.send(commands.RunAction(), r):
            return r.status
        raise IOError

    def refresh_editor(self, editor):
        r = commands.RefreshEditor()
        r.frame = editor
        if self._client.send(r, None):
            return
        raise IOError

    def begin_commit(self):
        self._client.send(commands.BeginCommit())

    def end_commit(self, message: str):
        m = commands.EndCommit()
        m.message = message
        self._client.send(m)