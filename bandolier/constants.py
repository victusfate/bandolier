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

EMPTY_SHA1 = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'