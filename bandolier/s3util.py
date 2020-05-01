import os
import json
import boto3
import sys
import subprocess
from sys import platform
from typing import Optional

class S3:
  def __init__(self,bucket_name: str, profile_name: Optional[str], region_name: str):
    self.session = None
    if profile_name:
      self.session = boto3.Session(profile_name=profile_name,region_name=region_name)
    else:
      self.session = boto3.Session(region_name=region_name)

    self.profile_name = profile_name
    self.bucket_name  = bucket_name
    self.region_name  = region_name
    self.s3           = self.session.resource('s3')
    self.bucket       = self.s3.Bucket(self.bucket_name)

  # method depends on aws cli installed locally
  def most_recent(self,under_path):
    cmd_find = "aws s3 ls --recursive s3://" + self.bucket_name + '/' + under_path + " | sort -r | head -n 1 | awk '{print $4}'"
    return subprocess.check_output(cmd_find,stderr=subprocess.STDOUT,shell=True).decode('utf-8').strip()

  def get_s3_url(self,base):
    return 's3://' + self.bucket_name + '/' + base

  def put_data(self,data,destination,content_type='application/octet-stream'):
    return self.bucket.put_object(
      ACL='bucket-owner-full-control',
      Body=data,
      Key=destination,
      ContentType = content_type
    )

  def put(self,local,destination,content_type='application/octet-stream'):
    return self.bucket.upload_file(
      local,
      destination,
      ExtraArgs={
          'ContentType' : content_type
      })

  def get(self,remote,local):
    return self.bucket.download_file(remote,local)

  # returns contents of s3 object
  def get_data(self,remote,encoding='utf-8'):
    obj = self.s3.Object(self.bucket_name, remote)
    body = obj.get()['Body'].read()  
    return body.decode(encoding)

  def remove(self,keys):
    if not isinstance(keys,list):
      keys = [keys]
    objects = []
    for key in keys:
      objects.append({'Key':key})
    return self.bucket.delete_objects(
      Delete={
          'Objects': objects
      }
    )

  def all(self):
    return self.bucket.objects.all()
