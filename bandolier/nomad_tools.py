import requests
import os

class NomadWrapper :
  def __init__(self,url):
    self.base_url = url
    print('NomadWrapper.__init__ base_url',self.base_url)

  def allocations(self,job_type: str,client_status = 'running'):
    url = self.base_url + os.path.join('/v1/job',job_type,'allocations')
    print('NomadWrapper.allocations base_url',self.base_url)
    print('NomadWrapper.allocations url',url)
    r = requests.get(url)
    r = r.json()
    out = []
    for allocation in r:
      if 'ClientStatus' in allocation and allocation['ClientStatus'] == client_status:
        out.append(allocation)
    return out


  def restart_allocations(self,allocations):
    results = []
    for alloc_id in allocations:
      url = self.base_url + os.path.join('/v1/client/allocation/',alloc_id,'restart')
      print('NomadWrapper.restart_allocations url',url)
      r = requests.post(url,json={})
      results.append({'id': alloc_id,'response':r.json()})
    return results