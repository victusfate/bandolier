import requests
import os
import time
import json

class NomadWrapper :
  def __init__(self,url):
    self.base_url = url
    print('NomadWrapper.__init__ base_url',self.base_url)

  def allocation(self,allocation_id: str):
    url = self.base_url +'/v1/allocations?prefix='+allocation_id
    print('NomadWrapper.allocation base_url',self.base_url)
    print('NomadWrapper.allocation url',url)
    r = requests.get(url)
    r = r.json()
    print('NomadWrapper.allocation',json.dumps(r,indent=2))
    return r

  def allocationStatus(self,allocation_id: str):
    allocations = self.allocation(allocation_id)
    status = None
    for allocation in allocations:
      if 'ClientStatus' in allocation:
        status = allocation['ClientStatus']
        break
    print('NomadWrapper.allocationStatus',status)
    return status

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


  def restart_allocations(self,allocations,sleep_between_restarts = 10):
    results = []
    for alloc_id in allocations:
      url = self.base_url + os.path.join('/v1/client/allocation/',alloc_id,'restart')
      print('NomadWrapper.restart_allocations url',url)
      r = requests.post(url,json={})
      results.append({'id': alloc_id,'response':r.json()})
      time.sleep(sleep_between_restarts)
    return results

  def restart_job(self,job_id):
    # first fetch job
    get_job_url = self.base_url + os.path.join('/v1/job',job_id)
    get_job_response = requests.get(get_job_url)
    job = get_job_response.json()
    job = { 'Job': job }
    
    # now post it back
    post_url = self.base_url + os.path.join('/v1/jobs')
    post_job_response = requests.post(post_url,json=job)
    print('restart job response',post_job_response.json())
    return post_job_response.json()