#!/usr/bin/env python

import time

def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        execution_time = end_time - start_time
        print(f"{func.__name__} took {execution_time:.4f} seconds to execute.")
        return result

    return wrapper

@timing
def test_loop() -> list[int]:
    odd: list[int] = []
    for number in range(1000000):
        if number % 2:
            odd.append(number)
    return odd
test_loop()

@timing
def test_filter() -> list[int]:
    return list(filter(lambda x: x % 2, range(1000000)))
test_filter()
