#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'


class SaveLoadMixin(object):
    def save(self, file_path, **kwargs):
        if file_path.endswith('.bcam'):
            pass

        if file_path.endswith('.cam'):
            self._save_ascii_file(file_path, **kwargs)
            return

    def _save_ascii_file(self, file_path, **kwargs):
        import json
        with open(file_path, 'w') as jf:
            result = {'global': dict(self.extra_data), 'channels': {}}
            result['global'].update(kwargs)
            result['global']['name'] = self.name
            result['global']['type'] = self.type
            result['global']['app'] = self.app
            result['global']['unit'] = self.unit
            result['global']['fps'] = self.fps
            result['global']['shutter'] = self.shutter
            result['global']['distort'] = self.distort
            result['global']['undistort'] = self.undistort
            result['global']['ccd'] = self.ccd
            result['global']['resolution'] = self.resolution
            result['global']['plate'] = self.plate
            result['global']['start'] = self.start
            result['global']['end'] = self.end
            result['global']['transform_order'] = self.transform_order
            result['global']['rotation_order'] = self.rotation_order

            result['channels']['x'] = self.x.to_dict()
            result['channels']['y'] = self.y.to_dict()
            result['channels']['z'] = self.z.to_dict()
            result['channels']['rx'] = self.rx.to_dict()
            result['channels']['ry'] = self.ry.to_dict()
            result['channels']['rz'] = self.rz.to_dict()
            result['channels']['sx'] = self.sx.to_dict()
            result['channels']['sy'] = self.sy.to_dict()
            result['channels']['sz'] = self.sz.to_dict()
            result['channels']['focal'] = self.focal.to_dict()
            result['channels']['focus'] = self.focus.to_dict()
            result['channels']['fstop'] = self.fstop.to_dict()
            result['channels']['near'] = self.near.to_dict()
            result['channels']['far'] = self.far.to_dict()
            result['channels']['pan_x'] = self.pan_x.to_dict()
            result['channels']['pan_y'] = self.pan_y.to_dict()
            result['channels']['zoom_x'] = self.zoom_x.to_dict()
            result['channels']['zoom_y'] = self.zoom_y.to_dict()
            result['channels']['a00'] = self.matrix[0][0].to_dict()
            result['channels']['a01'] = self.matrix[0][1].to_dict()
            result['channels']['a02'] = self.matrix[0][2].to_dict()
            result['channels']['a03'] = self.matrix[0][3].to_dict()
            result['channels']['a10'] = self.matrix[1][0].to_dict()
            result['channels']['a11'] = self.matrix[1][1].to_dict()
            result['channels']['a12'] = self.matrix[1][2].to_dict()
            result['channels']['a13'] = self.matrix[1][3].to_dict()
            result['channels']['a20'] = self.matrix[2][0].to_dict()
            result['channels']['a21'] = self.matrix[2][1].to_dict()
            result['channels']['a22'] = self.matrix[2][2].to_dict()
            result['channels']['a23'] = self.matrix[2][3].to_dict()
            result['channels']['a30'] = self.matrix[3][0].to_dict()
            result['channels']['a31'] = self.matrix[3][1].to_dict()
            result['channels']['a32'] = self.matrix[3][2].to_dict()
            result['channels']['a33'] = self.matrix[3][3].to_dict()

            json.dump(result, jf)

    def _load_ascii_file(self, file_path):
        import json
        from base import Curve
        json_data = None
        with open(file_path, 'r') as jf:
            json_data = json.load(jf)

        self.name = json_data['global'].pop('name')
        self.type = json_data['global'].pop('type')
        self.app = json_data['global'].pop('app')
        self.unit = json_data['global'].pop('unit')
        self.fps = json_data['global'].pop('fps')
        self.shutter = json_data['global'].pop('shutter')
        self.distort = json_data['global'].pop('distort')
        self.undistort = json_data['global'].pop('undistort')
        self.ccd = json_data['global'].pop('ccd')
        self.resolution = json_data['global'].pop('resolution')
        self.plate = json_data['global'].pop('plate')
        self.start = json_data['global'].pop('start')
        self.end = json_data['global'].pop('end')
        self.transform_order = json_data['global'].pop('transform_order')
        self.rotation_order = json_data['global'].pop('rotation_order')
        self.extra_data = dict(json_data['global'])

        self.x = Curve.from_dict(json_data['channels'].pop('x'))
        self.y = Curve.from_dict(json_data['channels'].pop('y'))
        self.z = Curve.from_dict(json_data['channels'].pop('z'))
        self.rx = Curve.from_dict(json_data['channels'].pop('rx'))
        self.ry = Curve.from_dict(json_data['channels'].pop('ry'))
        self.rz = Curve.from_dict(json_data['channels'].pop('rz'))
        self.sx = Curve.from_dict(json_data['channels'].pop('sx'))
        self.sy = Curve.from_dict(json_data['channels'].pop('sy'))
        self.sz = Curve.from_dict(json_data['channels'].pop('sz'))
        self.focal = Curve.from_dict(json_data['channels'].pop('focal'))
        self.focus = Curve.from_dict(json_data['channels'].pop('focus'))
        self.fstop = Curve.from_dict(json_data['channels'].pop('fstop'))
        self.near = Curve.from_dict(json_data['channels'].pop('near'))
        self.far = Curve.from_dict(json_data['channels'].pop('far'))
        self.pan_x = Curve.from_dict(json_data['channels'].pop('pan_x'))
        self.pan_y = Curve.from_dict(json_data['channels'].pop('pan_y'))
        self.zoom_x = Curve.from_dict(json_data['channels'].pop('zoom_x'))
        self.zoom_y = Curve.from_dict(json_data['channels'].pop('zoom_y'))
        a00 = Curve.from_dict(json_data['channels'].pop('a00'))
        a01 = Curve.from_dict(json_data['channels'].pop('a01'))
        a02 = Curve.from_dict(json_data['channels'].pop('a02'))
        a03 = Curve.from_dict(json_data['channels'].pop('a03'))
        a10 = Curve.from_dict(json_data['channels'].pop('a10'))
        a11 = Curve.from_dict(json_data['channels'].pop('a11'))
        a12 = Curve.from_dict(json_data['channels'].pop('a12'))
        a13 = Curve.from_dict(json_data['channels'].pop('a13'))
        a20 = Curve.from_dict(json_data['channels'].pop('a20'))
        a21 = Curve.from_dict(json_data['channels'].pop('a21'))
        a22 = Curve.from_dict(json_data['channels'].pop('a22'))
        a23 = Curve.from_dict(json_data['channels'].pop('a23'))
        a30 = Curve.from_dict(json_data['channels'].pop('a30'))
        a31 = Curve.from_dict(json_data['channels'].pop('a31'))
        a32 = Curve.from_dict(json_data['channels'].pop('a32'))
        a33 = Curve.from_dict(json_data['channels'].pop('a33'))
        self.matrix = [[a00, a01, a02, a03],
                       [a10, a11, a12, a13],
                       [a20, a21, a22, a23],
                       [a30, a31, a32, a33]]

        return True

    @classmethod
    def load(cls, file_path):
        if file_path.endswith('.bcam'):
            pass

        if file_path.endswith('.cam'):
            instance = cls()
            instance._load_ascii_file(file_path)
            return instance
