import requests

# oauth 
def get_token(auth_url,headers,client_id,client_secret,scope):
  r = requests.post(auth_url,
    headers=headers,
    json={
      'client_id': client_id,
      'grant_type': 'client_credentials',
      'client_secret': client_secret,
      'scope': scope
    }
  )
  # print('response',r.json())
  data = r.json()
  token = None
  expires_in = None
  if 'access_token' in data:
    token = data['access_token']
  if 'expires_in' in data:
    expires_in = data['expires_in']
  return token,expires_in
