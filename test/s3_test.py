import os
import json
import bandolier
from bandolier import constants


from bandolier.s3util import S3

# my local test 
s3 = S3(bucket_name='dev.welco.me',profile_name='welco',region_name='us-east-1')

data = { 'hash' : 'something' }

s3.put('./s3_test.py','test/s3_test.py','text/plain')
s3.put_data(json.dumps(data).encode('utf-8'),'test/stuff.json','application/json')
print('get_data s3_test.py')
print(s3.get_data('test/s3_test.py'))
print('end get_data s3_test.py\n\n\n')
s3.get('test/s3_test.py','/tmp/s3_test.py')
print('get_data stuff.json',s3.get_data('test/stuff.json'))
s3.get('test/stuff.json','/tmp/stuff.json')

print('contents of uploaded/downloaded s3_test.py')
os.system('cat /tmp/s3_test.py')
print('contents of uploaded/downloaded stuff.json')
os.system('cat /tmp/stuff.json')
print('end contents cat\n\n\n')

most_recent = s3.most_recent('test')
print('most recent object',most_recent)

s3.remove('test/s3_test.py') 
s3.remove('test/stuff.json')

os.system('rm /tmp/s3_test.py')
os.system('rm /tmp/stuff.json')

print('done')