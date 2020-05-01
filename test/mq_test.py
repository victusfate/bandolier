import json
from bandolier import constants
from bandolier import message_queue as mq
from bandolier.message_queue import MessageQueue

test_queue = MessageQueue(constants.CONFIG['queues']['test_queue'])
# test_queue.send('boop') # default message_id None uses content deduplication
test_queue.send(body='boop',message_id=mq.random_id())
json_message_body = test_queue.pop()
print('beep',json_message_body)

data = { 'beep': 'boop', 'asdf': 17.0 }
test_queue.send(body=data,message_id=mq.random_id())
dict_message_body = test_queue.pop()
print('json_message_body',dict_message_body)
