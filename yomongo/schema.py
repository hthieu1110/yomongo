# -*- coding: utf-8 -*-
from copy import deepcopy
from bson.objectid import ObjectId
from utils import cached_classproperty
from fields import BaseField
from exceptions import SchemaValidationError
from validator import CustomValidator


class Schema(object):
    """Python representation of Cerberus"""
    _views = {
        "default": {'include': None, 'exclude': None}
    }
    _custom_fields = []

    def __init__(self, **kwargs):
        self._doc = {}

        # Set kwargs to schema _doc
        for field, value in kwargs.items():
            if field == '_id':
                if not isinstance(value, ObjectId):
                    value = ObjectId(value)
            self._doc[field] = value

        # Set default value
        # We have to get original definition if field
        # Because definition in schema is cerberus compatible
        # So we have already removed 'default'
        for field in self._schema.keys():
            definition = getattr(self.__class__, field).definition
            if 'default' in definition and field not in self._doc:
                default_value = definition['default']
                if callable(default_value):
                    default_value = default_value()
                self._doc[field] = default_value
        self.validate()

    def __repr__(self):
        return "<{}: {} at {}>".format(
            self.__class__.__name__,
            self._id,
            hex(id(self))
        )

    def __getattribute__(self, name):
        if name != '_doc' and name in self._doc:
            return self._doc[name]
        elif name == '_id' and '_id' not in self._doc:
            return None

        # If value is BaseField instance, it means that:
        # - object has not requested attribute
        # - attribute come from class attribute. This is not a expected behavior
        #
        # So when val is BaseField instance, it's considered that
        # object attribute is not defined yet then return None
        val = super(Schema, self).__getattribute__(name)
        if isinstance(val, BaseField):
            return None
        return val

    def __setattr__(self, name, value):
        if name != '_doc' and name in self._schema or name == '_id':
            self._doc[name] = value
        else:
            super(Schema, self).__setattr__(name, value)

    @cached_classproperty
    def _schema(cls):
        """Return Cerberus schema

        :return: dict
        """
        schema = {}
        for attr_name in cls.__dict__.keys():
            if not attr_name.startswith('_'):
                attr = getattr(cls, attr_name)
                if isinstance(attr, BaseField):
                    _definition = deepcopy(attr.definition)
                    _definition.pop('default', None)
                    schema[attr_name] = _definition
        return schema

    @cached_classproperty
    def _validator(cls):
        """Return the Validator instance of Cerberus"""
        return CustomValidator(cls._schema)

    @classmethod
    def add_view(cls, name, include=None, exclude=None):
        cls._views[name] = {
            'include': include,
            'exclude': exclude
        }

    def validate(self, update=False, context=None):
        """Validate the document against the schema"""
        data = self._doc
        if '_id' in self._doc:
            data = deepcopy(self._doc)
            _id = data.pop('_id', None)
            # Test if _id is valid
            if _id is not None and not isinstance(_id, ObjectId):
                ObjectId(_id)

        if not self._validator.validate(data, update=update, context=context):
            raise SchemaValidationError(self._validator.errors)
        return self._doc

    def to_view(self, name=None, include=None, exclude=None):
        view = self._views[name or 'default']
        _include = include or view['include']
        _exclude = exclude or view['exclude']

        fields = set(_include or self._doc.keys() + self._custom_fields)
        if _exclude:
            fields = fields - set(_exclude)

        results = {}
        for field in fields:
            results[field] = self._doc.get(field, getattr(self, field, None))
        return results

    def to_dict(self):
        return self._doc



    # @classproperty
    # def custom_field(cls):
    #     """Special decorator used for registering the name of all custom field automatically
    #
    #     This is a class property, so we can decorate a method like that
    #     >>> @Schema.custom_field
    #     >>> def my_property(self):
    #     >>>    return 'value'
    #     We use classproperty for having access to current class
    #
    #     When decorating a method with this decorator, we return an object that:
    #         - Register the name of attribute into _custom_fields
    #         - When called, return the value of field
    #     """
    #     class wrapper(object):
    #         def __init__(self, f):
    #             cls._custom_fields.append(f.__name__)
    #             self.f = f
    #
    #         def __get__(self, instance, owner):
    #             if isinstance(instance, owner):
    #                 return self.f(instance)
    #             return super(wrapper, self).__get__(instance, owner)
    #
    #     return wrapper