# -*- coding: utf-8 -*-
import re


def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class classproperty(property):
    def __get__(self, cls, owner):
        return self.fget(owner)


class cached_classproperty(property):
    _cached = {}

    def __get__(self, cls, owner=None):
        _cached = self.__class__._cached
        _owner_id = id(owner)
        _attr_id = id(self.fget)

        if _owner_id not in _cached:
            _cached[_owner_id] = {}

        if _attr_id not in _cached[_owner_id]:
            _cached[_owner_id][_attr_id] = self.fget(owner)

        return _cached[_owner_id][_attr_id]