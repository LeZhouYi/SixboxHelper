import time
from typing import Callable, Tuple, Any


def run_with_retry(func: Callable, args: Tuple = (), retry: int = 1, delay: int = 10, kwargs: dict = None):
    """若出错，则重试"""
    kwargs = kwargs or {}
    last_error = None
    for attempt in range(retry + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_error = e
            if attempt < retry:
                time.sleep(delay)
    raise last_error


def check_with_retry(func: Callable, args: Tuple = (), expect_value: Any = True, retry: int = 1, delay: int = 10,
                   kwargs: dict = None):
    """若不符合预期，则重试，则重试"""
    kwargs = kwargs or {}
    result = None
    for attempt in range(retry + 1):
        result = func(*args, **kwargs)
        if result == expect_value:
            return result
        else:
            if attempt < retry:
                time.sleep(delay)
    return result
