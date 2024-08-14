#!/usr/bin/env python3
"""_summary_ method that takes a data argument and returns a string.
The method should generate a random key (e.g. using uuid),
store the input data in Redis using the random key and return the key.

  Returns:
      str: the key
  """
import redis
import uuid
from typing import Union


class Cache:
  def __init__(self):
    self._redis = redis.Redis()
    self._redis.flushdb()
    
  def store(self, data: Union[str, bytes, int, float]) -> str:
    key = str(uuid.uuid4())
    self._redis.set(key, data)
    return key
  