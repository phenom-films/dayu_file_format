#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import pytest
from dayu_file_format.curve.base import *


class TestCurve(object):
    def test_add(self):
        c = Curve()
        with pytest.raises(ValueError) as e:
            c.add(1)

        k1 = KeyFrame(Point2D(0, 0))
        k2 = KeyFrame(Point2D(1, 3))
        c.add(k1)
        c.add(k2)
        assert c[0] == k1
        assert c[1] == k2

        c.clear()
        c.add(k2)
        c.add(k1)
        assert c[0] == k1
        assert c[1] == k2

    def test_extend(self):
        k1 = KeyFrame(Point2D(0, 0))
        k2 = KeyFrame(Point2D(3, 2))
        k3 = KeyFrame(Point2D(2, 5))
        k4 = KeyFrame(Point2D(9, 1))
        k5 = KeyFrame(Point2D(6, 2))
        c = Curve()
        with pytest.raises(ValueError) as e:
            c.extend(12)
        with pytest.raises(ValueError) as e:
            c.extend([1, 2, 3])
        with pytest.raises(ValueError) as e:
            c.extend('123123')

        c.extend([k1, k2, k3, k4, k5])
        assert c[0] == k1
        assert c[1] == k3
        assert c[2] == k2
        assert c[3] == k5
        assert c[4] == k4

    def test_pop(self):
        k1 = KeyFrame(Point2D(0, 0))
        k2 = KeyFrame(Point2D(2, 2))
        k3 = KeyFrame(Point2D(3, 5))
        k4 = KeyFrame(Point2D(4, 1))
        k5 = KeyFrame(Point2D(5, 2))
        c = Curve()
        c.extend([k1, k2, k3, k4, k5])

        assert k5 == c.pop()
        assert len(c) == 4
        assert k2 == c.pop(1)
        assert len(c) == 3

    def test_duration(self):
        k1 = KeyFrame(Point2D(0, 0))
        k2 = KeyFrame(Point2D(2, 2))
        k3 = KeyFrame(Point2D(3, 5))
        k4 = KeyFrame(Point2D(4, 1))
        k5 = KeyFrame(Point2D(5, 2))
        c = Curve()
        c.extend([k1, k2, k3, k4, k5])

        assert c.duration == 5
        c.clear()
        assert c.duration == 0

    def test_remove(self):
        k1 = KeyFrame(Point2D(0, 0))
        k2 = KeyFrame(Point2D(2, 2))
        k3 = KeyFrame(Point2D(3, 5))
        k4 = KeyFrame(Point2D(4, 1))
        k5 = KeyFrame(Point2D(5, 2))
        k6 = KeyFrame(Point2D(7, 2))
        c = Curve()
        c.extend([k1, k2, k3, k4, k5])

        c.remove(k2)
        assert len(c) == 4

        with pytest.raises(ValueError) as e:
            c.remove(k6)

    def test_find_nearest_keyframe(self):
        k1 = KeyFrame(Point2D(0, 0))
        k2 = KeyFrame(Point2D(2, 2))
        k3 = KeyFrame(Point2D(3, 5))
        k4 = KeyFrame(Point2D(4, 1))
        k5 = KeyFrame(Point2D(5, 2))
        c = Curve()
        c.extend([k1, k2, k3, k4, k5])

        assert k1 == c.find_nearest_keyframe(-2)
        assert k1 == c.find_nearest_keyframe(0)
        assert k2 == c.find_nearest_keyframe(1.8)
        assert k2 == c.find_nearest_keyframe(2.2)
        assert k3 == c.find_nearest_keyframe(2.7)
        assert k5 == c.find_nearest_keyframe(5)
        assert k5 == c.find_nearest_keyframe(20)

    def test_clear(self):
        k1 = KeyFrame(Point2D(0, 0))
        k2 = KeyFrame(Point2D(2, 2))
        k3 = KeyFrame(Point2D(3, 5))
        k4 = KeyFrame(Point2D(4, 1))
        k5 = KeyFrame(Point2D(5, 2))
        c = Curve()
        c.extend([k1, k2, k3, k4, k5])

        assert c.clear() is True
        assert c.extra_data == {}
        assert c._keyframes == []
