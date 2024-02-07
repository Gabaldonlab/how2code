#!/usr/bin/env python3
"""
# 1. Using different data structures!

Previously install memory_profiler.

```bash
pip install memory_profiler
```

```bash
conda install conda-forge::memory_profiler
```

Run script:
python3 -m memory_profiler 1_data_structures.py
"""

import time
from typing import Iterable, Iterator
from memory_profiler import profile


def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        execution_time = end_time - start_time
        print(f"{func.__name__} took {execution_time:.4f} seconds to execute.")
        return result

    return wrapper


@profile(precision=4)
# @timing
def create_list_procedural() -> list[str]:
    print()
    print("create_list_procedural")
    print("===============")
    result: list[str] = []
    for _ in range(100000):
        result.append("list_item")
    return result
value1: list[str] = create_list_procedural()


@profile(precision=4)
# @timing
def create_list_with_comprehension() -> list[str]:
    print()
    print("create_list_with_comprehension")
    print("===============")
    return ["list_item" for _ in range(100000)]
value2: list[str] = create_list_with_comprehension()


@profile(precision=4)
# @timing
def create_tuple_with_comprehension() -> tuple[str, ...]:
    print()
    print("create_tuple_with_comprehension")
    print("===============")
    return tuple("list_item" for _ in range(100000))
value3: tuple[str, ...] = create_tuple_with_comprehension()


@profile(precision=4)
# @timing
def create_tuple_with_from_map_generator() -> Iterator[str]:
    print()
    print("create_tuple_with_from_map_generator")
    print("===============")
    return map(lambda _: "list_item", range(100000))
value4: Iterator[str] = create_tuple_with_from_map_generator()

print()
print("===================")
print("Notice the last one with the generator! What happened?")
print("Let's loop them and for each item do something!")
print("===================")



@profile(precision=4)
def loop_and_diddle_array(array: Iterable[str]) -> int:
    result: int = 0
    for item in array:
        lala: str = 1000 * item
        result += len(lala)
    return result

print()
print("loop_procedural_list")
print("====================")
loop_and_diddle_array(value1)

print("loop_list_comprehension")
print("=======================")
loop_and_diddle_array(value2)

print("loop_tuple")
print("==========")
loop_and_diddle_array(value3)

print("loop_iterator")
print("=============")
loop_and_diddle_array(value4)
