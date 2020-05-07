import bandolier
from bandolier import constants
from bandolier import hash

print('hash string foo bar',hash.sha1_str('foo bar'))
print('hash dictionary { "foo": "bar" }',hash.sha1_dict({  'foo': 'bar'}))
print('hash file this one',hash.sha1_file('./hash_test.py'))
print('hash empty string',hash.sha1_str(''))
print('hash empty file',hash.sha1_str('./empty_file.txt'))
