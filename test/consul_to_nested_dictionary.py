from bandolier import data_tools
import json


consul_list = [
  {'LockIndex': 0, 'Key': 'recommender/queues/photo3d_video_queue', 'Flags': 0, 'Value': b'photo3d_video.fifo', 'CreateIndex': 8665, 'ModifyIndex': 8665}, 
  {'LockIndex': 0, 'Key': 'recommender/queues/quality_video_queue', 'Flags': 0, 'Value': b'quality_video.fifo', 'CreateIndex': 8666, 'ModifyIndex': 8666}, 
  {'LockIndex': 0, 'Key': 'recommender/queues/recommender_training_queue', 'Flags': 0, 'Value': b'recommender_training.fifo', 'CreateIndex': 8667, 'ModifyIndex': 8667}
]

print('consul like list',consul_list)

config = data_tools.consul_to_nested_dict(consul_list)
print('nested config',json.dumps(config, indent=2))