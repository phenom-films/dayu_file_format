#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import inspect
from functools import wraps


def data_type_validation(**validation):
    def outter_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            call_args = inspect.getcallargs(func, *args, **kwargs)
            call_args.pop(inspect.getargspec(func).args[0], None)
            for k, v in call_args.items():
                if validation.has_key(k) and (not isinstance(v, validation.get(k))):
                    raise ValueError('{} except type: {}'.format(k, validation.get(k)))

            return func(*args, **kwargs)

        return wrapper

    return outter_wrapper
