# Copyright The KiCad Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pytest
from kipy.geometry import Box2, Vector2, arc_center

def test_arc_center_circle():
    start = Vector2.from_xy(0, 0)
    mid = Vector2.from_xy(1, 1)
    end = Vector2.from_xy(0, 0)
    center = arc_center(start, mid, end)
    assert center == (start + mid) * 0.5

def test_arc_center_collinear():
    start = Vector2.from_xy(0, 0)
    mid = Vector2.from_xy(1, 1)
    end = Vector2.from_xy(2, 2)
    center = arc_center(start, mid, end)
    assert center is None

def test_arc_center_normal_case():
    start = Vector2.from_xy(1000, 0)
    mid = Vector2.from_xy(1500, 1000)
    end = Vector2.from_xy(1000, 2000)
    center = arc_center(start, mid, end)
    assert center is not None
    assert center.x == pytest.approx(250, rel=1e-2)
    assert center.y == pytest.approx(1000, rel=1e-2)

def test_arc_center_another_case():
    start = Vector2.from_xy(1000, 0)
    mid = Vector2.from_xy(0, 1000)
    end = Vector2.from_xy(-1000, 0)
    center = arc_center(start, mid, end)
    assert center is not None
    assert center.x == pytest.approx(0, rel=1e-2)
    assert center.y == pytest.approx(0, rel=1e-2)

def test_box2_merge():
    box1 = Box2.from_pos_size(Vector2.from_xy(0, 0), Vector2.from_xy(1000, 1000))
    box2 = Box2.from_pos_size(Vector2.from_xy(2000, 2000), Vector2.from_xy(1000, 1000))
    box1.merge(box2)
    assert box1.pos == Vector2.from_xy(0, 0)
    assert box1.size == Vector2.from_xy(3000, 3000)

def test_box2_inflate():
    box = Box2.from_pos_size(Vector2.from_xy(1000, 1000), Vector2.from_xy(1000, 1000))
    box.inflate(1000)
    assert box.pos == Vector2.from_xy(500, 500)
    assert box.size == Vector2.from_xy(2000, 2000)

def test_box2_inflate_negative():
    box = Box2.from_pos_size(Vector2.from_xy(1000, 1000), Vector2.from_xy(2000, 2000))
    box.inflate(-1000)
    assert box.pos == Vector2.from_xy(1500, 1500)
    assert box.size == Vector2.from_xy(1000, 1000)
