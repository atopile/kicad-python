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

import os
import platform
import random
import string
from typing import List

from result import Ok, Err

from kipy.board import Board
from kipy.client import KiCadClient, ApiError
from kipy.proto.common import commands
from kipy.proto.common.types import DocumentType, DocumentSpecifier

def default_socket_path() -> str:
    path = os.environ.get('KICAD_API_SOCKET')
    if path is not None:
        return path
    return 'ipc://\\.\\pipe\\kicad' if platform.system() == 'Windows' else 'ipc:///tmp/kicad/api.sock'

def random_client_name() -> str:
    return 'anonymous-'+''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def default_kicad_token() -> str:
    token = os.environ.get('KICAD_API_TOKEN')
    if token is not None:
        return token
    return ""

class KiCad:
    def __init__(self, socket_path: str=default_socket_path(),
                 client_name: str=random_client_name(),
                 kicad_token: str=default_kicad_token()):
        self._client = KiCadClient(socket_path, client_name, kicad_token)
        
    def get_version(self):
        """Returns the KiCad version as a string, including any package-specific info"""
        match self._client.send(commands.GetVersion(), commands.GetVersionResponse):
            case Ok(response):
                return response.version.full_version
            case Err(e):
                raise ApiError(e)

    def run_action(self, action: str):
        """Runs a KiCad tool action, if it is available

        WARNING: This is an unstable API and is not intended for use other
        than by API developers. KiCad does not guarantee the stability of
        action names, and running actions may have unintended side effects.
        :param action: the name of a KiCad TOOL_ACTION
        :return: a value from the KIAPI.COMMON.COMMANDS.RUN_ACTION_STATUS enum
        """
        match self._client.send(commands.RunAction(), commands.RunActionResponse):
            case Ok(response):
                return response.status
            case Err(e):
                raise ApiError(e)

    def get_open_documents(self, doc_type: DocumentType) -> List[DocumentSpecifier]:
        """Retrieves a list of open documents matching the given type"""
        command = commands.GetOpenDocuments()
        command.type = doc_type
        match self._client.send(command, commands.GetOpenDocumentsResponse):
            case Ok(response):
                return response.documents
            case Err(e):
                raise ApiError(e)
            
    def get_board(self) -> Board:
        """Retrieves an open board"""
        docs = self.get_open_documents(DocumentType.DOCTYPE_PCB)
        if len(docs) == 0:
            raise ApiError("Expected to be able to retrieve at least one board")
        return Board(self._client, docs[0])
