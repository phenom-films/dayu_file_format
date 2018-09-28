#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from numbers import Number
from deco import data_type_validation


class Vec3f(object):
    __slots__ = ['x', 'y', 'z']

    @data_type_validation(x=Number, y=Number, z=Number)
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, other):
        if isinstance(other, Vec3f):
            return Vec3f(self.x + other.x, self.y + other.y, self.z + other.z)
        if isinstance(other, Number):
            return Vec3f(self.x + other, self.y + other, self.z + other)
        raise TypeError()

    def __sub__(self, other):
        if isinstance(other, Vec3f):
            return Vec3f(self.x - other.x, self.y - other.y, self.z - other.z)
        if isinstance(other, Number):
            return Vec3f(self.x - other, self.y - other, self.z - other)
        raise TypeError()

    def __mul__(self, other):
        if isinstance(other, Vec3f):
            return Vec3f(self.x * other.x, self.y * other.y, self.z * other.z)
        if isinstance(other, Number):
            return Vec3f(self.x * other, self.y * other, self.z * other)
        raise TypeError()

    def __div__(self, other):
        if isinstance(other, Vec3f):
            return Vec3f(self.x / other.x, self.y / other.y, self.z / other.z)
        if isinstance(other, Number):
            return Vec3f(self.x / other, self.y / other, self.z / other)
        raise TypeError()

    def __neg__(self):
        return self * (-1)

    data_type_validation(index=int)
    def __getitem__(self, index):
        if index > 2 or index < 0:
            raise IndexError('Vec3f out of range: {}'.format(index))
        mapping = {0: 'x', 1: 'y', 2: 'z'}
        return getattr(self, mapping[index], None)

    def __repr__(self):
        return '<Vec3f>({}, {}, {})'.format(self.x, self.y, self.z)

    def dot(self, other):
        if isinstance(other, Vec3f):
            return self.x * other.x + self.y * other.y + self.z * other.z
        raise TypeError()

    @property
    def length(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    @property
    def length2(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def normalize(self):
        _length = self.length
        return Vec3f(self.x / _length, self.y / _length, self.z / _length)

    def cross(self, other):
        if isinstance(other, Vec3f):
            x = self.y * other.z - self.z * other.y
            y = self.z * other.x - self.x * other.z
            z = self.x * other.y - self.y * other.x
            return Vec3f(x, y, z)
        raise TypeError()
