import os
import sys
import json
import bandolier
import requests
from bandolier import constants

from bandolier import auth

if len(sys.argv) < 7:
  print('usage: ' + sys.argv[0] + ' <auth_url> <host_url> <client_id> <client_secret> <scope> <test_url>')
  exit(0)

auth_url      = sys.argv[1]
host_url      = sys.argv[2]
client_id     = sys.argv[3]
client_secret = sys.argv[4]
scope         = sys.argv[5]
test_url      = sys.argv[6]
headers = {}
headers['Host'] = host_url
token,expires_in = auth.get_token(auth_url=auth_url,headers=headers,client_id=client_id,client_secret=client_secret,scope='services')
print('token',token,'expires_in',expires_in)

# lets try a get request
r = requests.get(test_url,headers={'Authorization': 'Bearer ' + token})
print(r.json())