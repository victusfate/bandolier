import hashlib
import json
import os
import shutil
import tempfile
import requests
from . import constants

def sha1_str(s: str):
  return hashlib.sha1(s.encode('utf-8')).hexdigest()

def sha1_dict(d: dict):
  s = json.dumps(d,sort_keys=True)
  return sha1_str(s)

def sha1_file(path_to_file: str):
  BLOCKSIZE = 65536
  m = hashlib.sha1()
  with open(path_to_file, 'rb') as afile:
      buf = afile.read(BLOCKSIZE)
      while len(buf) > 0:
          m.update(buf)
          buf = afile.read(BLOCKSIZE)
  return m.hexdigest()


# returns if file successfully fetched
def fetch_url(url:str,local_file:str):
  try:
    response = requests.get(url, stream=True)
    local_buffer = open(local_file, 'wb')
    shutil.copyfileobj(response.raw, local_buffer)
    del response
    local_buffer.close()
    return True
  except Exception as err:
    # TODO convert print to log.err
    print('fetch_url.err',err)
  return False


# returns { 'medium_id': medium_id, 'local_path': local_path  } local_path set if cleanup False
def hash_url(url:str,file_base_name:str='img.jpg',cleanup:bool=True):
  medium_id = constants.EMPTY_SHA1 # default to sha1 of empty string
  local_path = None
  temp_dir = tempfile.mkdtemp()
  try:
    local_path = os.path.join(temp_dir,file_base_name)
    fetched  = fetch_url(url,local_path)
    if fetched:
      medium_id = sha1_file(local_path)
  except Exception as err:
    # TODO convert print to log.err
    print('hash_url.err',err)
  finally:
    if cleanup:
      shutil.rmtree(temp_dir)
  return { 'medium_id':medium_id,'local_path':local_path }
