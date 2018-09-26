#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import bisect
from collections import Iterable

from data_structure import data_type_validation, KeyFrame, Point2D
from mixin import SaveLoadMixin, InterpolationMixin


class Curve(SaveLoadMixin, InterpolationMixin):
    def __init__(self):
        super(Curve, self).__init__()
        self.extra_data = {}
        self._keyframes = []

    def __len__(self):
        return len(self._keyframes)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._keyframes[item]

    def __iter__(self):
        for keyframe in self._keyframes:
            yield keyframe

    @data_type_validation(keyframe=KeyFrame)
    def add(self, keyframe):
        index = bisect.bisect([k.current.x for k in self], keyframe.current.x)
        self._keyframes.insert(index, keyframe)

    @data_type_validation(keyframes=Iterable)
    def extend(self, keyframes):
        for k in keyframes:
            self.add(k)

    @data_type_validation(index=int)
    def pop(self, index=-1):
        return self._keyframes.pop(index)
