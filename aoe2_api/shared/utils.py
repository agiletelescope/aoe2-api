# Utility Functions

import time
import functools


def remove_none_keys(d):
    """
    Clean a dict of its None values,
    i.e remove all keys whose values are None

    :param d: dict to be parsed
    :return: dict, cleaned version of `d`
    """

    if d is None:
        return {}
    if not isinstance(d, dict):
        return {}

    return {key: value for key, value in d.items()
            if value is not None}


def timer(func):
    """
    Decorator,
    Prints the time taken for a function to execute
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_ts = time.perf_counter()
        ret = func(*args, **kwargs)
        time_elapsed_sec = time.perf_counter() - start_ts
        print('Timer Result, Func: ', func.__name__, ':', time_elapsed_sec, 'sec')

        return ret

    return wrapper
