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


def replay(fn: Callable) -> None:
    """Displays the call history of a Cache class' method.

    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))

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
