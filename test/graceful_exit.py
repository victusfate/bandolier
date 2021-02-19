import time
import bandolier
from bandolier import graceful_exit


graceful_exit.register_handlers()

while True:
  print(time.time())
  time.sleep(4)
