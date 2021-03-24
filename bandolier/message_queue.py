import json
import sys
from sys import platform
import time
import random
import boto3
from typing import Optional
from . import constants

def random_id():
  return '%08x' % random.getrandbits(32) + '_' + str(int(time.time()))

class MessageQueue:
  def __init__(self,name: str, env: str, region_name: str, profile_name: Optional[str], aws_key: Optional[str], aws_secret: Optional[str]):
    
    self.name = name
    self.env  = env
    self.region_name = region_name
    self.profile_name = profile_name
    self.session = None
    
    if aws_key and aws_secret:
      self.session = boto3.Session(aws_access_key_id=aws_key,aws_secret_access_key=aws_secret)
    elif self.profile_name:
      self.session = boto3.Session(profile_name=self.profile_name,region_name=self.region_name)
    else:
      self.session = boto3.Session(region_name=self.region_name)
    # Create SQS client
    self.sqs = self.session.resource('sqs')
    # https://boto3.amazonaws.com/v1/documentation/api/1.9.42/reference/services/sqs.html#id53
    self.queue_name = self.get_name()

  def get_name(self):
    return self.env + '_' + self.name

  def send(self,body,message_id=None):
    sbody = json.dumps(body)
    queue = self.sqs.get_queue_by_name(QueueName=self.queue_name)
    # allow specification of message_id, default is content deduplication with 5 min timeout interval
    # see https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues.html#FIFO-queues-exactly-once-processing
    if message_id:
      response = queue.send_message(
          MessageBody=sbody,
          MessageGroupId='messageGroup1',
          MessageDeduplicationId=message_id
      )
    else:
      response = queue.send_message(
          MessageBody=sbody,
          MessageGroupId='messageGroup1'
      )

    return response

  def pop(self):
    body = None
    queue = self.sqs.get_queue_by_name(QueueName=self.queue_name)
    while body is None:
      messages = queue.receive_messages(
        MaxNumberOfMessages=1,
        WaitTimeSeconds=1,
      )
      if len(messages) > 0:
        message = messages.pop(0)
        sbody = message.body
        body = json.loads(sbody)
        # Let the queue know that the message is processed
        message.delete()
        break
    return body

  def receive_all(self):
    queue = self.sqs.get_queue_by_name(QueueName=self.queue_name)
    messages = []
    for message in queue.receive_messages():
      messages.append(message.body)
      message.delete()
    return messages

  def purge(self):
    queue = self.sqs.get_queue_by_name(QueueName=self.queue_name)
    queue.purge()


  def create_queue(self):
    self.sqs.create_queue(
      QueueName=self.queue_name,
      Attributes={
          'FifoQueue'                 : 'true',  # Allows for deduplication ids
          'ContentBasedDeduplication' : 'false'        
          # 'DelaySeconds': '0',
          # 'MessageRetentionPeriod': '86400',
          # 'FifoQueue': 'true',
          # 'ContentBasedDeduplication': 'true'
      })
