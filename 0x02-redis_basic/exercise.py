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
  

def call_history(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        # Create input and output list keys
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store the input arguments
        self._redis.rpush(input_key, str(args))

        # Execute the wrapped function
        output = method(self, *args, **kwargs)

        # Store the output
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper

class Cache:
  def __init__(self):
    self._redis = redis.Redis()
    self._redis.flushdb()
   
  @call_history
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
  

def replay(method):
    cache = method.__self__
    inputs = cache.redis.lrange(cache.store_inputs, 0, -1)
    outputs = cache.redis.lrange(cache.store_outputs, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input_data, output_key in zip(inputs, outputs):
        input_str = input_data.decode('utf-8')
        output_str = output_key.decode('utf-8')
        print(f"{method.__qualname__}(*({input_str},)) -> {output_str}")
  