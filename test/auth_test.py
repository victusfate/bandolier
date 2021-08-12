import os
import sys
import json
import bandolier
import requests
from bandolier import constants

from bandolier import auth

if len(sys.argv) < 6:
  print('usage: ' + sys.argv[0] + ' <auth_url> <client_id> <client_secret> <scope> <test_url>')
  exit(0)

auth_url      = sys.argv[1]
client_id     = sys.argv[2]
client_secret = sys.argv[3]
scope         = sys.argv[4]
test_url      = sys.argv[5]
token,expires_in = auth.get_token(auth_url=auth_url,client_id=client_id,client_secret=client_secret,scope='services')
print('token',token,'expires_in',expires_in)

# lets try a get request
r = requests.get(test_url,headers={'Authorization': 'Bearer ' + token})
print(r.json())