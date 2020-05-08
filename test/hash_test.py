import bandolier
from bandolier import constants
from bandolier import hash

print('hash string foo bar',hash.sha1_str('foo bar'))
print('hash dictionary { "foo": "bar" }',hash.sha1_dict({  'foo': 'bar'}))
print('hash file this one',hash.sha1_file('./hash_test.py'))
print('hash empty string',hash.sha1_str(''))
print('hash empty file',hash.sha1_str('./empty_file.txt'))

# ❯ shasum /var/folders/pf/cn6tk67n1yx6yqmwy7x7tfy80000gn/T/tmpnm0_3fk9/img.jpg
# acf38b520554dc1ae651c1517b41d365e030b252  /var/folders/pf/cn6tk67n1yx6yqmwy7x7tfy80000gn/T/tmpnm0_3fk9/img.jpg
print('hash file',hash.hash_url('https://raw.githubusercontent.com/welcotravel/3d-photo-inpainting/master/photo_3d/image/moon.jpg'))
print('hash should be acf38b520554dc1ae651c1517b41d365e030b252')