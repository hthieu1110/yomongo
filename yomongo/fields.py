# -*- coding: utf-8 -*-
from utils import camel_to_snake


class BaseField(object):
    """Base field for Schema.

    Each field correspond to one definition in Cerberus schema
    By default, a field is required.
    """
    def __init__(self, **kwargs):
        self.definition = kwargs
        self.definition['type'] = self.type
        self.definition['required'] = self.definition.get('required', True)

    def __call__(self, *args, **kwargs):
        self.definition.update(kwargs)
        return self

    @property
    def type(self):
        """Get type compatible with Cerberus by converting class name
        from camel case to snake case

        :return: (str) snake case version of class name
        """
        return camel_to_snake(self.__class__.__name__.replace('Field', ''))


# Cerberus base types
class String(BaseField): pass
class Integer(BaseField): pass
class Float(BaseField): pass
class Number(BaseField): pass
class Boolean(BaseField): pass
class Datetime(BaseField): pass
class Dict(BaseField): pass
class List(BaseField): pass
class Set(BaseField): pass
class ObjectId(BaseField): pass
class Location(BaseField): pass

# Shortcuts
class Str(String): type = 'string'
class Int(Integer): type = 'integer'
class Num(Number): type = 'number'
class Bool(Boolean): type = 'boolean'
class Loc(Location): type = 'location'