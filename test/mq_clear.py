import json
from bandolier import constants
from bandolier import message_queue as mq
from bandolier.message_queue import MessageQueue

training_queue = mq.MessageQueue(constants.CONFIG['queues']['test_queue'])

training_queue.purge()
