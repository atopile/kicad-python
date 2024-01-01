#!/usr/bin/env python3

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

from PyQt6.QtWidgets import *

from random import randrange

from kipy.common.commands import (
    refresh_editor,
    begin_commit,
    end_commit
)
from kipy.board.commands import get_tracks, create_track, update_track
from kipy.board.types.track_pb2 import TRACK
from kipy.common.types.frame_type_pb2 import FRAME_TYPE
from kipy.util import from_mm
from kipy.enums import PCB_LAYER_ID

def create_some_tracks():
    begin_commit()

    for i in range(5):
        t = TRACK()
        t.start_x = from_mm(randrange(1, 100))
        t.start_y = from_mm(randrange(1, 100))
        t.end_x = from_mm(randrange(1, 100))
        t.end_y = from_mm(randrange(1, 100))
        t.width = from_mm(1.0)
        t.layer = PCB_LAYER_ID.F_Cu
        create_track(t)

    end_commit("Created some tracks")
    refresh_editor(FRAME_TYPE.FT_PCB_EDITOR)

def make_them_bigger():
    begin_commit()

    tracks = get_tracks()

    for track in tracks:
        track.width += from_mm(0.5)
        update_track(track)

    end_commit("Changed all track widths by 0.5mm")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("KiCad Python Example")
        btn1 = QPushButton("Create some tracks")
        btn2 = QPushButton("Make them bigger")
        szr = QVBoxLayout()
        szr.addWidget(btn1)
        szr.addWidget(btn2)

        btn1.clicked.connect(create_some_tracks)
        btn2.clicked.connect(make_them_bigger)

        widget = QWidget()
        widget.setLayout(szr)
        self.setCentralWidget(widget)

if __name__=='__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()