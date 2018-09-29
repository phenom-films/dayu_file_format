#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from deco import data_type_validation
from numbers import Number
from vector import Vec2f, Vec3f, Vec4f


class MatrixBase(object):
    __slots__ = ['data']
    dimension = (1, 1)

    def __eq__(self, other):
        if isinstance(other, MatrixBase):
            return all((round(self[r][c] - other[r][c], 6) == 0
                        for r in range(self.dimension[0])
                        for c in range(self.dimension[1])))
        return False

    def clear(self):
        for r in range(self.dimension[0]):
            for c in range(self.dimension[1]):
                self[r][c] = 0


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

    @classmethod
    def from_matrix_33(cls, m33):
        if isinstance(m33, Matrix_33f):
            return Matrix_22f(m33[0][0], m33[0][1],
                              m33[1][0], m33[1][1])

    @classmethod
    def from_matrix_44(cls, m44):
        if isinstance(m44, Matrix_44f):
            return Matrix_22f(m44[0][0], m44[0][1],
                              m44[1][0], m44[1][1])


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

    @data_type_validation(other=Number)
    def __rmul__(self, other):
        return Matrix_33f(self[0][0] * other, self[0][1] * other, self[0][2] * other,
                          self[1][0] * other, self[1][1] * other, self[1][2] * other,
                          self[2][0] * other, self[2][1] * other, self[2][2] * other)

    def t(self):
        return Matrix_33f(self[0][0], self[1][0], self[2][0],
                          self[0][1], self[1][1], self[2][1],
                          self[0][2], self[1][2], self[2][2])

    def det(self):
        d1 = self[0][0] * Matrix_22f(self[1][1], self[1][2], self[2][1], self[2][2]).det()
        d2 = self[0][1] * Matrix_22f(self[1][0], self[1][2], self[2][0], self[2][2]).det()
        d3 = self[0][2] * Matrix_22f(self[1][0], self[1][1], self[2][0], self[2][1]).det()
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
    def from_matrix_44(cls, m44):
        if isinstance(m44, Matrix_44f):
            return Matrix_33f(m44[0][0], m44[0][1], m44[0][2],
                              m44[1][0], m44[1][1], m44[1][2],
                              m44[2][0], m44[2][1], m44[2][2])

    @classmethod
    def from_matrix_22(cls, m22):
        if isinstance(m44, Matrix_22f):
            return Matrix_33f(m22[0][0], m22[0][1], 0.0,
                              m22[1][0], m22[1][1], 0.0,
                              0.0, 0.0, 1.0)

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
            return angle_1, angle_2, angle_3
        if order == 'xzy':
            angle_1 = -math.degrees(math.atan2(self[1][2], self[1][1]))
            angle_2 = math.degrees(math.asin(self[1][0]))
            angle_3 = -math.degrees(math.atan2(self[2][0], self[0][0]))
            return angle_1, angle_3, angle_2
        if order == 'yzx':
            angle_1 = math.degrees(math.atan2(self[0][2], self[0][0]))
            angle_2 = -math.degrees(math.asin(self[0][1]))
            angle_3 = math.degrees(math.atan2(self[2][1], self[1][1]))
            return angle_3, angle_1, angle_2
        if order == 'yxz':r
            angle_1 = -math.degrees(math.atan2(self[0][1], self[1][1]))
            angle_2 = math.degrees(math.asin(self[2][0]))
            angle_3 = -math.degrees(math.atan2(self[2][0], self[2][2]))
            return angle_2, angle_1, angle_3
        if order == 'zxy':
            angle_1 = math.degrees(math.atan2(self[1][0], self[1][1]))
            angle_2 = -math.degrees(math.asin(self[1][2]))
            angle_3 = math.degrees(math.atan2(self[0][2], self[2][2]))
            return angle_2, angle_3, angle_1
        if order == 'zyx':
            angle_1 = -math.degrees(math.atan2(self[0][1], self[0][0]))
            angle_2 = math.degrees(math.asin(self[0][2]))
            angle_3 = -math.degrees(math.atan2(self[1][2], self[2][2]))
            return angle_3, angle_2, angle_1


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

    def __repr__(self):
        return '{:.06f}\t{:.06f}\t{:.06f}\t{:.06f}\n' \
               '{:.06f}\t{:.06f}\t{:.06f}\t{:.06f}\n' \
               '{:.06f}\t{:.06f}\t{:.06f}\t{:.06f}\n' \
               '{:.06f}\t{:.06f}\t{:.06f}\t{:.06f}\n'.format(
                self.data[0][0], self.data[0][1], self.data[0][2], self.data[0][3],
                self.data[1][0], self.data[1][1], self.data[1][2], self.data[1][3],
                self.data[2][0], self.data[2][1], self.data[2][2], self.data[2][3],
                self.data[3][0], self.data[3][1], self.data[3][2], self.data[3][3])

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
        if isinstance(other, Matrix_44f):
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
            return Matrix_44f(a00, a01, a02, a03,
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
        return Matrix_44f(self[0][0], self[1][0], self[2][0], self[3][0],
                          self[0][1], self[1][1], self[2][1], self[3][1],
                          self[0][2], self[1][2], self[2][2], self[3][2],
                          self[0][3], self[1][3], self[2][3], self[3][3])

    def det(self):
        d1 = self[0][0] * Matrix_33f(self[1][1], self[1][2], self[1][3],
                                     self[2][1], self[2][2], self[2][3],
                                     self[3][1], self[3][2], self[3][3]).det()
        d2 = self[0][1] * Matrix_33f(self[1][0], self[1][2], self[1][3],
                                     self[2][0], self[2][2], self[2][3],
                                     self[3][0], self[3][2], self[3][3]).det()
        d3 = self[0][2] * Matrix_33f(self[1][0], self[1][1], self[1][3],
                                     self[2][0], self[2][1], self[2][3],
                                     self[3][0], self[3][1], self[3][3]).det()
        d4 = self[0][3] * Matrix_33f(self[1][0], self[1][1], self[1][2],
                                     self[2][0], self[2][1], self[2][2],
                                     self[3][0], self[3][1], self[3][2]).det()
        return d1 - d2 + d3 - d4

    def inv(self):
        d00 = Matrix_33f(self[1][1], self[1][2], self[1][3],
                         self[2][1], self[2][2], self[2][3],
                         self[3][1], self[3][2], self[3][3]).det()
        d01 = Matrix_33f(self[1][0], self[1][2], self[1][3],
                         self[2][0], self[2][2], self[2][3],
                         self[3][0], self[3][2], self[3][3]).det()
        d02 = Matrix_33f(self[1][0], self[1][1], self[1][3],
                         self[2][0], self[2][1], self[2][3],
                         self[3][0], self[3][1], self[3][3]).det()
        d03 = Matrix_33f(self[1][0], self[1][1], self[1][2],
                         self[2][0], self[2][1], self[2][2],
                         self[3][0], self[3][1], self[3][2]).det()
        det = self[0][0] * d00 - self[0][1] * d01 + self[0][2] * d02 - self[0][3] * d03
        if det == 0:
            raise ValueError('this Matrix is singular!')

        a00 = d00 / det
        a01 = -d01 / det
        a02 = d02 / det
        a03 = -d03 / det

        a10 = -Matrix_33f(self[0][1], self[0][2], self[0][3],
                          self[2][1], self[2][2], self[2][3],
                          self[3][1], self[3][2], self[3][3]).det() / det
        a11 = Matrix_33f(self[0][0], self[0][2], self[0][3],
                         self[2][0], self[2][2], self[2][3],
                         self[3][0], self[3][2], self[3][3]).det() / det
        a12 = -Matrix_33f(self[0][0], self[0][1], self[0][3],
                          self[2][0], self[2][1], self[2][3],
                          self[3][0], self[3][1], self[3][3]).det() / det
        a13 = Matrix_33f(self[0][0], self[0][1], self[0][2],
                         self[2][0], self[2][1], self[2][2],
                         self[3][0], self[3][1], self[3][2]).det() / det
        a20 = Matrix_33f(self[0][1], self[0][2], self[0][3],
                         self[1][1], self[1][2], self[1][3],
                         self[3][1], self[3][2], self[3][3]).det() / det
        a21 = -Matrix_33f(self[0][0], self[0][2], self[0][3],
                          self[1][0], self[1][2], self[1][3],
                          self[3][0], self[3][2], self[3][3]).det() / det
        a22 = Matrix_33f(self[0][0], self[0][1], self[0][3],
                         self[1][0], self[1][1], self[1][3],
                         self[3][0], self[3][1], self[3][3]).det() / det
        a23 = -Matrix_33f(self[0][0], self[0][1], self[0][2],
                          self[1][0], self[1][1], self[1][2],
                          self[3][0], self[3][1], self[3][2]).det() / det
        a30 = -Matrix_33f(self[0][1], self[0][2], self[0][3],
                          self[1][1], self[1][2], self[1][3],
                          self[2][1], self[2][2], self[2][3]).det() / det
        a31 = Matrix_33f(self[0][0], self[0][2], self[0][3],
                         self[1][0], self[1][2], self[1][3],
                         self[2][0], self[2][2], self[2][3]).det() / det
        a32 = -Matrix_33f(self[0][0], self[0][1], self[0][3],
                          self[1][0], self[1][1], self[1][3],
                          self[2][0], self[2][1], self[2][3]).det() / det
        a33 = Matrix_33f(self[0][0], self[0][1], self[0][2],
                         self[1][0], self[1][1], self[1][2],
                         self[2][0], self[2][1], self[2][2]).det() / det

        return Matrix_44f(a00, a10, a20, a30,
                          a01, a11, a21, a31,
                          a02, a12, a22, a32,
                          a03, a13, a23, a33)

    @property
    def diagonal(self):
        return Vec4f(self[0][0], self[1][1], self[2][2], self[3][3])

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
                   l[3][0], l[3][1], l[3][2], l[3][3])

    @classmethod
    @data_type_validation(diagonal=(list, Vec4f))
    def from_diagonal(cls, diagonal):
        return cls(diagonal[0], 0, 0, 0,
                   0, diagonal[1], 0, 0,
                   0, 0, diagonal[2], 0,
                   0, 0, 0, diagonal[3])

    @classmethod
    @data_type_validation(m22=Matrix_22f)
    def from_matrix_22(cls, m22):
        return cls(m22[0][0], m22[0][1], 0, 0,
                   m22[1][0], m22[1][1], 0, 0,
                   0, 0, 1, 0,
                   0, 0, 0, 1)

    @classmethod
    @data_type_validation(m33=Matrix_33f)
    def from_matrix_33(cls, m33):
        return cls(m33[0][0], m33[0][1], m33[0][2], 0,
                   m33[1][0], m33[1][1], m33[1][2], 0,
                   m33[2][0], m33[2][1], m33[2][2], 0,
                   0, 0, 0, 1)

    @classmethod
    @data_type_validation(x=Number, y=Number, z=Number,
                          rx=Number, ry=Number, rz=Number,
                          sx=Number, sy=Number, sz=Number)
    def compose(cls, x, y, z, rx, ry, rz, sx=1.0, sy=1.0, sz=1.0, transform_order='srt', rotation_order='xyz'):
        translate_matrix = Matrix_44f.identity()
        translate_matrix[0][3] = x
        translate_matrix[1][3] = y
        translate_matrix[2][3] = z
        rotate_matrix = Matrix_44f.from_matrix_33(Matrix_33f.from_euler_angles(rx, ry, rz, order=rotation_order))
        scale_matrix = Matrix_44f.from_diagonal(Vec4f(sx, sy, sz, 1.0))

        mapping = {'s': scale_matrix, 'r': rotate_matrix, 't': translate_matrix}
        return mapping[transform_order[2]] * mapping[transform_order[1]] * mapping[transform_order[0]]

    def _decompose_rst(self):
        return self._decompose_srt()

    def _decompose_rts(self):
        return self._decompose_str()

    def _decompose_trs(self):
        return self._decompose_tsr()

    def _decompose_srt(self):
        translate_matrix = Matrix_44f.identity()
        translate_matrix[0][3] = self[0][3]
        translate_matrix[1][3] = self[1][3]
        translate_matrix[2][3] = self[2][3]

        scale_matrix = Matrix_44f.from_diagonal([self.col(0).length, self.col(1).length, self.col(2).length, 1.0])
        rotate_matrix = Matrix_44f.identity()
        rotate_matrix[0][0] = self[0][0] / scale_matrix[0][0]
        rotate_matrix[1][0] = self[1][0] / scale_matrix[0][0]
        rotate_matrix[2][0] = self[2][0] / scale_matrix[0][0]
        rotate_matrix[0][1] = self[0][1] / scale_matrix[1][1]
        rotate_matrix[1][1] = self[1][1] / scale_matrix[1][1]
        rotate_matrix[2][1] = self[2][1] / scale_matrix[1][1]
        rotate_matrix[0][2] = self[0][2] / scale_matrix[2][2]
        rotate_matrix[1][2] = self[1][2] / scale_matrix[2][2]
        rotate_matrix[2][2] = self[2][2] / scale_matrix[2][2]

        return {'translate': translate_matrix,
                'rotate'   : rotate_matrix,
                'scale'    : scale_matrix}

    def _decompose_str(self):
        scale_matrix = Matrix_44f.from_diagonal([self.col(0).length, self.col(1).length, self.col(2).length, 1.0])
        rotate_matrix = Matrix_44f.identity()
        rotate_matrix[0][0] = self[0][0] / scale_matrix[0][0]
        rotate_matrix[1][0] = self[1][0] / scale_matrix[0][0]
        rotate_matrix[2][0] = self[2][0] / scale_matrix[0][0]
        rotate_matrix[0][1] = self[0][1] / scale_matrix[1][1]
        rotate_matrix[1][1] = self[1][1] / scale_matrix[1][1]
        rotate_matrix[2][1] = self[2][1] / scale_matrix[1][1]
        rotate_matrix[0][2] = self[0][2] / scale_matrix[2][2]
        rotate_matrix[1][2] = self[1][2] / scale_matrix[2][2]
        rotate_matrix[2][2] = self[2][2] / scale_matrix[2][2]

        translate_matrix = Matrix_44f.identity()
        temp = rotate_matrix.inv() * self
        translate_matrix[0][3] = temp[0][3]
        translate_matrix[1][3] = temp[1][3]
        translate_matrix[2][3] = temp[2][3]

        return {'translate': translate_matrix,
                'rotate'   : rotate_matrix,
                'scale'    : scale_matrix}

    def _decompose_tsr(self):
        scale_matrix = Matrix_44f.from_diagonal([self.col(0).length, self.col(1).length, self.col(2).length, 1.0])
        rotate_matrix = Matrix_44f.identity()
        rotate_matrix[0][0] = self[0][0] / scale_matrix[0][0]
        rotate_matrix[1][0] = self[1][0] / scale_matrix[0][0]
        rotate_matrix[2][0] = self[2][0] / scale_matrix[0][0]
        rotate_matrix[0][1] = self[0][1] / scale_matrix[1][1]
        rotate_matrix[1][1] = self[1][1] / scale_matrix[1][1]
        rotate_matrix[2][1] = self[2][1] / scale_matrix[1][1]
        rotate_matrix[0][2] = self[0][2] / scale_matrix[2][2]
        rotate_matrix[1][2] = self[1][2] / scale_matrix[2][2]
        rotate_matrix[2][2] = self[2][2] / scale_matrix[2][2]

        translate_matrix = Matrix_44f.identity()
        temp = scale_matrix.inv() * rotate_matrix.inv() * self
        translate_matrix[0][3] = temp[0][3]
        translate_matrix[1][3] = temp[1][3]
        translate_matrix[2][3] = temp[2][3]

        return {'translate': translate_matrix,
                'rotate'   : rotate_matrix,
                'scale'    : scale_matrix}

    def decompose(self, transform_order='srt', rotation_order='xyz', matrix_form=False):
        func = getattr(self, '_decompose_{}'.format(transform_order), None)
        if func:
            result = func()
            if matrix_form:
                return result

            translate = (result['translate'][0][3], result['translate'][1][3], result['translate'][2][3])
            rotate = Matrix_33f.from_matrix_44(result['rotate']).euler_angles(order=rotation_order)
            scale = (result['scale'][0][0], result['scale'][1][1], result['scale'][2][2])
            return {'translate': translate, 'rotate': rotate, 'scale': scale}

        return None


if __name__ == '__main__':
    from quaternion import Quaternion

    transform_order = 'trs'

    m44 = Matrix_44f.compose(1, 2, 3, 10, 20, 30, 1, 1, 1, transform_order=transform_order)
    m44_2 = Matrix_44f.compose(1, 2, 3, 10, 20, 30, 1, 1, 1)

    # print Quaternion.from_euler_angles(10, 20, 30).matrix()

    print m44.decompose(transform_order=transform_order)

    m44.clear()
    print m44

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
