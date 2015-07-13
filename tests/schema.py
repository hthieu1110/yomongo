from yomongo.exceptions import SchemaInitError
from yomongo.schema import Schema
from yomongo.fields import Str, Datetime, Int
from datetime import datetime

bs = Schema()
assert bs._doc == {}
assert bs._schema == {}


# Test default value
class MyDoc(Schema):
    age = Int()
    name = Str(default='My name')
    dt = Datetime(default=datetime.utcnow)


class MySchema(Schema):
    _custom_fields = ['age', 'full_name']

    name = Str(maxlength=10)

    @property
    def age(self):
        return 10

    @property
    def full_name(self):
        return 'My name is %s' % self.name



MySchema.add_view('all')
MySchema.add_view('full1', ['full_name'])
MySchema.add_view('full2', ['full_name', 'age'], exclude=['age'])
MySchema.add_view('full3', exclude=['age', 'name'])

my = MySchema(name='Hieu')

assert my.to_view('all') == {'age': 10, 'name': 'Hieu', 'full_name': 'My name is Hieu'}
assert my.to_view('full1') == my.to_view('full2')
assert my.to_view('full2') == my.to_view('full3')

my = MySchema(name="Hello")
assert my._doc == {'name': 'Hello'}
assert my._schema == {'name': {'required': True, 'type': 'string', 'maxlength': 10}}
assert my.name == 'Hello'
assert my._id == None


try:
    Schema(content='new')
    assert False
except SchemaInitError:
    assert True


print 'Test OK'


