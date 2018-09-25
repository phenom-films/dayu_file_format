#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import bisect
from mixin import SaveLoadMixin
from collections import Iterable
from data_structure import *


class Curve(SaveLoadMixin):
    def __init__(self):
        super(Curve, self).__init__()
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

    def eval(self, x, method='hermite'):
        pass


if __name__ == '__main__':
    import time

    cc = Curve()

    for x in range(2880):
        cc.add(KeyFrame(Point2D(x, x + 1)))

    start = time.time()
    cc.save('/Users/andyguo/Desktop/curve.bcurve', name='sdf', haha=123, ff=12.5)
    print time.time() - start

    start = time.time()
    cc.save('/Users/andyguo/Desktop/curve.curve', name='sdf', haha=123, ff=12.5)
    print time.time() - start

    bb = Curve()
    start = time.time()
    bb.load('/Users/andyguo/Desktop/curve.bcurve')
    print time.time() - start

    bb = Curve()
    start = time.time()
    bb.load('/Users/andyguo/Desktop/curve.curve')
    print time.time() - start
