#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

pack_fmt_func = {str  : lambda v: '{}s'.format(len(v)),
                 int  : lambda v: 'i',
                 long : lambda v: 'l',
                 float: lambda v: 'f'}
pack_fmt_code = {str  : 0x01,
                 int  : 0x02,
                 long : 0x04,
                 float: 0x08}

unpack_fmt_code = dict(zip(pack_fmt_code.values(), pack_fmt_code.keys()))
