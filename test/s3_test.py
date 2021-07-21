import os
import json
import bandolier
from bandolier import constants

from bandolier import s3util
from bandolier.s3util import S3

# bucket_name = 'internal.dev.welco.me'
# acl = s3util.ACL_BUCKET_OWNER_FULL_CONTROL

bucket_name = 'd2.welco.me'
acl = s3util.ACL_PUBLIC_READ

# my local test 
s3 = S3(bucket_name=bucket_name,region_name='us-east-1',profile_name='welco')

data = { 'hash' : 'something' }

s3.put('./foo.txt','test/foo.txt','text/plain',acl)
s3.put_data(json.dumps(data).encode('utf-8'),'test/stuff.json','application/json',acl)

print('get_data foo.txt')
print(s3.get_data('test/foo.txt'))
print('foo.txt exists?',s3.exists('test/foo.txt'))
print('doesNotExists.txt exists?',s3.exists('test/doesNotExists.txt'))
print('\nend get_data foo.txt\n\n\n')
s3.get('test/foo.txt','/tmp/foo.txt')
print('get_data stuff.json',s3.get_data('test/stuff.json'))
s3.get('test/stuff.json','/tmp/stuff.json')

print('contents of uploaded/downloaded foo.txt')
os.system('cat /tmp/foo.txt')
print('contents of uploaded/downloaded stuff.json')
os.system('cat /tmp/stuff.json')
print('\nend contents cat\n\n\n')

most_recent = s3.most_recent('test')
print('most recent object',most_recent)


os.system('rm /tmp/stuff.json')

s3_url = 's3://d2.welco.me/test/stuff.json'
http_url = 'https://s3.amazonaws.com/d2.welco.me/test/stuff.json'
print(s3.parse_s3_url(s3_url))
s3.get_s3_file(s3_url,'/tmp/stuff.json')
os.system('cat /tmp/stuff.json')
print('\nend contents cat\n\n\n')

os.system('rm /tmp/stuff.json')

s3.fetch_http_or_s3_file(s3_url,'/tmp/stuff.json')
print('fetch_http_or_s3_file s3_url',s3_url,' to /tmp/stuff.json')
os.system('cat /tmp/stuff.json')
print('\nend contents cat\n\n\n')
os.system('rm /tmp/stuff.json')

s3.fetch_http_or_s3_file(http_url,'/tmp/stuff.json')
print('fetch_http_or_s3_file http_url',http_url,' to /tmp/stuff.json')
os.system('cat /tmp/stuff.json')
print('\nend contents cat\n\n\n')
os.system('rm /tmp/stuff.json')

s3.remove('test/foo.txt') 
s3.remove('test/stuff.json')

os.system('rm /tmp/foo.txt')
os.system('rm /tmp/stuff.json')

print('done')