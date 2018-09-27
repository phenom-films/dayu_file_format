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


class Vec3f(object):
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


class Quaternion(object):
    @data_type_validation(w=Number, x=Number, y=Number, z=Number)
    def __init__(self, w, x, y, z):
        self.w = float(w)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    @classmethod
    @data_type_validation(axis=Vec3f, angle=Number)
    def from_axis_angle(cls, axis, angle):
        import math
        sin_value = math.sin(angle)
        return cls(math.cos(angle), axis.x * sin_value, axis.y * sin_value, axis.z * sin_value)

    @classmethod
    @data_type_validation(rx=Number, ry=Number, rz=Number, order=str)
    def from_euler_angles(cls, rx, ry, rz, order='xyz'):
        import math

        if order == 'xyz':
            sin_1 = math.sin(math.radians(rz) / 2.0)
            sin_2 = math.sin(math.radians(ry) / 2.0)
            sin_3 = math.sin(math.radians(rx) / 2.0)
            cos_1 = math.cos(math.radians(rz) / 2.0)
            cos_2 = math.cos(math.radians(ry) / 2.0)
            cos_3 = math.cos(math.radians(rx) / 2.0)
            w = sin_1 * sin_2 * sin_3 + cos_1 * cos_2 * cos_3
            x = -sin_1 * sin_2 * cos_3 + sin_3 * cos_1 * cos_2
            y = sin_1 * sin_3 * cos_2 + sin_2 * cos_1 * cos_3
            z = sin_1 * cos_2 * cos_3 - sin_2 * sin_3 * cos_1
            return Quaternion(w, x, y, z)

        if order == 'xzy':
            sin_1 = math.sin(math.radians(ry) / 2.0)
            sin_2 = math.sin(math.radians(rz) / 2.0)
            sin_3 = math.sin(math.radians(rx) / 2.0)
            cos_1 = math.cos(math.radians(ry) / 2.0)
            cos_2 = math.cos(math.radians(rz) / 2.0)
            cos_3 = math.cos(math.radians(rx) / 2.0)
            w = -sin_1 * sin_2 * sin_3 + cos_1 * cos_2 * cos_3
            x = sin_1 * sin_2 * cos_3 + sin_3 * cos_1 * cos_2
            y = sin_1 * cos_2 * cos_3 + sin_2 * sin_3 * cos_1
            z = -sin_1 * sin_3 * cos_2 + sin_2 * cos_1 * cos_3
            return Quaternion(w, x, y, z)

        if order == 'yxz':
            sin_1 = math.sin(math.radians(rz) / 2.0)
            sin_2 = math.sin(math.radians(rx) / 2.0)
            sin_3 = math.sin(math.radians(ry) / 2.0)
            cos_1 = math.cos(math.radians(rz) / 2.0)
            cos_2 = math.cos(math.radians(rx) / 2.0)
            cos_3 = math.cos(math.radians(ry) / 2.0)
            w = -sin_1 * sin_2 * sin_3 + cos_1 * cos_2 * cos_3
            x = -sin_1 * sin_3 * cos_2 + sin_2 * cos_1 * cos_3
            y = sin_1 * sin_2 * cos_3 + sin_3 * cos_1 * cos_2
            z = sin_1 * cos_2 * cos_3 + sin_2 * sin_3 * cos_1
            return Quaternion(w, x, y, z)

        if order == 'yzx':
            sin_1 = math.sin(math.radians(rx) / 2.0)
            sin_2 = math.sin(math.radians(rz) / 2.0)
            sin_3 = math.sin(math.radians(ry) / 2.0)
            cos_1 = math.cos(math.radians(rx) / 2.0)
            cos_2 = math.cos(math.radians(rz) / 2.0)
            cos_3 = math.cos(math.radians(ry) / 2.0)
            w = sin_1 * sin_2 * sin_3 + cos_1 * cos_2 * cos_3
            x = sin_1 * cos_2 * cos_3 - sin_2 * sin_3 * cos_1
            y = -sin_1 * sin_2 * cos_3 + sin_3 * cos_1 * cos_2
            z = sin_1 * sin_3 * cos_2 + sin_2 * cos_1 * cos_3
            return Quaternion(w, x, y, z)

        if order == 'zxy':
            sin_1 = math.sin(math.radians(ry) / 2.0)
            sin_2 = math.sin(math.radians(rx) / 2.0)
            sin_3 = math.sin(math.radians(rz) / 2.0)
            cos_1 = math.cos(math.radians(ry) / 2.0)
            cos_2 = math.cos(math.radians(rx) / 2.0)
            cos_3 = math.cos(math.radians(rz) / 2.0)
            w = sin_1 * sin_2 * sin_3 + cos_1 * cos_2 * cos_3
            x = sin_1 * sin_3 * cos_2 + sin_2 * cos_1 * cos_3
            y = sin_1 * cos_2 * cos_3 - sin_2 * sin_3 * cos_1
            z = -sin_1 * sin_2 * cos_3 + sin_3 * cos_1 * cos_2
            return Quaternion(w, x, y, z)

        if order == 'zyx':
            sin_1 = math.sin(math.radians(rx) / 2.0)
            sin_2 = math.sin(math.radians(ry) / 2.0)
            sin_3 = math.sin(math.radians(rz) / 2.0)
            cos_1 = math.cos(math.radians(rx) / 2.0)
            cos_2 = math.cos(math.radians(ry) / 2.0)
            cos_3 = math.cos(math.radians(rz) / 2.0)
            w = -sin_1 * sin_2 * sin_3 + cos_1 * cos_2 * cos_3
            x = sin_1 * cos_2 * cos_3 + sin_2 * sin_3 * cos_1
            y = -sin_1 * sin_3 * cos_1 + sin_2 * cos_1 * cos_3
            z = sin_1 * sin_2 * cos_3 + sin_3 * cos_1 * cos_2
            return Quaternion(w, x, y, z)

    @property
    def real(self):
        return self.w

    @property
    def imagine(self):
        return Vec3f(self.x, self.y, self.z)

    def __repr__(self):
        return '<Quaternion>({}, {}, {}, {})'.format(self.w, self.x, self.y, self.z)

    def __add__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)
        raise TypeError()

    def __sub__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(self.w - other.w, self.x - other.x, self.y - other.y, self.z - other.z)
        raise TypeError()

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            real = self.w * other.w - self.imagine.dot(other.imagine)
            imagine = other.imagine * self.w + self.imagine * other.w + self.imagine.cross(other.imagine)
            return Quaternion(real, imagine.x, imagine.y, imagine.z)
        if isinstance(other, Number):
            return Quaternion(self.x * other, self.x * other, self.y * other, self.z * other)
        raise TypeError()

    def __div__(self, other):
        if isinstance(other, Number):
            return Quaternion(self.w / other, self.x / other, self.y / other, self.z / other)
        raise TypeError()

    def __neg__(self):
        return self * (-1)

    def normalize(self):
        return self / self.length

    @property
    def length(self):
        return (self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    @property
    def length2(self):
        return self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2

    @property
    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def inverse(self):
        return self.conjugate / self.length2

    @property
    def axis(self):
        denominator = (1.0 - self.w ** 2) ** 0.5
        return Vec3f(self.x / denominator, self.y / denominator, self.z / denominator).normalize()

    @property
    def radian(self):
        import math
        return math.acos(self.w) * 2.0

    def rotate(self, v):
        if isinstance(v, Vec3f):
            p = Quaternion(0, v.x, v.y, v.z)
            return (self * p * self.inverse()).imagine
        raise TypeError()

    data_type_validation(order=str)

    def euler_angles(self, order='xyz'):
        import math

        angle_1 = math.degrees(math.atan2(2.0 * (self.w * self.x + self.y * self.z),
                                          1.0 - 2.0 * (self.x ** 2 + self.y ** 2)))
        t2 = 2.0 * (self.w * self.y - self.z * self.x)
        t2 = max(min(t2, 1), -1)
        angle_2 = math.degrees(math.asin(t2))
        angle_3 = math.degrees(
                math.atan2(2.0 * (self.w * self.z + self.x * self.y), 1.0 - 2.0 * (self.y ** 2 + self.z ** 2)))
        return dict(zip(order.lower(), (angle_1, angle_2, angle_3)))


if __name__ == '__main__':
    order = 'zyx'
    aa = Quaternion.from_euler_angles(10, 20, 30, order=order)
    # print aa

    '''
    xyz = 0.951549,  0.0381346,	0.189308,	0.239298,	
    xzy = 0.943714,  0.127679,	0.189308,	0.239298,	
    yxz = 0.943714,  0.0381346,	0.189308,	0.268536,	
    yzx = 0.951549,  0.0381346,	0.144878,	0.268536,	
    zxy = 0.951549,  0.127679,	0.144878,	0.239298,	
    zyx = 0.943714,  0.127679,	0.144878,	0.268536,	
  

    '''

    # a = Quaternion(0.943714, 0.127679, 0.189308, 0.239298).normalize()
    # print a
    # print a.axis
    # print a.radian
    print aa.euler_angles(order=order)
    # print a.rotate(Vec3f(1, 0, 0))
