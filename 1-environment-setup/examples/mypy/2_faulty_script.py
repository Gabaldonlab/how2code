#!/usr/bin/env python3

from typing import TypedDict


def add_numbers(a: int, b: int) -> str:
    # This will fail because the return type is annotated as str, but the actual type is int
    return a + b


def greet(name: str) -> None:
    print("Hello, " + name)


# This will fail because the argument type is annotated as str, but the actual type is int
greet(42)


# ===========================================================
# ===========================================================


def double_numbers(numbers: list[str]) -> list[str]:
    return [2 * num for num in numbers]


# This will fail because the list elements are annotated as str, but the actual types are int
double_numbers([1, 2, 3])


# ===========================================================
# ===========================================================


class Person(TypedDict):
    name: str
    age: int


# This will fail because the 'email' field is not defined in the TypedDict
person_info: Person = {"name": "John", "age": 30, "email": "john@example.com"}
