#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import inspect
from functools import wraps
from numbers import Number


def data_type_validation(**validation):
    def outter_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            call_args = inspect.getcallargs(func, *args, **kwargs)
            call_args.pop(inspect.getargspec(func).args[0], None)
            for k, v in call_args.items():
                if validation.has_key(k) and (not isinstance(v, validation.get(k))):
                    raise ValueError('{} except type: {}'.format(k, validation.get(k)))

            return func(*args, **kwargs)

        return wrapper

    return outter_wrapper


class Point2D(object):
    __slots__ = ['x', 'y']

    @data_type_validation(x=Number, y=Number)
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Point2D):
            return round(self.x - other.x, 7) == 0 and round(self.y == other.y, 7) == 0
        return False

    def __repr__(self):
        return '<Point2D>(x={}, y={})'.format(self.x, self.y)


class KeyFrame(object):
    __slots__ = ['current', 'left', 'right']

    @data_type_validation(current=Point2D, left=Point2D, right=Point2D)
    def __init__(self, current, left=Point2D(0, 0), right=Point2D(0, 0)):
        self.current = current
        self.left = left
        self.right = right

    @property
    def left_tangent(self):
        if round(self.left.x, 7) == 0:
            return 1e8
        return (self.left.y) / float(self.left.x)

    @property
    def right_tangent(self):
        if round(self.right.x, 7) == 0:
            return 1e8
        return (self.right.y) / float(self.right.x)

    @property
    def left_magnitude(self):
        return (self.left.x ** 2 + self.left.y ** 2) ** 0.5

    @property
    def right_magnitude(self):
        return (self.right.x ** 2 + self.right.y ** 2) ** 0.5

    def to_list(self):
        return [[self.current.x, self.current.y], [self.left.x, self.left.y], [self.right.x, self.right.y]]

    def __eq__(self, other):
        if isinstance(other, KeyFrame):
            return self.current == other.current and self.left == other.left and self.right == other.right
        return False

    def __repr__(self):
        return '<KeyPoint>(current={}, left={}, right={})'.format(self.current, self.left, self.right)
