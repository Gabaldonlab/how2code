#!/usr/bin/env python3
"""
# 1. Using different data structures!

Use the following alias in your ~/.bashrc!!

alias get-quick-stats="/usr/bin/time -f \"mem=%K RSS=%M elapsed=%E cpu.sys=%S user=%U\""

Then you can execute this script as:
get-quick-stats python3 1_data_structures.py
"""

import os
import time
from typing import Iterator
import psutil
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


def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


@profile
def create_list_procedural() -> list[str]:
    print()
    print("create_list_procedural")
    print("===============")
    result: list[str] = []
    for _ in range(100000):
        result.append("list_item")
    return result


value1: list[str] = create_list_procedural()


@profile
def create_list_with_comprehension() -> list[str]:
    print()
    print("create_list_with_comprehension")
    print("===============")
    return ["list_item" for _ in range(100000)]


value2: list[str] = create_list_with_comprehension()


@profile
def create_tuple_with_comprehension() -> tuple[str, ...]:
    print()
    print("create_tuple_with_comprehension")
    print("===============")
    return tuple("list_item" for _ in range(100000))


value3: tuple[str, ...] = create_tuple_with_comprehension()


@profile
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


@profile
def loop_an_iterator(array: Iterator[str]) -> None:
    for item in array:
        lala: str = 1000 * item
        lala_len: int = len(lala)


loop_an_iterator(value4)
