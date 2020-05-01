import os
import sys
import json

CONFIG = {
  'aws': {
    'bucket': None,
    'region': 'us-east-1',
    'profile': None
  },
  'environment': 'development',
  'queues': {
    'test_queue': 'bandolier_test.fifo'
  }
}
