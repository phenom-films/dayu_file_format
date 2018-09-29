#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from dayu_file_format.curve import Point2D, KeyFrame, Curve
from dayu_file_format.lina.matrix import Matrix_44f
from config import UNIT_SCALE
from mixin import SaveLoadMixin
from deco import data_type_validation


class CameraKeyFrame(object):
    __slots__ = ['time', 'matrix', 'focus', 'focal', 'near', 'far', 'fstop',
                 'translate', 'rotate', 'scale', 'pan', 'zoom']

    def __init__(self, time=0, translate=None, rotate=None, scale=None, matrix=None,
                 focus=None, focal=None, near=None, far=None, fstop=None,
                 pan=None, zoom=None):
        self.time = time
        self.translate = translate
        self.rotate = rotate
        self.scale = scale
        self.matrix = matrix
        self.focus = focus
        self.focal = focal
        self.fstop = fstop
        self.near = near
        self.far = far
        self.pan = pan
        self.zoom = zoom

    def __repr__(self):
        return '<CameraKeyFrame>\n' \
               'time =      {}\n' \
               'translate = {}\n' \
               'rotate =    {}\n' \
               'scale =     {}\n' \
               'focal =     {}\n' \
               'focus =     {}\n' \
               'fstop =     {}\n' \
               'near =      {}\n' \
               'far =       {}\n' \
               'pan =       {}\n' \
               'zoom =      {}\n' \
               'matrix = \n' \
               '{}\n'.format(self.time, self.translate, self.rotate, self.scale, self.focal, self.focus,
                             self.fstop, self.near, self.far, self.pan, self.zoom, self.matrix)


class Camera(SaveLoadMixin):
    def __init__(self):
        self.name = 'main'
        self.type = 'generic'
        self.app = ''
        self.unit = 'cm'
        self.fps = 24.0
        self.shutter = 180.0
        self.distort = ''
        self.undistort = ''
        self.ccd = [23.76, 12.84]
        self.resolution = [1920, 1080]
        self.plate = ''
        self.start = 1001
        self.end = 1100
        self.x = Curve()
        self.y = Curve()
        self.z = Curve()
        self.rx = Curve()
        self.ry = Curve()
        self.rz = Curve()
        self.sx = Curve()
        self.sy = Curve()
        self.sz = Curve()
        self.focal = Curve()
        self.focus = Curve()
        self.fstop = Curve()
        self.near = Curve()
        self.far = Curve()
        self.pan_x = Curve()
        self.pan_y = Curve()
        self.zoom_x = Curve()
        self.zoom_y = Curve()
        self.transform_order = 'srt'
        self.rotation_order = 'xyz'
        self.matrix = [[Curve(), Curve(), Curve(), Curve()],
                       [Curve(), Curve(), Curve(), Curve()],
                       [Curve(), Curve(), Curve(), Curve()],
                       [Curve(), Curve(), Curve(), Curve()]]
        self.extra_data = {}

    def eval(self, time, method=None, unit=None, use_matrix=False):
        unit = unit if unit else self.unit
        unit_factor = pow(10.0, UNIT_SCALE.index(self.unit) - UNIT_SCALE.index(unit))

        focal = self.focal.eval(time, method=method if method else self.x.method)
        focus = self.focus.eval(time, method=method if method else self.x.method)
        fstop = self.fstop.eval(time, method=method if method else self.x.method)
        near = self.near.eval(time, method=method if method else self.x.method)
        far = self.far.eval(time, method=method if method else self.x.method)
        pan_x = self.pan_x.eval(time, method=method if method else self.x.method)
        pan_y = self.pan_y.eval(time, method=method if method else self.x.method)
        zoom_x = self.zoom_x.eval(time, method=method if method else self.x.method)
        zoom_y = self.zoom_y.eval(time, method=method if method else self.x.method)

        if use_matrix:
            a00 = self.matrix[0][0].eval(time, method=method if method else self.matrix[0][0].method)
            a01 = self.matrix[0][1].eval(time, method=method if method else self.matrix[0][1].method)
            a02 = self.matrix[0][2].eval(time, method=method if method else self.matrix[0][2].method)
            a03 = self.matrix[0][3].eval(time, method=method if method else self.matrix[0][3].method)
            a10 = self.matrix[1][0].eval(time, method=method if method else self.matrix[1][0].method)
            a11 = self.matrix[1][1].eval(time, method=method if method else self.matrix[1][1].method)
            a12 = self.matrix[1][2].eval(time, method=method if method else self.matrix[1][2].method)
            a13 = self.matrix[1][3].eval(time, method=method if method else self.matrix[1][3].method)
            a20 = self.matrix[2][0].eval(time, method=method if method else self.matrix[2][0].method)
            a21 = self.matrix[2][1].eval(time, method=method if method else self.matrix[2][1].method)
            a22 = self.matrix[2][2].eval(time, method=method if method else self.matrix[2][2].method)
            a23 = self.matrix[2][3].eval(time, method=method if method else self.matrix[2][3].method)
            a30 = self.matrix[3][0].eval(time, method=method if method else self.matrix[3][0].method)
            a31 = self.matrix[3][1].eval(time, method=method if method else self.matrix[3][1].method)
            a32 = self.matrix[3][2].eval(time, method=method if method else self.matrix[3][2].method)
            a33 = self.matrix[3][3].eval(time, method=method if method else self.matrix[3][3].method)
            m44 = Matrix_44f(a00, a01, a02, a03,
                             a10, a11, a12, a13,
                             a20, a21, a22, a23,
                             a30, a31, a32, a33)
            srt_component = m44.decompose(transform_order=self.transform_order,
                                          rotation_order=self.rotation_order)
            return CameraKeyFrame(time, srt_component['translate'],
                                  srt_component['rorate'], srt_component['scale'], m44,
                                  focus, focal, near, far, fstop, (pan_x, pan_y), (zoom_x, zoom_y))

        else:
            x = self.x.eval(time, method=method if method else self.x.method)
            y = self.y.eval(time, method=method if method else self.x.method)
            z = self.z.eval(time, method=method if method else self.x.method)
            rx = self.rx.eval(time, method=method if method else self.x.method)
            ry = self.ry.eval(time, method=method if method else self.x.method)
            rz = self.rz.eval(time, method=method if method else self.x.method)
            sx = self.sx.eval(time, method=method if method else self.x.method)
            sy = self.sy.eval(time, method=method if method else self.x.method)
            sz = self.sz.eval(time, method=method if method else self.x.method)
            m44 = Matrix_44f.compose(x, y, z, rx, ry, rz, sx, sy, sz,
                                     transform_order=self.transform_order, rotation_order=self.rotation_order)
            return CameraKeyFrame(time, (x, y, z), (rx, ry, rz), (sx, sy, sz), m44,
                                  focus, focal, near, far, fstop, (pan_x, pan_y), (zoom_x, zoom_y))

    @property
    def duration(self):
        return self.end - self.start


class StereoCamera(Camera):
    def __init__(self):
        super(StereoCamera, self).__init__()
        self.inter_axial = Curve()
        self.left_inter_axial = Curve()
        self.right_inter_axial = Curve()
        self.inter_toe = Curve()
        self.left_inter_toe = Curve()
        self.right_inter_axial = Curve()

    @property
    def main_camera(self):
        return

    @property
    def left_camera(self):
        return

    @property
    def right_camera(self):
        return


if __name__ == '__main__':
    ccc = Camera.load('/Users/andyguo/Desktop/cccc.cam')
    for t in range(0, 35):
        print ccc.eval(t)

    # ccc = Camera()
    # ccc.x.add(KeyFrame(Point2D(1, 1),
    #                    left=Point2D(1, 0),
    #                    right=Point2D(1, 0.66435778141).normalize()))
    # ccc.x.add(KeyFrame(Point2D(20, 9.835835457),
    #                    left=Point2D(-1, -0.0664163604379).normalize(),
    #                    right=Point2D(1, 0.0664163604379).normalize()))
    # ccc.x.add(KeyFrame(Point2D(50, 10.49999905),
    #                    left=Point2D(-1, 5.68935010214e-10).normalize(),
    #                    right=Point2D(1, 0).normalize()))
    #
    # ccc.y.add(KeyFrame(Point2D(1, 2.0),
    #                    left=Point2D(1, 0),
    #                    right=Point2D(1, 0.341514438391).normalize()))
    # ccc.y.add(KeyFrame(Point2D(20, 6.325849533),
    #                    left=Point2D(-1, 0).normalize(),
    #                    right=Point2D(1, 0).normalize()))
    # ccc.y.add(KeyFrame(Point2D(50, 2.409999609),
    #                    left=Point2D(-1, 0.195792496204).normalize(),
    #                    right=Point2D(1, 0).normalize()))
    #
    # ccc.z.add(KeyFrame(Point2D(1, 3.0),
    #                    left=Point2D(-1, 0),
    #                    right=Point2D(1, -0.185011982918).normalize()))
    # ccc.z.add(KeyFrame(Point2D(20, 0.6565149426),
    #                    left=Point2D(-1, 0).normalize(),
    #                    right=Point2D(1, 0).normalize()))
    # ccc.z.add(KeyFrame(Point2D(50, 3.660000324),
    #                    left=Point2D(-1, -0.150174275041).normalize(),
    #                    right=Point2D(1, 0).normalize()))
    #
    # ccc.rx.add(KeyFrame(Point2D(1, -88.49148009),
    #                     left=Point2D(-1, 0),
    #                     right=Point2D(1, 5.44862508774).normalize()))
    # ccc.rx.add(KeyFrame(Point2D(20, -19.47556383),
    #                     left=Point2D(-1, 0).normalize(),
    #                     right=Point2D(1, 0).normalize()))
    # ccc.rx.add(KeyFrame(Point2D(50, -28.81797854),
    #                     left=Point2D(-1, 0.467120736837).normalize(),
    #                     right=Point2D(1, 0).normalize()))
    #
    # ccc.ry.add(KeyFrame(Point2D(1, 28.9703908),
    #                     left=Point2D(-1, 0),
    #                     right=Point2D(1, -4.01200819016).normalize()))
    # ccc.ry.add(KeyFrame(Point2D(20, -21.84837838),
    #                     left=Point2D(-1, 0).normalize(),
    #                     right=Point2D(1, 0).normalize()))
    # ccc.ry.add(KeyFrame(Point2D(50, 2.858288813),
    #                     left=Point2D(-1, -1.23533332348).normalize(),
    #                     right=Point2D(1, 0).normalize()))
    #
    # ccc.rz.add(KeyFrame(Point2D(1, -27.07991909),
    #                     left=Point2D(-1, 0),
    #                     right=Point2D(1, -1.20982503891).normalize()))
    # ccc.rz.add(KeyFrame(Point2D(20, -42.40436886),
    #                     left=Point2D(-1, 0).normalize(),
    #                     right=Point2D(1, 0).normalize()))
    # ccc.rz.add(KeyFrame(Point2D(50, 9.235821923),
    #                     left=Point2D(-1, -2.58200955391).normalize(),
    #                     right=Point2D(1, 0).normalize()))
    #
    # ccc.sx.add(KeyFrame(Point2D(1, 1)))
    # ccc.sy.add(KeyFrame(Point2D(1, 1)))
    # ccc.sz.add(KeyFrame(Point2D(1, 1)))
    #
    # ccc.focal.add(KeyFrame(Point2D(1, 50.0),
    #                        left=Point2D(-1, 0).normalize(),
    #                        right=Point2D(1, -1.7763158083).normalize()))
    # ccc.focal.add(KeyFrame(Point2D(20, 27.5),
    #                        left=Point2D(-1, 0).normalize(),
    #                        right=Point2D(1, -1.7763158083).normalize()))
    # ccc.focal.add(KeyFrame(Point2D(50, 100.0),
    #                        left=Point2D(-1, -3.625).normalize(),
    #                        right=Point2D(1, 0).normalize()))
    #
    # ccc.focus.add(KeyFrame(Point2D(1, 2.0),
    #                        left=Point2D(-1, 0).normalize(),
    #                        right=Point2D(1, 0.631578922272).normalize()))
    # ccc.focus.add(KeyFrame(Point2D(20, 10.0),
    #                        left=Point2D(-1, 0).normalize(),
    #                        right=Point2D(1, 0).normalize()))
    # ccc.focus.add(KeyFrame(Point2D(50, 0.47),
    #                        left=Point2D(-1, 0.47650000453).normalize(),
    #                        right=Point2D(1, 0).normalize()))
    #
    # ccc.fstop.add(KeyFrame(Point2D(1, 16.0),
    #                        left=Point2D(-1, 0).normalize(),
    #                        right=Point2D(1, -1.01052629948).normalize()))
    # ccc.fstop.add(KeyFrame(Point2D(20, 3.2),
    #                        left=Point2D(-1, 0).normalize(),
    #                        right=Point2D(1, 0).normalize()))
    # ccc.fstop.add(KeyFrame(Point2D(50, 29.0),
    #                        left=Point2D(-1, -1.28999996185).normalize(),
    #                        right=Point2D(1, 0).normalize()))
    #
    # ccc.near.add(KeyFrame(Point2D(1, 0.1),
    #                       left=Point2D(-1, 0).normalize(),
    #                       right=Point2D(1, 0.000947368447669).normalize()))
    # ccc.near.add(KeyFrame(Point2D(20, 0.118),
    #                       left=Point2D(-1, -0.000947368447669).normalize(),
    #                       right=Point2D(1, 0).normalize()))
    #
    # ccc.pan_x.add(KeyFrame(Point2D(1, 0)))
    # ccc.pan_y.add(KeyFrame(Point2D(1, 0)))
    #
    # ccc.zoom_x.add(KeyFrame(Point2D(1, 1)))
    # ccc.zoom_y.add(KeyFrame(Point2D(1, 1)))
    #
    # for t in range(20, 51):
    #     print ccc.eval(t)
    #
    # ccc.save('/Users/andyguo/Desktop/cccc.cam', xxxx='woshi')
