# -*- coding: utf-8 -*-


class ClientError(Exception):
    """Raised when there is an exception occurs for YoMongoClient"""
    pass


class DbError(Exception):
    """Raised when error occurs for YoDb"""
    pass


class SchemaInitError(Exception):
    """Raised when initialize a schema with bad fields"""
    pass


class SchemaValidationError(Exception):
    """Raised when a document is not valid for Schema"""
    pass


class DocumentActionError(Exception):
    """Raised when unable to do an action on a document"""
    pass