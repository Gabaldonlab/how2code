#!/usr/bin/env python3


def add_numbers(a: int, b: int) -> int:
    return a + b


def divide_numbers(a: int, b: int) -> tuple[float, float]:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    quotient = a / b
    remainder = a % b
    return quotient, remainder


def filter_even_numbers(numbers: list[int]) -> list[int]:
    return [num for num in numbers if num % 2 == 0]


def invert_dictionary(input_dict: dict[str, int]) -> dict[int, str]:
    return {value: key for key, value in input_dict.items()}
