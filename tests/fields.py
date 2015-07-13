from yomongo import fields

str_field = fields.String(maxlength=15)
assert str_field.definition == {'required': True, 'type': 'string', 'maxlength': 15}

int_field = fields.Int(allowed=[1, 2])
assert int_field.definition == {'required': True, 'type': 'integer', 'allowed': [1, 2]}


print 'Test OK'
