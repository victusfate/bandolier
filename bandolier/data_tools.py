

def consul_to_dict(consul_list):
  d2 = {}
  if consul_list:
    for obj in consul_list:
      d2[obj['Key']] = obj['Value'].decode()
  return d2

def flat_to_nested(d1,delimiter='/'):
  d2 = {}
  if d1:
    for key_path,obj in d1.items():
      keys = key_path.split(delimiter)
      child = d2
      for i,key in enumerate(keys):
        if key not in child:
          if i == len(keys) - 1:
            child[key] = obj
          else:
            child[key] = {}
        child = child[key]
  return d2

def consul_to_nested_dict(consul_list):
  d2 = consul_to_dict(consul_list)
  return flat_to_nested(d2)
