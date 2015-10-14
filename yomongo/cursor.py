# -*- coding: utf-8 -*-
from pymongo.cursor import Cursor


class YoCursor(Cursor):
    def __init__(self, cls, *args, **kwargs):
        self.cls = cls
        super(YoCursor, self).__init__(cls._collection, *args, **kwargs)

        self._start = 0
        self._stop = self.count()
        self._step = 1
        self._current = 0

    def __iter__(self):
        if self._start:
            self._current = self._start
            for i in xrange(self._start):
                self.next()

        while self._current < self._stop:
            yield self.cls(**self.next())
            self._current += self._step

    def __len__(self):
        return self.count()

    def __getitem__(self, item):
        if isinstance(item, int):
            for i in xrange(item):
                self.next()
            return self.cls(**self.next())
        elif isinstance(item, slice):
            self._start = item.start
            self._stop = item.stop
            self._step = item.step or self._step
            return self

    def remove(self):
        for item in self.__iter__():
            item.remove()

    def to_list(self):
        return list(self.__iter__())

    def to_view(self, name=None):
        return [doc.to_view(name) for doc in self.__iter__()]