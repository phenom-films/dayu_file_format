#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from deco import data_type_validation
from numbers import Number
from vector import Vec2f, Vec3f, Vec4f


class MatrixBase(object):
    pass


class Matrix_22f(MatrixBase):
    dimension = (2, 2)

    @data_type_validation(a00=Number, a01=Number, a10=Number, a11=Number)
    def __init__(self, a00, a01, a10, a11):
        self.data = [Vec2f(a00, a01), Vec2f(a10, a11)]

    def __repr__(self):
        return '{:.06f}\t{:.06f}\n' \
               '{:.06f}\t{:.06f}\n'.format(self.data[0][0], self.data[0][1],
                                           self.data[1][0], self.data[1][1])

    @data_type_validation(index=int)
    def row(self, index):
        return Vec2f(self.data[index][0], self.data[index][1])

    @data_type_validation(index=int)
    def col(self, index):
        return Vec2f(self.data[0][index], self.data[1][index])

    @data_type_validation(index=int)
    def __getitem__(self, index):
        return self.data[index]

    def __add__(self, other):
        if isinstance(other, Matrix_22f):
            return Matrix_22f(self[0][0] + other[0][0], self[0][1] + other[0][1],
                              self[1][0] + other[1][0], self[1][1] + other[1][1])
        if isinstance(other, Number):
            return Matrix_22f(self[0][0] + other, self[0][1] + other,
                              self[1][0] + other, self[1][1] + other)

    @data_type_validation(other=Number)
    def __radd__(self, other):
        return Matrix_22f(self[0][0] + other, self[0][1] + other,
                          self[1][0] + other, self[1][1] + other)

    def __sub__(self, other):
        if isinstance(other, Matrix_33f):
            return Matrix_22f(self[0][0] - other[0][0], self[0][1] - other[0][1],
                              self[1][0] - other[1][0], self[1][1] - other[1][1])
        if isinstance(other, Number):
            return Matrix_22f(self[0][0] - other, self[0][1] - other,
                              self[1][0] - other, self[1][1] - other)

    @data_type_validation(other=Number)
    def __rsub__(self, other):
        return Matrix_33f(other - self[0][0], other - self[0][1],
                          other - self[1][0], other - self[1][1])

    def __neg__(self):
        return -1.0 * self

    def __mul__(self, other):
        if isinstance(other, Matrix_22f):
            a00 = self.row(0).dot(other.col(0))
            a01 = self.row(0).dot(other.col(1))
            a10 = self.row(1).dot(other.col(0))
            a11 = self.row(1).dot(other.col(1))
            return Matrix_22f(a00, a01,
                              a10, a11)

        if isinstance(other, Vec2f):
            x = self.row(0).dot(other)
            y = self.row(1).dot(other)
            return Vec2f(x, y)

        if isinstance(other, Number):
            return Matrix_22f(self[0][0] * other, self[0][1] * other,
                              self[1][0] * other, self[1][1] * other)

    @data_type_validation(other=Number)
    def __rmul__(self, other):
        return Matrix_22f(self[0][0] * other, self[0][1] * other,
                          self[1][0] * other, self[1][1] * other)

    def t(self):
        return Matrix_22f.from_list(self.data)

    def det(self):
        return self[0][0] * self[1][1] - self[0][1] * self[1][0]

    def inv(self):
        det = self.det()
        if det == 0:
            raise ValueError('this Matrix is singular!')
        a00 = self[1][1] / det
        a10 = -self[1][0] / det
        a01 = -self[0][1] / det
        a11 = self[0][0] / det
        return Matrix_22f(a00, a01,
                          a10, a11)

    @classmethod
    def identity(cls):
        return cls(1.0, 0.0,
                   0.0, 1.0)

    @classmethod
    @data_type_validation(l=list)
    def from_list(cls, l):
        return cls(l[0][0], l[0][1],
                   l[1][0], l[1][1])

    @classmethod
    @data_type_validation(diagonal=(list, Vec2f))
    def from_diagonal(cls, diagonal):
        return cls(diagonal[0], 0,
                   0, diagonal[1])


class Matrix_33f(MatrixBase):
    dimension = (3, 3)

    @data_type_validation(a00=Number, a01=Number, a02=Number, a10=Number, a11=Number, a12=Number, a20=Number,
                          a21=Number, a22=Number)
    def __init__(self, a00, a01, a02, a10, a11, a12, a20, a21, a22):
        self.data = [Vec3f(a00, a01, a02), Vec3f(a10, a11, a12), Vec3f(a20, a21, a22)]

    def __repr__(self):
        return '{:.06f}\t{:.06f}\t{:.06f}\n' \
               '{:.06f}\t{:.06f}\t{:.06f}\n' \
               '{:.06f}\t{:.06f}\t{:.06f}\n'.format(self.data[0][0], self.data[0][1], self.data[0][2],
                                                    self.data[1][0], self.data[1][1], self.data[1][2],
                                                    self.data[2][0], self.data[2][1], self.data[2][2])

    @data_type_validation(index=int)
    def row(self, index):
        return Vec3f(self.data[index][0], self.data[index][1], self.data[index][2])

    @data_type_validation(index=int)
    def col(self, index):
        return Vec3f(self.data[0][index], self.data[1][index], self[2][index])

    @data_type_validation(index=int)
    def __getitem__(self, index):
        return self.data[index]

    def __add__(self, other):
        if isinstance(other, Matrix_33f):
            return Matrix_33f(self[0][0] + other[0][0], self[0][1] + other[0][1], self[0][2] + other[0][2],
                              self[1][0] + other[1][0], self[1][1] + other[1][1], self[1][2] + other[1][2],
                              self[2][0] + other[2][0], self[2][1] + other[2][1], self[2][2] + other[2][2])
        if isinstance(other, Number):
            return Matrix_33f(self[0][0] + other, self[0][1] + other, self[0][2] + other,
                              self[1][0] + other, self[1][1] + other, self[1][2] + other,
                              self[2][0] + other, self[2][1] + other, self[2][2] + other)

    @data_type_validation(other=Number)
    def __radd__(self, other):
        return Matrix_33f(self[0][0] + other, self[0][1] + other, self[0][2] + other,
                          self[1][0] + other, self[1][1] + other, self[1][2] + other,
                          self[2][0] + other, self[2][1] + other, self[2][2] + other)

    def __sub__(self, other):
        if isinstance(other, Matrix_33f):
            return Matrix_33f(self[0][0] - other[0][0], self[0][1] - other[0][1], self[0][2] - other[0][2],
                              self[1][0] - other[1][0], self[1][1] - other[1][1], self[1][2] - other[1][2],
                              self[2][0] - other[2][0], self[2][1] - other[2][1], self[2][2] - other[2][2])
        if isinstance(other, Number):
            return Matrix_33f(self[0][0] - other, self[0][1] - other, self[0][2] - other,
                              self[1][0] - other, self[1][1] - other, self[1][2] - other,
                              self[2][0] - other, self[2][1] - other, self[2][2] - other)

    @data_type_validation(other=Number)
    def __rsub__(self, other):
        return Matrix_33f(other - self[0][0], other - self[0][1], other - self[0][2],
                          other - self[1][0], other - self[1][1], other - self[1][2],
                          other - self[2][0], other - self[2][1], other - self[2][2])

    def __neg__(self):
        return -1.0 * self

    def __mul__(self, other):
        if isinstance(other, Matrix_33f):
            a00 = self.row(0).dot(other.col(0))
            a01 = self.row(0).dot(other.col(1))
            a02 = self.row(0).dot(other.col(2))
            a10 = self.row(1).dot(other.col(0))
            a11 = self.row(1).dot(other.col(1))
            a12 = self.row(1).dot(other.col(2))
            a20 = self.row(2).dot(other.col(0))
            a21 = self.row(2).dot(other.col(1))
            a22 = self.row(2).dot(other.col(2))
            return Matrix_33f(a00, a01, a02,
                              a10, a11, a12,
                              a20, a21, a22)

        if isinstance(other, Vec3f):
            x = self.row(0).dot(other)
            y = self.row(1).dot(other)
            z = self.row(2).dot(other)
            return Vec3f(x, y, z)

        if isinstance(other, Number):
            return Matrix_33f(self[0][0] * other, self[0][1] * other, self[0][2] * other,
                              self[1][0] * other, self[1][1] * other, self[1][2] * other,
                              self[2][0] * other, self[2][1] * other, self[2][2] * other)

    data_type_validation(other=Number)

    def __rmul__(self, other):
        return Matrix_33f(self[0][0] * other, self[0][1] * other, self[0][2] * other,
                          self[1][0] * other, self[1][1] * other, self[1][2] * other,
                          self[2][0] * other, self[2][1] * other, self[2][2] * other)

    def t(self):
        return Matrix_33f.from_list(self[0][0], self[1][0], self[2][0],
                                    self[0][1], self[1][1], self[2][1],
                                    self[0][2], self[1][2], self[2][2])

    def det(self):
        d1 = self[0][0] * (self[1][1] * self[2][2] - self[1][2] * self[2][1])
        d2 = self[0][1] * (self[1][0] * self[2][2] - self[1][2] * self[2][0])
        d3 = self[0][2] * (self[1][0] * self[2][1] - self[1][1] * self[2][0])
        return d1 - d2 + d3

    def inv(self):
        det = self.det()
        if det == 0:
            raise ValueError('this Matrix is singular!')
        a00 = (self[1][1] * self[2][2] - self[1][2] * self[2][1]) / det
        a10 = -(self[1][0] * self[2][2] - self[1][2] * self[2][0]) / det
        a20 = (self[1][0] * self[2][1] - self[1][1] * self[2][0]) / det
        a01 = -(self[0][1] * self[2][2] - self[0][2] * self[2][1]) / det
        a11 = (self[0][0] * self[2][2] - self[0][2] * self[2][0]) / det
        a21 = -(self[0][0] * self[2][1] - self[0][1] * self[2][0]) / det
        a02 = (self[0][1] * self[1][2] - self[0][2] * self[1][1]) / det
        a12 = -(self[0][0] * self[1][2] - self[0][2] * self[1][0]) / det
        a22 = (self[0][0] * self[1][1] - self[0][1] * self[1][0]) / det
        return Matrix_33f(a00, a01, a02,
                          a10, a11, a12,
                          a20, a21, a22)

    @classmethod
    def identity(cls):
        return cls(1.0, 0.0, 0.0,
                   0.0, 1.0, 0.0,
                   0.0, 0.0, 1.0)

    @classmethod
    @data_type_validation(l=list)
    def from_list(cls, l):
        return cls(l[0][0], l[0][1], l[0][2],
                   l[1][0], l[1][1], l[1][2],
                   l[2][0], l[2][1], l[2][2])

    @classmethod
    @data_type_validation(diagonal=(list, Vec3f))
    def from_diagonal(cls, diagonal):
        return cls(diagonal[0], 0, 0,
                   0, diagonal[1], 0,
                   0, 0, diagonal[2])

    @classmethod
    def from_quaternion(cls, q):
        from quaternion import Quaternion
        if isinstance(q, Quaternion):
            return q.matrix()

    @classmethod
    @data_type_validation(rx=Number, ry=Number, rz=Number)
    def from_euler_angles(cls, rx, ry, rz, order='xyz'):
        import math
        mx = cls.identity()
        mx[1][1] = mx[2][2] = math.cos(math.radians(rx))
        mx[1][2] = -math.sin(math.radians(rx))
        mx[2][1] = -mx[1][2]
        my = cls.identity()
        my[0][0] = my[2][2] = math.cos(math.radians(ry))
        my[0][2] = math.sin(math.radians(ry))
        my[2][0] = -my[0][2]
        mz = cls.identity()
        mz[0][0] = mz[1][1] = math.cos(math.radians(rz))
        mz[0][1] = -math.sin(math.radians(rz))
        mz[1][0] = -mz[0][1]

        mapping = {'x': mx, 'y': my, 'z': mz}
        return mapping[order[2]] * mapping[order[1]] * mapping[order[0]]

    def quaternion(self):
        from quaternion import Quaternion
        return Quaternion.from_matrix(self)

    def euler_angles(self, order='xyz'):
        import math
        if order == 'xyz':
            angle_1 = math.degrees(math.atan2(self[2][1], self[2][2]))
            angle_2 = -math.degrees(math.asin(self[2][0]))
            angle_3 = math.degrees(math.atan2(self[1][0], self[0][0]))
            return dict(zip(order.lower(), (angle_1, angle_2, angle_3)))
        if order == 'xzy':
            angle_1 = -math.degrees(math.atan2(self[1][2], self[1][1]))
            angle_2 = math.degrees(math.asin(self[1][0]))
            angle_3 = -math.degrees(math.atan2(self[2][0], self[0][0]))
            return dict(zip(order.lower(), (angle_1, angle_2, angle_3)))
        if order == 'yzx':
            angle_1 = math.degrees(math.atan2(self[0][2], self[0][0]))
            angle_2 = -math.degrees(math.asin(self[0][1]))
            angle_3 = math.degrees(math.atan2(self[2][1], self[1][1]))
            return dict(zip(order.lower(), (angle_1, angle_2, angle_3)))
        if order == 'yxz':
            angle_1 = -math.degrees(math.atan2(self[0][1], self[1][1]))
            angle_2 = math.degrees(math.asin(self[2][0]))
            angle_3 = -math.degrees(math.atan2(self[2][0], self[2][2]))
            return dict(zip(order.lower(), (angle_1, angle_2, angle_3)))
        if order == 'zxy':
            angle_1 = math.degrees(math.atan2(self[1][0], self[1][1]))
            angle_2 = -math.degrees(math.asin(self[1][2]))
            angle_3 = math.degrees(math.atan2(self[0][2], self[2][2]))
            return dict(zip(order.lower(), (angle_1, angle_2, angle_3)))
        if order == 'zyx':
            angle_1 = -math.degrees(math.atan2(self[0][1], self[0][0]))
            angle_2 = math.degrees(math.asin(self[0][2]))
            angle_3 = -math.degrees(math.atan2(self[1][2], self[2][2]))
            return dict(zip(order.lower(), (angle_1, angle_2, angle_3)))


class Matrix_44f(MatrixBase):
    dimension = (4, 4)

    @data_type_validation(a00=Number, a01=Number, a02=Number, a03=Number,
                          a10=Number, a11=Number, a12=Number, a13=Number,
                          a20=Number, a21=Number, a22=Number, a23=Number,
                          a30=Number, a31=Number, a32=Number, a33=Number)
    def __init__(self, a00, a01, a02, a03, a10, a11, a12, a13, a20, a21, a22, a23, a30, a31, a32, a33):
        self.data = [Vec4f(a00, a01, a02, a03),
                     Vec4f(a10, a11, a12, a13),
                     Vec4f(a20, a21, a22, a23),
                     Vec4f(a30, a31, a32, a33)]

    @data_type_validation(index=int)
    def row(self, index):
        return Vec4f(self[index][0], self[index][1], self[index][2], self[index][3])

    @data_type_validation(index=int)
    def col(self, index):
        return Vec4f(self[0][index], self[1][index], self[2][index], self[3][index])

    @data_type_validation(index=int)
    def __getitem__(self, index):
        return self.data[index]

    def __add__(self, other):
        if isinstance(other, Matrix_44f):
            return Matrix_44f(self[0][0] + other[0][0], self[0][1] + other[0][1], self[0][2] + other[0][2],
                              self[0][3] + other[0][3],
                              self[1][0] + other[1][0], self[1][1] + other[1][1], self[1][2] + other[1][2],
                              self[1][3] + other[1][4],
                              self[2][0] + other[2][0], self[2][1] + other[2][1], self[2][2] + other[2][2],
                              self[2][3] + other[2][4],
                              self[3][0] + other[3][0], self[3][1] + other[3][1], self[3][2] + other[3][2],
                              self[3][3] + other[3][4],
                              )
        if isinstance(other, Number):
            return Matrix_44f(self[0][0] + other, self[0][1] + other, self[0][2] + other, self[0][3] + other,
                              self[1][0] + other, self[1][1] + other, self[1][2] + other, self[1][3] + other,
                              self[2][0] + other, self[2][1] + other, self[2][2] + other, self[2][3] + other,
                              self[3][0] + other, self[3][1] + other, self[3][2] + other, self[3][3] + other)

    @data_type_validation(other=Number)
    def __radd__(self, other):
        return Matrix_44f(self[0][0] + other, self[0][1] + other, self[0][2] + other, self[0][3] + other,
                          self[1][0] + other, self[1][1] + other, self[1][2] + other, self[1][3] + other,
                          self[2][0] + other, self[2][1] + other, self[2][2] + other, self[2][3] + other,
                          self[3][0] + other, self[3][1] + other, self[3][2] + other, self[3][3] + other)

    def __sub__(self, other):
        if isinstance(other, Matrix_44f):
            return Matrix_44f(self[0][0] - other[0][0], self[0][1] - other[0][1], self[0][2] - other[0][2],
                              self[0][3] - other[0][3],
                              self[1][0] - other[1][0], self[1][1] - other[1][1], self[1][2] - other[1][2],
                              self[1][3] - other[1][4],
                              self[2][0] - other[2][0], self[2][1] - other[2][1], self[2][2] - other[2][2],
                              self[2][3] - other[2][4],
                              self[3][0] - other[3][0], self[3][1] - other[3][1], self[3][2] - other[3][2],
                              self[3][3] - other[3][4],
                              )
        if isinstance(other, Number):
            return Matrix_44f(other - self[0][0], other - self[0][1], other - self[0][2], other - self[0][3],
                              other - self[1][0], other - self[1][1], other - self[1][2], other - self[1][3],
                              other - self[2][0], other - self[2][1], other - self[2][2], other - self[2][3],
                              other - self[3][0], other - self[3][1], other - self[3][2], other - self[3][3])

    @data_type_validation(other=Number)
    def __rsub__(self, other):
        return Matrix_44f(other - self[0][0], other - self[0][1], other - self[0][2], other - self[0][3],
                          other - self[1][0], other - self[1][1], other - self[1][2], other - self[1][3],
                          other - self[2][0], other - self[2][1], other - self[2][2], other - self[2][3],
                          other - self[3][0], other - self[3][1], other - self[3][2], other - self[3][3])

    def __neg__(self):
        return -1.0 * self

    def __mul__(self, other):
        if isinstance(other, Matrix_33f):
            a00 = self.row(0).dot(other.col(0))
            a01 = self.row(0).dot(other.col(1))
            a02 = self.row(0).dot(other.col(2))
            a03 = self.row(0).dot(other.col(3))
            a10 = self.row(1).dot(other.col(0))
            a11 = self.row(1).dot(other.col(1))
            a12 = self.row(1).dot(other.col(2))
            a13 = self.row(1).dot(other.col(3))
            a20 = self.row(2).dot(other.col(0))
            a21 = self.row(2).dot(other.col(1))
            a22 = self.row(2).dot(other.col(2))
            a23 = self.row(2).dot(other.col(3))
            a30 = self.row(3).dot(other.col(0))
            a31 = self.row(3).dot(other.col(1))
            a32 = self.row(3).dot(other.col(2))
            a33 = self.row(3).dot(other.col(3))
            return Matrix_33f(a00, a01, a02, a03,
                              a10, a11, a12, a13,
                              a20, a21, a22, a23,
                              a30, a31, a32, a33)

        if isinstance(other, Vec4f):
            x = self.row(0).dot(other)
            y = self.row(1).dot(other)
            z = self.row(2).dot(other)
            w = self.row(3).dot(other)
            return Vec3f(x, y, z, w)

        if isinstance(other, Number):
            return Matrix_33f(self[0][0] * other, self[0][1] * other, self[0][2] * other,
                              self[1][0] * other, self[1][1] * other, self[1][2] * other,
                              self[2][0] * other, self[2][1] * other, self[2][2] * other)

    data_type_validation(other=Number)

    def __rmul__(self, other):
        return Matrix_44f(self[0][0] * other, self[0][1] * other, self[0][2] * other, self[0][3] * other,
                          self[1][0] * other, self[1][1] * other, self[1][2] * other, self[1][3] * other,
                          self[2][0] * other, self[2][1] * other, self[2][2] * other, self[2][3] * other,
                          self[3][0] * other, self[3][1] * other, self[3][2] * other, self[3][3] * other)

    def t(self):
        return Matrix_33f.from_list(self[0][0], self[1][0], self[2][0], self[3][0],
                                    self[0][1], self[1][1], self[2][1], self[3][1],
                                    self[0][2], self[1][2], self[2][2], self[3][2],
                                    self[0][3], self[1][3], self[2][3], self[3][3], )

    # def det(self):
    #     d1 = self[0][0] * (self[1][1] * self[2][2] - self[1][2] * self[2][1])
    #     d2 = self[0][1] * (self[1][0] * self[2][2] - self[1][2] * self[2][0])
    #     d3 = self[0][2] * (self[1][0] * self[2][1] - self[1][1] * self[2][0])
    #     return d1 - d2 + d3
    #
    # def inv(self):
    #     det = self.det()
    #     if det == 0:
    #         raise ValueError('this Matrix is singular!')
    #     a00 = (self[1][1] * self[2][2] - self[1][2] * self[2][1]) / det
    #     a10 = -(self[1][0] * self[2][2] - self[1][2] * self[2][0]) / det
    #     a20 = (self[1][0] * self[2][1] - self[1][1] * self[2][0]) / det
    #     a01 = -(self[0][1] * self[2][2] - self[0][2] * self[2][1]) / det
    #     a11 = (self[0][0] * self[2][2] - self[0][2] * self[2][0]) / det
    #     a21 = -(self[0][0] * self[2][1] - self[0][1] * self[2][0]) / det
    #     a02 = (self[0][1] * self[1][2] - self[0][2] * self[1][1]) / det
    #     a12 = -(self[0][0] * self[1][2] - self[0][2] * self[1][0]) / det
    #     a22 = (self[0][0] * self[1][1] - self[0][1] * self[1][0]) / det
    #     return Matrix_33f(a00, a01, a02,
    #                       a10, a11, a12,
    #                       a20, a21, a22)

    @classmethod
    def identity(cls):
        return cls(1.0, 0.0, 0.0, 0.0,
                   0.0, 1.0, 0.0, 0.0,
                   0.0, 0.0, 1.0, 0.0,
                   0.0, 0.0, 0.0, 1.0)

    @classmethod
    @data_type_validation(l=list)
    def from_list(cls, l):
        return cls(l[0][0], l[0][1], l[0][2], l[0][3],
                   l[1][0], l[1][1], l[1][2], l[1][3],
                   l[2][0], l[2][1], l[2][2], l[2][3],
                   l[3][0], l[3][1], l[3][2], l[3][3], )

    @classmethod
    @data_type_validation(diagonal=(list, Vec4f))
    def from_diagonal(cls, diagonal):
        return cls(diagonal[0], 0, 0, 0,
                   0, diagonal[1], 0, 0,
                   0, 0, diagonal[2], 0,
                   0, 0, 0, diagonal[3])


if __name__ == '__main__':
    from quaternion import Quaternion

    m22 = Matrix_22f(4, 7, 2, 6)
    print m22.inv()
    print m22.inv() * m22

    m33 = Matrix_33f(4, 7, 2, 6, 1, 4, 2, 2, 8)
    print m33.inv()
    print m33.inv() * m33
    # order = 'zyx'
    #
    # a = Quaternion.from_euler_angles(10, 20, 30, order=order)
    # print a
    # print a.matrix()
    #
    # m = Matrix_33f.from_quaternion(a)
    # print m
    #
    # print Matrix_33f.from_euler_angles(10, 20, 30, order=order)
    # print m.quaternion()
    # print m.euler_angles(order)
