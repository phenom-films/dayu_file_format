#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import bisect
import struct

from config import pack_fmt_code, pack_fmt_func, unpack_fmt_code
from data_structure import Point2D, KeyFrame


class InterpolationMixin(object):
    def eval(self, x, method='hermite'):
        if not self._keyframes:
            return None

        func = getattr(self, '_eval_{}'.format(method))
        if func:
            return func(x)

        return None

    def _eval_step(self, x):
        if x <= self[0].current.x:
            return self[0].current.y

        if x >= self[-1].current.x:
            return self[-1].current.y

        index = bisect.bisect([k.current.x for k in self], x)
        prev_keyframe = self[index - 1]
        return prev_keyframe.current.y

    def _eval_linear(self, x):
        if x <= self[0].current.x:
            left_most_keyframe = self[0]
            result = left_most_keyframe.current.y - \
                     left_most_keyframe.left_tangent * (left_most_keyframe.current.x - x)
            return result

        if x >= self[-1].current.x:
            right_most_keyframe = self[-1]
            result = right_most_keyframe.current.y + \
                     right_most_keyframe.right_tangent * (x - right_most_keyframe.current.x)
            return result

        index = bisect.bisect([k.current.x for k in self], x)
        prev_keyframe = self[index - 1]
        next_keyframe = self[index]

        t = (x - prev_keyframe.current.x) / float(next_keyframe.current.x - prev_keyframe.current.x)
        result = (1.0 - t) * prev_keyframe.current.y + t * next_keyframe.current.y
        return result

    def _eval_hermite(self, x):
        if x <= self[0].current.x:
            left_most_keyframe = self[0]
            result = left_most_keyframe.current.y - \
                     left_most_keyframe.left_tangent * (left_most_keyframe.current.x - x)
            return result

        if x >= self[-1].current.x:
            right_most_keyframe = self[-1]
            result = right_most_keyframe.current.y + \
                     right_most_keyframe.right_tangent * (x - right_most_keyframe.current.x)
            return result

        index = bisect.bisect([k.current.x for k in self], x)
        prev_keyframe = self[index - 1]
        next_keyframe = self[index]

        delta_x = next_keyframe.current.x - prev_keyframe.current.x
        delta_y = next_keyframe.current.y - prev_keyframe.current.y
        p0 = prev_keyframe.current.y
        p1 = prev_keyframe.right_tangent
        p2 = (3 * delta_y - (2 * p1 + next_keyframe.left_tangent) * delta_x) / (delta_x ** 2)
        p3 = ((next_keyframe.left_tangent + p1) * delta_x - 2 * delta_y) / (delta_x ** 3)
        result = ((p3 * x + p2) * x + p1) * x + p0
        return result

    def _eval_natural_cubic(self, x):
        if x <= self[0].current.x:
            left_most_keyframe = self[0]
            result = left_most_keyframe.current.y - \
                     left_most_keyframe.left_tangent * (left_most_keyframe.current.x - x)
            return result

        if x >= self[-1].current.x:
            right_most_keyframe = self[-1]
            result = right_most_keyframe.current.y + \
                     right_most_keyframe.right_tangent * (x - right_most_keyframe.current.x)
            return result

        index = bisect.bisect([k.current.x for k in self], x)
        prev_keyframe = self[index - 1]
        next_keyframe = self[index]

        prev_x = prev_keyframe.current.x
        prev_y = prev_keyframe.current.y
        next_x = next_keyframe.current.x
        next_y = next_keyframe.current.y

        delta_x = next_x - prev_x
        f_z0 = prev_y
        f_z0z1 = prev_keyframe.right_tangent
        f_z1z2 = (next_y - prev_y) / delta_x
        f_z2z3 = next_keyframe.left_tangent
        f_z0z1z2 = (f_z1z2 - f_z0z1) / delta_x
        f_z1z2z3 = (f_z2z3 - f_z1z2) / delta_x
        f_z0z1z2z3 = (f_z1z2z3 - f_z0z1z2) / delta_x

        temp_p0 = x - prev_x
        result = f_z0 + f_z0z1 * temp_p0 + f_z0z1z2 * (temp_p0 ** 2) + f_z0z1z2z3 * (x - next_x) * (temp_p0 ** 2)
        return result


class SaveLoadMixin(object):
    @classmethod
    def load(cls, file_path):
        instance = cls()
        if file_path.endswith(u'.curve'):
            instance._load_ascii_file(file_path)
            return instance

        elif file_path.endswith(u'.bcurve'):
            instance._load_binary_file(file_path)
            return instance
        else:
            raise IOError(u'cannot open {}'.format(file_path))

    def _load_ascii_file(self, file_path):
        import json
        with open(file_path, 'r') as jf:
            data = json.load(jf)
            self.extra_data = data['global']
            for k in data['keyframes']:
                self._keyframes.append(KeyFrame(Point2D(*k[0]), Point2D(*k[1]), Point2D(*k[2])))

    def _load_binary_file(self, file_path):
        import os
        total_file_size = os.stat(file_path).st_size
        with open(file_path, 'r') as bf:
            magic, major_version, minor_version = struct.unpack_from('>4s 2h', bf.read(8))
            if magic != 'curv':
                raise ValueError('not a valid binary curve file!')

            while bf.tell() < total_file_size:
                atom = struct.unpack_from('>I 4s', bf.read(8))
                func = getattr(self, '_load_{}_part'.format(atom[1]))
                if func:
                    func(bf, bf.tell() + atom[0] - 8)

    def _load_keyf_part(self, file_obj, end):
        while file_obj.tell() < end:
            values = struct.unpack_from('>6f', file_obj.read(24))
            self._keyframes.append(KeyFrame(Point2D(*values[:2]), Point2D(*values[2:4]), Point2D(*values[4:])))

    def _load_glob_part(self, file_obj, end):
        while file_obj.tell() < end:
            key = ''.join(iter(lambda: file_obj.read(1), '\x00'))
            data_type = struct.unpack_from('>2b', file_obj.read(2))[0]
            func = getattr(self, '_load_glob_value_{}'.format(unpack_fmt_code[data_type].__name__))
            if func:
                value = func(file_obj)
                self.extra_data[key] = value

    def _load_glob_value_str(self, file_obj):
        return ''.join(iter(lambda: file_obj.read(1), '\x00'))

    def _load_glob_value_int(self, file_obj):
        return struct.unpack_from('>i b', file_obj.read(5))[0]

    def _load_glob_value_long(self, file_obj):
        return struct.unpack_from('>l b', file_obj.read(5))[0]

    def _load_glob_value_float(self, file_obj):
        return struct.unpack_from('>f b', file_obj.read(5))[0]

    def save(self, file_path, **kwargs):
        if not all([isinstance(x, str) for x in kwargs]):
            raise ValueError('global keys should all be str')

        if not all([isinstance(x, (str, int, float, long)) for x in kwargs.values()]):
            raise ValueError('global values should all be str')

        if not file_path.endswith(('.curve', '.bcurve')):
            raise ValueError(u'file name should end with .curve or .bcurve')

        if file_path.endswith('.curve'):
            return self._save_ascii_file(file_path, **kwargs)

        if file_path.endswith('.bcurve'):
            return self._save_binary_file(file_path, **kwargs)

    def _save_ascii_file(self, file_path, **kwargs):
        import json
        temp_dict = self.extra_data
        temp_dict.update(kwargs)
        result = {'global': temp_dict, 'keyframes': []}
        for k in self:
            result['keyframes'].append(k.to_list())

        try:
            with open(file_path, 'w') as jf:
                json.dump(result, jf)
                return True
        except Exception as e:
            print e
            return False

    def _save_binary_file(self, file_path, **kwargs):
        magic = 'curv'
        major_version = 0x0000
        minor_version = 0x0001

        with open(file_path, 'wb') as bf:
            bf.write(struct.pack('>4s', magic))
            bf.write(struct.pack('>2h', major_version, minor_version))
            self._write_global_part(bf, **kwargs)
            self._write_keyframe_part(bf)

    def _write_keyframe_part(self, file_obj):
        keyframe_atom = {'size': 0, 'type': 'keyf'}

        if not self._keyframes:
            keyframe_atom['size'] = 8
            file_obj.write(struct.pack('>I 4s', keyframe_atom['size'], keyframe_atom['type']))
            return

        fmt_string = '>{}f'.format(len(self) * 6)
        keyframe_atom['size'] = 8 + struct.calcsize(fmt_string)
        file_obj.write(struct.pack('>I 4s', keyframe_atom['size'], keyframe_atom['type']))

        for k in self:
            file_obj.write(struct.pack('>6f', k.current.x, k.current.y, k.left.x, k.left.y, k.right.x, k.right.y))

    def _write_global_value_str(self, key, value, file_obj):
        file_obj.write(struct.pack('>{}s b b b{}s b'.format(len(key), len(value)),
                                   key, 0x00, pack_fmt_code[type(value)], 0x00, value, 0x00))

    def _write_global_value_int(self, key, value, file_obj):
        file_obj.write(struct.pack('>{}s b b b i b'.format(len(key)),
                                   key, 0x00, pack_fmt_code[type(value)], 0x00, value, 0x00))

    def _write_global_value_long(self, key, value, file_obj):
        file_obj.write(struct.pack('>{}s b b b l b'.format(len(key)),
                                   key, 0x00, pack_fmt_code[type(value)], 0x00, value, 0x00))

    def _write_global_value_float(self, key, value, file_obj):
        file_obj.write(struct.pack('>{}s b b b f b'.format(len(key)),
                                   key, 0x00, pack_fmt_code[type(value)], 0x00, value, 0x00))

    def _write_global_part(self, file_obj, **kwargs):
        global_atom = {'size': 0, 'type': 'glob'}

        fmt_string = '>'
        temp_dict = self.extra_data
        temp_dict.update(kwargs)
        ordered_values = temp_dict.items()
        for key, value in ordered_values:
            fmt_string += '{key}s b b b {value} b '.format(key=len(key),
                                                           value=pack_fmt_func[type(value)](value))
        global_atom['size'] = 8 + struct.calcsize(fmt_string)
        file_obj.write(struct.pack('>I', global_atom['size']))
        file_obj.write(struct.pack('>4s', global_atom['type']))

        for key, value in ordered_values:
            func = getattr(self, '_write_global_value_{}'.format(type(value).__name__), None)
            if func:
                func(key, value, file_obj)
            else:
                raise TypeError('no function for {}: {}'.format(key, value))
