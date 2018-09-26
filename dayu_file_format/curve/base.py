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

    @property
    def duration(self):
        if self._keyframes:
            return self[-1].current.x - self[0].current.x
        return 0

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

    @data_type_validation(KeyFrame=KeyFrame)
    def remove(self, keyframe):
        self._keyframes.remove(keyframe)

    @data_type_validation(x=(int, float))
    def find_nearest_keyframe(self, x):
        if x <= self[0].current.x:
            return self[0]
        if x >= self[-1].current.x:
            return self[-1]

        index = bisect.bisect([k.current.x for k in self], x)
        if (x - self[index - 1].current.x) <= (self[index].current.x - x):
            return self[index - 1]
        else:
            return self[index]

    def clear(self):
        try:
            self.extra_data = {}
            self._keyframes = []
            return True
        except Exception as e:
            return False
