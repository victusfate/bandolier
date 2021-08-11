import requests

# oauth 
def get_token(auth_url,client_id,client_secret,scope):
  r = requests.post(auth_url,json={
    'client_id': client_id,
    'grant_type': 'client_credentials',
    'client_secret': client_secret,
    'scope': scope
  })
  print('response',r.json())
  data = r.json()
  token = None
  if 'access_token' in data:
    token = data['access_token']
  return token
