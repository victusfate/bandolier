import os
import json
import bandolier
from bandolier import constants

# my local test 
constants.CONFIG['aws']['profile'] = 'welco'
constants.CONFIG['aws']['bucket'] = 'dev.welco.me'

from bandolier import s3
from s3 import S3



data = { 'hash' : 'something' }

s3.put('./s3_test.py','recommender/s3_test.py','text/plain')
s3.put_data(json.dumps(data).encode('utf-8'),'recommender/stuff.json','application/json')
print('get_data s3_test.py')
print(s3.get_data('recommender/s3_test.py'))
print('end get_data s3_test.py\n\n\n')
s3.get('recommender/s3_test.py','/tmp/s3_test.py')
print('get_data stuff.json',s3.get_data('recommender/stuff.json'))
s3.get('recommender/stuff.json','/tmp/stuff.json')

print('contents of uploaded/downloaded s3_test.py')
os.system('cat /tmp/s3_test.py')
print('contents of uploaded/downloaded stuff.json')
os.system('cat /tmp/stuff.json')
print('end contents cat\n\n\n')

most_recent = s3.most_recent('recommender')
print('most recent object',most_recent)

s3.remove('recommender/s3_test.py') 
s3.remove('recommender/stuff.json')

os.system('rm /tmp/s3_test.py')
os.system('rm /tmp/stuff.json')

print('done')