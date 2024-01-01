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
from .editor_commands_pb2 import REFRESH_EDITOR
from .get_version_pb2 import GET_VERSION, GET_VERSION_RESPONSE
from .run_action_pb2 import RUN_ACTION, RUN_ACTION_RESPONSE
from .commit_pb2 import BEGIN_COMMIT, END_COMMIT

def get_version():
    """
    :return: the KiCad version as a string, including any package-specific info
    """
    r = GET_VERSION_RESPONSE()
    if _client.send(GET_VERSION(), r):
        return r.version.full_version
    raise IOError

def run_action(action: str):
    """
    Runs a KiCad tool action, if it is available.
    WARNING: This is an unstable API and is not intended for use other than by API developers.
    KiCad does not guarantee the stability of action names, and running actions may have unintended
    side effects.
    :param action: the name of a KiCad TOOL_ACTION
    :return: a value from the KIAPI.COMMON.COMMANDS.RUN_ACTION_STATUS enum
    """
    r = RUN_ACTION_RESPONSE()
    if _client.send(RUN_ACTION(), r):
        return r.status
    raise IOError

def refresh_editor(editor):
    r = REFRESH_EDITOR()
    r.frame = editor
    if _client.send(r, None):
        return
    raise IOError

def begin_commit():
    _client.send(BEGIN_COMMIT())

def end_commit(message: str):
    m = END_COMMIT()
    m.message = message;
    _client.send(m)
