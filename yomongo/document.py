# -*- coding: utf-8 -*-
from bson import ObjectId

from utils import classproperty, camel_to_snake
from client import Client

from schema import Schema
from werkzeug.exceptions import NotFound
from yomongo.cursor import YoCursor
from yomongo.exceptions import DocumentActionError


class Document(Schema):
    """Base model used for definition of all YoMongo Model"""

    def __init__(self, **kwargs):
        super(Document, self).__init__(**kwargs)

    @classproperty
    def _db_name(cls):
        return Client.default_db_name

    @classproperty
    def _db(cls):
        """Get DataBase instance"""
        return Client.connected_databases[cls._db_name]

    @classproperty
    def _collection_name(cls):
        """Get name of collection by converting class name to snake case"""
        return camel_to_snake(cls.__name__)

    @classproperty
    def _collection(cls):
        """Access to Collection instance"""
        return cls._db[cls._collection_name]

    @classmethod
    def get(cls, _id=None, **kwargs):
        """Like find_one but take _id directly or filter from kwargs,
        so we can not pass the options. Use find_one if need options
        """
        if _id is not None:
            if not isinstance(_id, ObjectId):
                _id = ObjectId(_id)
            filter_or_id = _id
        else:
            filter_or_id = kwargs
        doc = cls._collection.find_one(filter_or_id)
        if doc:
            return cls(**doc)
        return None

    @classmethod
    def get_or_404(cls, _id=None, **kwargs):
        result = cls.get(_id, **kwargs)
        if not result:
            raise NotFound('{} not found'.format(cls.__name__))
        return result

    @classmethod
    def filter(cls, **kwargs):
        """Like find but take filter from kwargs and we can not pass options"""
        return YoCursor(cls, kwargs)

    @classmethod
    def find(cls, *args, **kwargs):
        """Find a document but bind the result to the corresponding model of collection"""
        return YoCursor(cls, *args, **kwargs)

    @property
    def id(self):
        return getattr(self, self._pk)

    def update(self, **new_values):
        """Update the current document we new values"""
        self._doc.update(new_values)
        self.save()
        return self

    def save(self, force_insert=False):
        """Save a document.

        If document is instance of an existing document then update
        If a new document instance then create a new one
        """
        self.validate()

        if self._id and not force_insert:
            self._collection.replace_one({"_id": self._id}, self._doc, upsert=True)
        else:
            result = self._collection.insert_one(self._doc)
            self._doc['_id'] = result.inserted_id
        return self

    def remove(self):
        if not self._id:
            raise DocumentActionError('Cannot remove an empty document')

        result = self._collection.delete_one({"_id": self._id})
        if not result.deleted_count:
            raise DocumentActionError('Document "{}" does not exist'.format(self._id))

        self._doc = {}
        return self
