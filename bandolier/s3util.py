import os
import json
import boto3
import sys
import subprocess
import time
from sys import platform
from typing import Optional


import urllib
from urllib.parse import urlparse


# https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html
# Canned ACL	Applies to	Permissions added to ACL
# private	Bucket and object	Owner gets FULL_CONTROL. No one else has access rights (default).
# public-read	Bucket and object	Owner gets FULL_CONTROL. The AllUsers group (see Who Is a Grantee?) gets READ access.
# public-read-write	Bucket and object	Owner gets FULL_CONTROL. The AllUsers group gets READ and WRITE access. Granting this on a bucket is generally not recommended.
# aws-exec-read	Bucket and object	Owner gets FULL_CONTROL. Amazon EC2 gets READ access to GET an Amazon Machine Image (AMI) bundle from Amazon S3.
# authenticated-read	Bucket and object	Owner gets FULL_CONTROL. The AuthenticatedUsers group gets READ access.
# bucket-owner-read	Object	Object owner gets FULL_CONTROL. Bucket owner gets READ access. If you specify this canned ACL when creating a bucket, Amazon S3 ignores it.
# bucket-owner-full-control	Object	Both the object owner and the bucket owner get FULL_CONTROL over the object. If you specify this canned ACL when creating a bucket, Amazon S3 ignores it.

ACL_PRIVATE                    = 'private'
ACL_PUBLIC_READ                = 'public-read'
ACL_PUBLIC_READ_WRITE          = 'public-read-write'
ACL_AWS_EXEC_READ              = 'aws-exec-read'
ACL_AUTHENTICATED_READ         = 'authenticated-read'
ACL_BUCKET_OWNER_READ          = 'bucket-owner-read'
ACL_BUCKET_OWNER_FULL_CONTROL  = 'bucket-owner-full-control'

DEFAULT_ACL = ACL_PRIVATE

class S3:
  def __init__(self,bucket_name: str, region_name: str, profile_name: Optional[str], aws_key: Optional[str] = None, aws_secret: Optional[str] = None):
    self.session = None
    if aws_key and aws_secret:
      self.session = boto3.Session(region_name=self.region_name,aws_access_key_id=aws_key,aws_secret_access_key=aws_secret)
    elif profile_name:
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

  def parse_s3_url(self,s3_url):
    parsed_s3_url = urlparse(s3_url)
    bucket = parsed_s3_url.netloc
    key = parsed_s3_url.path  
    key = key.lstrip('/')
    return { 'bucket': bucket, 'key': key }

  def put_data(self,data,destination,content_type='application/octet-stream',acl=DEFAULT_ACL):
    return self.bucket.put_object(
      ACL=acl,
      Body=data,
      Key=destination,
      ContentType = content_type
    )

  def put(self,local,destination,content_type='application/octet-stream',acl=DEFAULT_ACL):
    return self.bucket.upload_file(
      local,
      destination,
      ExtraArgs={
          'ACL': acl,
          'ContentType' : content_type
      })

  def get(self,remote,local,retries=0):
    iattempt = 0
    resp = None
    fetched = False
    while not fetched and iattempt <= retries:
      iattempt += 1
      try:
        resp = self.bucket.download_file(remote,local)
        fetched = True
      except Exception as e:
        raise e
      time.sleep(1)
    return resp

  def get_s3_file(self,s3_url,local,retries=0):
    parsed = self.parse_s3_url(s3_url)
    temp_bucket = self.s3.Bucket(parsed['bucket'])
    iattempt = 0
    resp = None
    fetched = False
    while not fetched and iattempt <= retries:
      iattempt += 1
      try:
        resp = temp_bucket.download_file(parsed['key'],local)
        fetched = True
      except Exception as e:
        raise e
      time.sleep(1)
    return resp

  def fetch_http_or_s3_file(self,file_url,local,retries=0):  
    if 's3://' in file_url:
      return self.get_s3_file(file_url,local,retries)
    else:  
      iattempt = 0
      resp = None
      while iattempt <= retries:
        iattempt += 1
        try:
          resp = urllib.request.urlretrieve(file_url, local)
        except Exception as e:
          raise e
      return resp 

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

  def exists(self,key):
    found = False
    try:
      _ = self.s3.ObjectSummary(self.bucket_name,key).load()
      found = True
    except Exception as err:
      print('s3.exists err',err)
      pass    
    return found

  def all(self):
    return self.bucket.objects.all()
