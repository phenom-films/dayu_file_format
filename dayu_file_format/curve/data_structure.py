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
        self.x = float(x)
        self.y = float(y)

    def __eq__(self, other):
        if isinstance(other, Point2D):
            return round(self.x - other.x, 7) == 0 and round(self.y - other.y, 7) == 0
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if isinstance(other, Number):
            return Point2D(self.x + other, self.y + other)
        if isinstance(other, Point2D):
            return Point2D(self.x + other.x, self.y + other.y)
        raise TypeError('Point2D cannot add with {}'.format(type(other)))

    def __iadd__(self, other):
        if isinstance(other, Number):
            self.x += other
            self.y += other
            return self
        if isinstance(other, Point2D):
            self.x += other.x
            self.y += other.y
            return self
        raise TypeError('Point2D cannot add with {}'.format(type(other)))

    def __sub__(self, other):
        if isinstance(other, Number):
            return Point2D(self.x - other, self.y - other)
        if isinstance(other, Point2D):
            return Point2D(self.x - other.x, self.y - other.y)
        raise TypeError('Point2D cannot sub with {}'.format(type(other)))

    def __isub__(self, other):
        if isinstance(other, Number):
            self.x -= other
            self.y -= other
            return self
        if isinstance(other, Point2D):
            self.x -= other.x
            self.y -= other.y
            return self
        raise TypeError('Point2D cannot sub with {}'.format(type(other)))

    def __neg__(self):
        return Point2D(-self.x, -self.y)

    def __mul__(self, other):
        if isinstance(other, Number):
            return Point2D(self.x * other, self.y * other)
        if isinstance(other, Point2D):
            return Point2D(self.x * other.x, self.y * other.y)
        raise TypeError('Point2D cannot multiply with {}'.format(type(other)))

    def __imul__(self, other):
        if isinstance(other, Number):
            self.x *= other
            self.y *= other
            return self
        if isinstance(other, Point2D):
            self.x *= other.x
            self.y *= other.y
            return self
        raise TypeError('Point2D cannot multiply with {}'.format(type(other)))

    def __div__(self, other):
        if isinstance(other, Number):
            return Point2D(self.x / other, self.y / other)
        if isinstance(other, Point2D):
            return Point2D(self.x / other.x, self.y / other.y)
        raise TypeError('Point2D cannot divide with {}'.format(type(other)))

    def __idiv__(self, other):
        if isinstance(other, Number):
            self.x /= other
            self.y /= other
            return self
        if isinstance(other, Point2D):
            self.x /= other.x
            self.y /= other.y
            return self
        raise TypeError('Point2D cannot divide with {}'.format(type(other)))

    def dot(self, other):
        if isinstance(other, Point2D):
            return self.x * other.x + self.y * other.y
        raise TypeError('Point2D cannot dot with {}'.format(type(other)))

    @property
    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def normalize(self):
        _length = self.length
        return Point2D(self.x / _length, self.y / _length)

    def to_list(self):
        return [self.x, self.y]

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
        return self.left.y / self.left.x

    @property
    def right_tangent(self):
        if round(self.right.x, 7) == 0:
            return 1e8
        return self.right.y / self.right.x

    def to_list(self):
        return [self.current.to_list(), self.left.to_list(), self.right.to_list()]

    def __eq__(self, other):
        if isinstance(other, KeyFrame):
            return self.current == other.current and self.left == other.left and self.right == other.right
        return False

    def __repr__(self):
        return '<KeyPoint>(current={}, left={}, right={})'.format(self.current, self.left, self.right)
