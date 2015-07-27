# -*- coding: utf-8 -*-
from bson.objectid import ObjectId
from cerberus.cerberus import Validator
from cerberus.errors import ERROR_BAD_TYPE


class CustomValidator(Validator):
    def _validate_type_object_id(self, field, value):
        if not isinstance(value, ObjectId):
            self._error(field, ERROR_BAD_TYPE.format('ObjectId'))

    def _validate_type_location(self, field, value):
        try:
            all([isinstance(value[0], float), isinstance(value[1], float)])
        except Exception as e:
            self._error(field, ERROR_BAD_TYPE.format('Location'))