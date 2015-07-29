# -*- coding: utf-8 -*-
from bson.objectid import ObjectId
from cerberus.cerberus import Validator
from cerberus.errors import ERROR_BAD_TYPE
import re


_URL_REGEX = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


_EMAIL_REGEX = re.compile(
    # dot-atom
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
    # quoted-string
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'
    # domain (max length of an ICAAN TLD is 22 characters)
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,253}[A-Z0-9])?\.)+[A-Z]{2,22}$', re.IGNORECASE
)


class CustomValidator(Validator):
    def _validate_type_object_id(self, field, value):
        if not isinstance(value, ObjectId):
            self._error(field, ERROR_BAD_TYPE.format('ObjectId'))

    def _validate_type_location(self, field, value):
        try:
            all([isinstance(value[0], float), isinstance(value[1], float)])
        except Exception as e:
            self._error(field, ERROR_BAD_TYPE.format('Location'))

    def _validate_type_url(self, field, value):
        if not _URL_REGEX.match(value):
            self._error(field, ERROR_BAD_TYPE.format('Url'))

    def _validate_type_email(self, field, value):
        if not _EMAIL_REGEX.match(value):
            self._error(field, ERROR_BAD_TYPE.format('Email'))