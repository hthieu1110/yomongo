# -*- coding: utf-8 -*-


class CursorBinder(object):
    def __init__(self, cursor, doc_cls):
        self.cursor = cursor
        self.cls = doc_cls
        self.start = 0
        self.stop = self.count()
        self.step = 1
        self.current = 0

    def __iter__(self):
        if self.start:
            self.current = self.start
            for i in xrange(self.start):
                self.cursor.next()

        while self.current < self.stop:
            yield self.cls(**self.cursor.next())
            self.current += self.step

    def __len__(self):
        return self.cursor.count()

    def __getitem__(self, item):
        if isinstance(item, int):
            for i in xrange(item):
                self.cursor.next()
            return self.cls(**self.cursor.next())
        elif isinstance(item, slice):
            self.start = item.start
            self.stop = item.stop
            self.step = item.step or self.step
            return self

    def count(self):
        return self.__len__()

    def to_list(self):
        return list(self.__iter__())

    def to_view(self, name=None):
        return [doc.to_view(name) for doc in self.__iter__()]