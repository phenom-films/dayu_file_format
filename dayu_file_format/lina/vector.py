#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from numbers import Number
from deco import data_type_validation


class Vec2f(object):
    __slots__ = ['x', 'y']

    @data_type_validation(x=Number, y=Number)
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        if isinstance(other, Vec2f):
            return Vec2f(self.x + other.x, self.y + other.y)
        if isinstance(other, Number):
            return Vec2f(self.x + other, self.y + other)
        raise TypeError()

    @data_type_validation(other=Number)
    def __radd__(self, other):
        return Vec2f(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vec2f):
            return Vec2f(self.x - other.x, self.y - other.y)
        if isinstance(other, Number):
            return Vec2f(self.x - other, self.y - other)
        raise TypeError()

    @data_type_validation(other=Number)
    def __rsub__(self, other):
        return Vec2f(other - self.x, other.self.y)

    def __mul__(self, other):
        if isinstance(other, Vec2f):
            return Vec2f(self.x * other.x, self.y * other.y)
        if isinstance(other, Number):
            return Vec2f(self.x * other, self.y * other)
        raise TypeError()

    @data_type_validation(other=Number)
    def __radd__(self, other):
        return Vec2f(self.x * other, self.y * other)

    def __div__(self, other):
        if isinstance(other, Vec2f):
            return Vec2f(self.x / other.x, self.y / other.y)
        if isinstance(other, Number):
            return Vec2f(self.x / other, self.y / other)
        raise TypeError()

    def __neg__(self):
        return self * (-1)

    @data_type_validation(index=int)
    def __getitem__(self, index):
        mapping = {0: 'x', 1: 'y'}
        return getattr(self, mapping[index], None)

    @data_type_validation(index=int, value=Number)
    def __setitem__(self, index, value):
        mapping = {0: 'x', 1: 'y'}
        setattr(self, mapping[index], value)

    def __repr__(self):
        return '<Vec2f>({}, {})'.format(self.x, self.y)

    def dot(self, other):
        if isinstance(other, Vec2f):
            return self.x * other.x + self.y * other.y
        raise TypeError()

    @property
    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    @property
    def length2(self):
        return self.x ** 2 + self.y ** 2

    def normalize(self):
        _length = self.length
        return Vec3f(self.x / _length, self.y / _length)


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

    @data_type_validation(other=Number)
    def __radd__(self, other):
        return Vec3f(self.x + other, self.y + other, self.z + other)

    def __sub__(self, other):
        if isinstance(other, Vec3f):
            return Vec3f(self.x - other.x, self.y - other.y, self.z - other.z)
        if isinstance(other, Number):
            return Vec3f(self.x - other, self.y - other, self.z - other)
        raise TypeError()

    @data_type_validation(other=Number)
    def __rsub__(self, other):
        return Vec3f(other - self.x, other - self.y, other - self.z)

    def __mul__(self, other):
        if isinstance(other, Vec3f):
            return Vec3f(self.x * other.x, self.y * other.y, self.z * other.z)
        if isinstance(other, Number):
            return Vec3f(self.x * other, self.y * other, self.z * other)
        raise TypeError()

    @data_type_validation(other=Number)
    def __rmul__(self, other):
        return Vec3f(self.x * other, self.y * other, self.z * other)

    def __div__(self, other):
        if isinstance(other, Vec3f):
            return Vec3f(self.x / other.x, self.y / other.y, self.z / other.z)
        if isinstance(other, Number):
            return Vec3f(self.x / other, self.y / other, self.z / other)
        raise TypeError()

    def __neg__(self):
        return self * (-1)

    @data_type_validation(index=int)
    def __getitem__(self, index):
        mapping = {0: 'x', 1: 'y', 2: 'z'}
        return getattr(self, mapping[index], None)

    @data_type_validation(index=int, value=Number)
    def __setitem__(self, index, value):
        mapping = {0: 'x', 1: 'y', 2: 'z'}
        setattr(self, mapping[index], value)

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


class Vec4f(object):
    __slots__ = ['x', 'y', 'z', 'w']

    @data_type_validation(x=Number, y=Number, z=Number, w=Number)
    def __init__(self, x, y, z, w):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)

    def __add__(self, other):
        if isinstance(other, Vec4f):
            return Vec4f(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)
        if isinstance(other, Number):
            return Vec4f(self.x + other, self.y + other, self.z + other, self.w + other)
        raise TypeError()

    @data_type_validation(other=Number)
    def __radd__(self, other):
        return Vec4f(self.x + other, self.y + other, self.z + other, self.w + other)

    def __sub__(self, other):
        if isinstance(other, Vec4f):
            return Vec4f(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)
        if isinstance(other, Number):
            return Vec4f(self.x - other, self.y - other, self.z - other, self.w - other)
        raise TypeError()

    @data_type_validation(other=Number)
    def __rsub__(self, other):
        return Vec4f(other - self.x, other - self.y, other - self.z, other - self.w)

    def __mul__(self, other):
        if isinstance(other, Vec4f):
            return Vec4f(self.x * other.x, self.y * other.y, self.z * other.z, self.w * other.w)
        if isinstance(other, Number):
            return Vec4f(self.x * other, self.y * other, self.z * other, self.w * other)
        raise TypeError()

    @data_type_validation(other=Number)
    def __rmul__(self, other):
        return Vec4f(self.x * other, self.y * other, self.z * other, self.w * other)

    def __div__(self, other):
        if isinstance(other, Vec4f):
            return Vec4f(self.x / other.x, self.y / other.y, self.z / other.z, self.w / other.w)
        if isinstance(other, Number):
            return Vec4f(self.x / other, self.y / other, self.z / other, self.w / other)
        raise TypeError()

    def __neg__(self):
        return self * (-1)

    @data_type_validation(index=int)
    def __getitem__(self, index):
        mapping = {0: 'x', 1: 'y', 2: 'z', 3: 'w'}
        return getattr(self, mapping[index], None)

    @data_type_validation(index=int, value=Number)
    def __setitem__(self, index, value):
        mapping = {0: 'x', 1: 'y', 2: 'z', 3: 'w'}
        setattr(self, mapping[index], value)

    def __repr__(self):
        return '<Vec3f>({}, {}, {})'.format(self.x, self.y, self.z)

    def dot(self, other):
        if isinstance(other, Vec4f):
            return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w
        raise TypeError()

    @property
    def length(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w ** 2) ** 0.5

    @property
    def length2(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w ** 2

    def normalize(self):
        _length = self.length
        return Vec4f(self.x / _length, self.y / _length, self.z / _length, self.w / _length)

    def cross(self, other):
        if isinstance(other, Vec3f):
            x = self.y * other.z - self.z * other.y
            y = self.z * other.x - self.x * other.z
            z = self.x * other.y - self.y * other.x
            return Vec3f(x, y, z)
        raise TypeError()
