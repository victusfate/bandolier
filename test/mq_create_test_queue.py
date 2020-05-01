import json
from bandolier import constants
from bandolier import message_queue as mq
from bandolier.message_queue import MessageQueue

test_queue = MessageQueue(constants.CONFIG['queues']['test_queue'])
test_queue.create_queue()
