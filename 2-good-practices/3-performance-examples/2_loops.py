import time
from itertools import count

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
def use_while_loop() -> None:
    test_arr: list[int] = list(range(1000000))
    index: int = 0
    while index < len(test_arr) - 1:
        index += 1
use_while_loop()

@timing
def use_for_loop() -> None:
    test_arr: list[int] = list(range(1000000))
    index: int = 0
    for number in test_arr:
        index += 1
use_for_loop()
