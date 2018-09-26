#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from dayu_file_format.curve.data_structure import Point2D
import pytest


class TestPoint2D(object):
    def test___init__(self):
        p = Point2D(0, 1)
        assert p.x == 0
        assert p.y == 1
        assert type(p.x) is float
        assert type(p.y) is float
        p = Point2D(0.0, 0.0)
        assert p.x == 0
        assert p.y == 0
        assert type(p.x) is float
        assert type(p.y) is float
        with pytest.raises(ValueError) as e:
            Point2D('12', 12)

    def test___eq__(self):
        assert Point2D(100, 100) == Point2D(100, 100)
        assert Point2D(100, 100) == Point2D(100.0, 100.0)
        assert Point2D(100.0, 100.9) != Point2D(100.0, 100.0)
        assert Point2D(0,0) != [0,0]

    def test___add__(self):
        assert Point2D(0, 0) + Point2D(1, 2) == Point2D(1, 2)
        assert Point2D(1, 1) + 2 == Point2D(3, 3)
        assert Point2D(1, 1) + 2.0 == Point2D(3, 3)
        assert Point2D(1, 1) + (-2.0) == Point2D(-1, -1)
        with pytest.raises(TypeError) as e:
            Point2D(1, 1) + [1, 2]

    def test___iadd__(self):
        p = Point2D(0, 0)
        p += 1
        assert p == Point2D(1, 1)
        p += Point2D(2, 3)
        assert p == Point2D(3, 4)
        p += (-4.0)
        assert p == Point2D(-1, 0)
        with pytest.raises(TypeError) as e:
            p += [1, 2]

    def test___sub__(self):
        assert Point2D(0, 0) - Point2D(1, 2) == Point2D(-1, -2)
        assert Point2D(1, 1) - 2 == Point2D(-1, -1)
        assert Point2D(1, 1) - 2.0 == Point2D(-1, -1)
        assert Point2D(1, 1) - (-2.0) == Point2D(3, 3)
        with pytest.raises(TypeError) as e:
            Point2D(1, 1) - [1, 2]

    def test___isub__(self):
        p = Point2D(0, 0)
        p -= 1
        assert p == Point2D(-1, -1)
        p -= Point2D(2, 3)
        assert p == Point2D(-3, -4)
        p -= (-4.0)
        assert p == Point2D(1, 0)
        with pytest.raises(TypeError) as e:
            p -= [1, 2]

    def test___neg__(self):
        assert -Point2D(1, 1) == Point2D(-1, -1)
        assert -Point2D(-3, 4) == Point2D(3, -4)
        assert -Point2D(0, 0) == Point2D(0, 0)

    def test___mul__(self):
        assert Point2D(0, 0) * Point2D(1, 2) == Point2D(0, 0)
        assert Point2D(1, 1) * 2 == Point2D(2, 2)
        assert Point2D(1, 1) * 2.0 == Point2D(2, 2)
        assert Point2D(1, 1) * (-2.0) == Point2D(-2, -2)
        with pytest.raises(TypeError) as e:
            Point2D(1, 1) * [1, 2]

    def test___imul__(self):
        p = Point2D(1, 2)
        p *= 1
        assert p == Point2D(1, 2)
        p *= Point2D(2, 3)
        assert p == Point2D(2, 6)
        p *= (-4.0)
        assert p == Point2D(-8, -24)
        with pytest.raises(TypeError) as e:
            p *= [1, 2]

    def test___div__(self):
        assert Point2D(0, 0) / Point2D(1, 2) == Point2D(0, 0)
        assert Point2D(1, 1) / 2 == Point2D(0.5, 0.5)
        assert Point2D(1, 1) / 2.0 == Point2D(0.5, 0.5)
        assert Point2D(1, 1) / (-2.0) == Point2D(-0.5, -0.5)
        with pytest.raises(TypeError) as e:
            Point2D(1, 1) / [1, 2]

        with pytest.raises(ZeroDivisionError) as e:
            Point2D(100, 24) / 0
        with pytest.raises(ZeroDivisionError) as e:
            Point2D(100, 24) / Point2D(0, 2)
        with pytest.raises(ZeroDivisionError) as e:
            Point2D(100, 24) / Point2D(2, 0)
        with pytest.raises(ZeroDivisionError) as e:
            Point2D(100, 24) / Point2D(0, 0)

    def test___idiv__(self):
        p = Point2D(1, 2)
        p /= 1
        assert p == Point2D(1, 2)
        p /= Point2D(2, 4)
        assert p == Point2D(0.5, 0.5)
        p /= (-0.25)
        assert p == Point2D(-2, -2)
        with pytest.raises(TypeError) as e:
            p /= [1, 2]

        with pytest.raises(ZeroDivisionError) as e:
            p /= 0
        with pytest.raises(ZeroDivisionError) as e:
            p /= Point2D(0, 2)
        with pytest.raises(ZeroDivisionError) as e:
            p /= Point2D(2, 0)
        with pytest.raises(ZeroDivisionError) as e:
            p /= Point2D(0, 0)

    def test_dot(self):
        assert Point2D(0, 0).dot(Point2D(1, 2)) == 0
        assert Point2D(0, 0).dot(Point2D(0, 0)) == 0
        assert Point2D(1, 3).dot(Point2D(1, 2)) == 7
        assert Point2D(-2, -3).dot(Point2D(1, 2)) == -8
        assert Point2D(-2, -3).dot(Point2D(-1, -2)) == 8
        assert Point2D(-2, 3).dot(Point2D(1, -2)) == -8
        with pytest.raises(TypeError) as e:
            Point2D(1, 2).dot([1, 2])

    def test_length(self):
        assert Point2D(0, 0).length == 0
        assert Point2D(1, 2).length == 5 ** 0.5
        assert Point2D(3, 4).length == 5
        assert Point2D(-3, 4).length == 5
        assert Point2D(-3, -4).length == 5

    def test_normalize(self):
        assert Point2D(1, 0).normalize() == Point2D(1, 0)
        assert Point2D(1, 1).normalize() == Point2D(1 / 2 ** 0.5, 1 / 2 ** 0.5)
        assert Point2D(-1, 1).normalize() == Point2D(-1 / 2 ** 0.5, 1 / 2 ** 0.5)
        assert Point2D(-1, -1).normalize() == Point2D(-1 / 2 ** 0.5, -1 / 2 ** 0.5)

    def test_to_list(self):
        assert Point2D(0, 0).to_list() == [0, 0]
        assert Point2D(1, 1).to_list() == [1, 1]
        assert Point2D(-1, 1).to_list() == [-1, 1]
