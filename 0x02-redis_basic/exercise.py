#!/usr/bin/env python3
"""_summary_ method that takes a data argument and returns a string.
The method should generate a random key (e.g. using uuid),
store the input data in Redis using the random key and return the key.

  Returns:
      str: the key
  """
import redis
import uuid
import functools
from typing import Union, Any, Callable


def count_calls(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''returns the given method after incrementing its call counter.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
  def __init__(self):
    self._redis = redis.Redis()
    self._redis.flushdb()
   
  @count_calls 
  def store(self, data: Union[str, bytes, int, float]) -> str:
    key = str(uuid.uuid4())
    self._redis.set(key, data)
    return key
  
  def get(self, key: str, fn: callable = None) -> Union[str, bytes, int, float, None]:
    value = self._redis.get(key)
    if value is None:
      return None
    if fn:
      return fn(value)
    return value
    
  def get_str(self, key: str) -> str:
    return self.get(key, str)

  def get_int(self, key: str) -> int:
    return self.get(key, int)
  