import atexit
import signal
import sys
  
def register_handlers():
  # graceful exit
  def log_atexit(sig,stack=None):
    sig_enum = None
    try:
      sig_enum = signal.Signals(sig)
    except:
      pass
    print('received atexit signal',sig,'sig_enum',sig_enum,'stopping process stack',stack)
    sys.exit()

  atexit.register(lambda: log_atexit(None,None))
  # https://stackabuse.com/handling-unix-signals-in-python/
  # 1 (SIGHUP): terminate a connection, or reload the configuration for daemons
  # 2 (SIGINT): interrupt the session from the dialogue station
  # 3 (SIGQUIT): terminate the session from the dialogue station
  # 4 (SIGILL): illegal instruction was executed
  # 5 (SIGTRAP): do a single instruction (trap)
  # 6 (SIGABRT): abnormal termination
  # 7 (SIGBUS): error on the system bus
  # 8 (SIGFPE): floating point error
  # 9 (SIGKILL): immmediately terminate the process
  # 10 (SIGUSR1): user-defined signal
  # 11 (SIGSEGV): segmentation fault due to illegal access of a memory segment
  # 12 (SIGUSR2): user-defined signal
  # 13 (SIGPIPE): writing into a pipe, and nobody is reading from it
  # 14 (SIGALRM): the timer terminated (alarm)
  # 15 (SIGTERM): terminate the process in a soft way

  # exit_signals = [
  #   signal.SIGHUP, signal.SIGINT, signal.SIGILL, signal.SIGFPE, signal.SIGSEGV,
  #   signal.SIGTERM, signal.SIGABRT, signal.SIGKILL
  # ]

  graceful_exit_signals = [
    signal.SIGHUP, signal.SIGINT, signal.SIGTERM, signal.SIGKILL
  ]
  for sig in graceful_exit_signals:
    try:
      signal.signal(sig, log_atexit) 
    except:
      pass
