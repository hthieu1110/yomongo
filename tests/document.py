from datetime import datetime
from bson.errors import InvalidId
from yomongo.client import Client
from yomongo.exceptions import SchemaValidationError
from yomongo.document import Document
from yomongo import fields


MODB2 = {
    'tss_db': {
        'host': 'dogen.mongohq.com:10011',
        'user': 'user_rw',
        'password': 'user_rw'
    }
}

MODB = {
    'test': {
        'host': 'localhost',
        'user': 'root',
        'password': ''
    }
}

client = Client(MODB)


class MyUser(Document):
    name = fields.Str(maxlength=5)

# Clean test
MyUser._collection.delete_many({})

assert list(MyUser._collection.find()) == []

# Begin of: Test create and save user with attr in __init__ and setter
user = MyUser()
assert user._id == None

try:
    user.save()
except SchemaValidationError as e:
    assert e.message == {'name': 'required field'}

try:
    user.name = 'Hieu haha'
except SchemaValidationError as e:
    assert e.message == {'name': 'max length is 5'}

user.name = 'Hieu'
user.save()
id = user._id
assert id is not None
assert MyUser._collection.find()[0]['name'] == 'Hieu'

user.name = 'Lobo'
user.save()
assert user._id == id
assert MyUser._collection.find()[0]['name'] == 'Lobo'


_id_orig = user._id
user._id = 'error'
try:
    user.save()
except InvalidId:
    assert True
user._id = _id_orig

_user = MyUser.get(_id_orig)
assert _user.name == user.name
assert _user.name == 'Lobo'


MyUser(name='tata').save()
users = MyUser.filter()
assert users.count() == 2
assert len(users) == 2

users = MyUser.filter({'name': 'Lobo'})
assert MyUser.filter()[0].name == 'Lobo'

MyUser(name='tutu').save()
assert MyUser.filter().count() == 3
# End of: Test create and save user with attr in __init__ and setter


# Begin of: Test default value
class YourUser(Document):
    _collection_name = 'my_user'

    age = fields.Int(default=10)
    dt = fields.Datetime(default=datetime.utcnow)
    name = fields.Str()

try:
    u = YourUser()
except SchemaValidationError as e:
    assert e.message == {'name': 'required field'}

u.name = 'Hieu'
u.save()
assert True
# End of: Test default value


# # List 3 users
# print list(MyUser.filter())
# print list(MyUser.filter()[0:3:2])
#
# # get user 1
# print MyUser.filter()[0]
# # get user 2
# print MyUser.filter()[1]
# # get user 3
# print MyUser.filter()[2]
#
# # Get list of [user 1]
# print list(MyUser.filter()[:1])
# # Get list of [user 2]
# print list(MyUser.filter()[1:2])
# # Get list of [user 2, user 3]
# print list(MyUser.filter()[1:3])
#
# # Get list of [user 2, 3]
# print list(MyUser.filter()[1:10])
#
# # List empty
# print list(MyUser.filter()[5:10])

# Clean test
# MyUser._collection.delete_many({})

print 'Test OK'