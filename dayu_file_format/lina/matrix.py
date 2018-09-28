#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from deco import data_type_validation
from numbers import Number
from vector import Vec3f


class MatrixBase(object):
    pass


class Matrix_33f(MatrixBase):
    @data_type_validation(a00=Number, a01=Number, a02=Number, a10=Number, a11=Number, a12=Number, a20=Number,
                          a21=Number, a22=Number)
    def __init__(self, a00, a01, a02, a10, a11, a12, a20, a21, a22, column_first=False):
        self.dimension = (3, 3)
        if column_first:
            self.data = [Vec3f(a00, a10, a20), Vec3f(a01, a11, a21), Vec3f(a02, a12, a22)]
        else:
            self.data = [Vec3f(a00, a01, a02), Vec3f(a10, a11, a12), Vec3f(a20, a21, a22)]

    def __repr__(self):
        return '{}\t{}\t{}\n{}\t{}\t{}\n{}\t{}\t{}'.format(self.data[0][0], self.data[0][1], self.data[0][2],
                                                           self.data[1][0], self.data[1][1], self.data[1][2],
                                                           self.data[2][0], self.data[2][1], self.data[2][2])

    @classmethod
    def identity(cls, column_first=False):
        return cls(1.0, 0.0, 0.0,
                   0.0, 1.0, 0.0,
                   0.0, 0.0, 1.0, column_first=column_first)

    @classmethod
    @data_type_validation(l=list)
    def from_list(cls, l, column_first=False):
        return cls(l[0][0], l[0][1], l[0][2],
                   l[1][0], l[1][1], l[1][2],
                   l[2][0], l[2][1], l[1][2], column_first=column_first)

    @classmethod
    @data_type_validation(diagonal=(list, Vec3f))
    def from_diagonal(cls, diagonal, column_first=False):
        return cls(diagonal[0], 0, 0,
                   0, diagonal[1], 0,
                   0, 0, diagonal[2], column_first=column_first)

    @classmethod
    def from_quaternion(cls, q):
        from quaternion import Quaternion
        if isinstance(q, Quaternion):
            matrix = q.matrix()
            return cls(matrix[0][0], matrix[0][1], matrix[0][2],
                       matrix[1][0], matrix[1][1], matrix[1][2],
                       matrix[2][0], matrix[2][1], matrix[2][2], column_first=False)

    @classmethod
    @data_type_validation(rx=Number, ry=Number, rz=Number)
    def from_euler_angles(cls, rx, ry, rz, order='xyz'):
        pass


if __name__ == '__main__':
    from quaternion import Quaternion

    a = Matrix_33f.identity()
    print a

    b = Matrix_33f.from_quaternion(Quaternion.from_euler_angles(10, 20, 30))
    print b
