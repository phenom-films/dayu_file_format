#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import pytest
from dayu_file_format.curve.data_structure import KeyFrame, Point2D


class TestKeyFrame(object):
    def test___init__(self):
        with pytest.raises(ValueError) as e:
            KeyFrame(1, 2, 3)

    def test___eq__(self):
        assert KeyFrame(Point2D(0, 0), Point2D(-1, -1), Point2D(1, 1)) == KeyFrame(Point2D(0, 0), Point2D(-1, -1),
                                                                                   Point2D(1, 1))
        assert KeyFrame(Point2D(0, 0), Point2D(-1, -1), Point2D(1, 1)) != KeyFrame(Point2D(0, 1), Point2D(-1, -1),
                                                                                   Point2D(1, 1))
        assert KeyFrame(Point2D(0, 0), Point2D(-1, -1), Point2D(1, 1)) != KeyFrame(Point2D(0, 0), Point2D(-2, -1),
                                                                                   Point2D(1, 1))
        assert KeyFrame(Point2D(0, 0), Point2D(-1, -1), Point2D(1, 1)) != KeyFrame(Point2D(0, 0), Point2D(-1, -1),
                                                                                   Point2D(-1, 1))
        assert KeyFrame(Point2D(0, 0), Point2D(-1, -1), Point2D(1, 1)) != KeyFrame(Point2D(0, 1), Point2D(-4, -1),
                                                                                   Point2D(2, 1))
        assert KeyFrame(Point2D(0, 0), Point2D(-1, -1), Point2D(1, 1)) != [1, 2, 3]

    def test_left_tangent(self):
        assert KeyFrame(Point2D(0, 0), Point2D(-1, -1), Point2D(1, 1)).left_tangent == 1
        assert KeyFrame(Point2D(0, 0), Point2D(-1, 2), Point2D(1, 1)).left_tangent == -2
        assert KeyFrame(Point2D(0, 0), Point2D(0, 0), Point2D(1, 1)).left_tangent == 1e8

    def test_right_tangent(self):
        assert KeyFrame(Point2D(0, 0), Point2D(-1, -1), Point2D(1, 1)).right_tangent == 1
        assert KeyFrame(Point2D(0, 0), Point2D(-1, -1), Point2D(1, -2)).right_tangent == -2
        assert KeyFrame(Point2D(0, 0), Point2D(-1, -1), Point2D(0, 1)).right_tangent == 1e8

    def test_to_list(self):
        assert KeyFrame(Point2D(0, 0), Point2D(-1, -1), Point2D(1, 1)).to_list() == [[0, 0], [-1, -1], [1, 1]]
