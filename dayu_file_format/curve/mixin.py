#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import struct
from config import *
from data_structure import *
import os


class SaveLoadMixin(object):
    def load(self, file_path):
        if file_path.endswith(u'.curve'):
            pass

        elif file_path.endswith(u'.bcurve'):
            self._load_binary_file(file_path)

        else:
            raise IOError(u'cannot open {}'.format(file_path))

    def _load_binary_file(self, file_path):
        total_file_size = os.stat(file_path).st_size
        with open(file_path, 'r') as bf:
            magic, major_version, minor_verion = struct.unpack_from('>4s 2h', bf.read(8))
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
            self.add(KeyFrame(Point2D(*values[:2]), Point2D(*values[2:4]), Point2D(*values[4:])))

    def _load_glob_part(self, file_obj, end):
        while file_obj.tell() < end:
            key = ''.join(iter(lambda: file_obj.read(1), '\x00'))
            data_type = struct.unpack_from('>2b', file_obj.read(2))[0]
            func = getattr(self, '_load_glob_value_{}'.format(unpack_fmt_code[data_type].__name__))
            if func:
                value = func(file_obj)
                setattr(self, key, value)

    def _load_glob_value_str(self, file_obj):
        return ''.join(iter(lambda: file_obj.read(1), '\x00'))

    def _load_glob_value_int(self, file_obj):
        return struct.unpack_from('>i b', file_obj.read(5))[0]

    def _load_glob_value_long(self, file_obj):
        return struct.unpack_from('>l b', file_obj.read(5))[0]

    def _load_glob_value_float(self, file_obj):
        return struct.unpack_from('>f b', file_obj.read(5))[0]

    def save(self, file_path, **kwargs):
        if not file_path.endswith(('.curve', '.bcurve')):
            raise ValueError(u'file name should end with .curve or .bcurve')

        if file_path.endswith('.curve'):
            return self._save_ascii_file(file_path, **kwargs)

        if file_path.endswith('.bcurve'):
            return self._save_binary_file(file_path, **kwargs)

    def _save_ascii_file(self, file_path, **kwargs):
        import json
        result = {'global': kwargs, 'keyframes': []}
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

        if not all([isinstance(x, str) for x in kwargs]):
            raise ValueError('global keys should all be str')

        if not all([isinstance(x, (str, int, float, long)) for x in kwargs.values()]):
            raise ValueError('global values should all be str')

        with open(file_path, 'w') as bf:
            bf.write(struct.pack('>4s', magic))
            bf.write(struct.pack('>2h', major_version, minor_version))
            self._write_global_part(bf, **kwargs)
            self._write_keyframe_part(bf)

    def _write_keyframe_part(self, file_obj):
        keyframe_atom = {'size': 0, 'type': 'keyf'}

        if not self._keyframes:
            keyframe_atom['size'] = 8
            file_obj.write('>I 4s', keyframe_atom['size'], keyframe_atom['type'])
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
        ordered_values = kwargs.items()
        for key, value in ordered_values:
            fmt_string += '{key}s b b b {value} b '.format(key=len(key),
                                                           value=pack_fmt_func[type(value)](value))
        print fmt_string
        global_atom['size'] = 8 + struct.calcsize(fmt_string)
        file_obj.write(struct.pack('>I', global_atom['size']))
        file_obj.write(struct.pack('>4s', global_atom['type']))

        for key, value in ordered_values:
            func = getattr(self, '_write_global_value_{}'.format(type(value).__name__), None)
            if func:
                func(key, value, file_obj)
            else:
                raise TypeError('no function for {}: {}'.format(key, value))
