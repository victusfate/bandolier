import hashlib
import json

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
