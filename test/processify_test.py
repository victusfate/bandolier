import os
import sys
import traceback
from functools import wraps
from multiprocessing import Process, Queue

from bandolier.processify import processify

@processify
def test_function():
  return os.getpid()


@processify
def test_generator_func():
  for msg in ["generator", "function"]:
    yield msg


@processify
def test_deadlock():
  return range(30000)


@processify
def test_exception():
  raise RuntimeError('xyz')


def test():
  print(os.getpid())
  print(test_function())
  print(list(test_generator_func()))
  print(len(test_deadlock()))
  test_exception()

if __name__ == '__main__':
  test()