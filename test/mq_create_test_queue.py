import json
from bandolier import constants
from bandolier import message_queue as mq
from bandolier.message_queue import MessageQueue

test_queue = MessageQueue(name=constants.CONFIG['queues']['test_queue'],
  env=constants.CONFIG['environment'],
  region_name=constants.CONFIG['aws']['region'],
  profile_name=constants.CONFIG['aws']['profile'])
test_queue.create_queue()
