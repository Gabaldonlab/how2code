#!/usr/bin/env python3

# - A function, which is called in another function, should never have side effects!!!
# ===================================================================
# Bad example
from io import TextIOWrapper
import os
from typing import Iterable, Iterator

"""
Variable Names:

    Use lowercase letters with words separated by underscores.
    Example: user_name, age, total_count

Function Names:

    Use lowercase letters with words separated by underscores.
    Example: calculate_average, validate_input

Constants:

    Use uppercase letters with words separated by underscores.
    Example: MAX_VALUE, PI

Class Names:

    Use CamelCase (capitalizing the first letter of each word).
    Example: CarModel, PersonInfo

Module Names:

    Use lowercase letters with words separated by underscores.
    Example: my_module, utils

Package Names:

    Use lowercase letters without underscores.
    Example: mypackage, commonutils

Global Variables:

    Use lowercase letters with words separated by underscores (similar to regular variables).
    Example: GLOBAL_COUNTER, TOTAL_RECORDS

Function/Method Parameters:

    Use lowercase letters with words separated by underscores.
    Example: input_data, initial_value

Private Variables/Methods:

    Prefix the name with a single underscore to indicate it's intended for internal use.
    Example: _internal_method, _hidden_variable

    OR to "increase" the privacy...: __internal_method, __hidden_variable
"""


def sum_doubled_array_unpure(array: list[int]) -> int:
    array.extend(array)
    array.sort()
    return sum(array)


# array1: list[int] = [1,2,3]
# result1: int = sum_doubled_array_unpure(array1)
# print("input array for unpure function: ", array1)
# print("result of unpure function: ", result1)


# Good example
def sum_doubled_array_pure(array: list[int]) -> int:
    new_array: list[int] = sorted(2 * array)
    return sum(new_array)


# array2: list[int] = [1,2,3]
# result2: int = sum_doubled_array_unpure(array2)
# print("input array for pure function: ", array2)
# print("result of pure function: ", result2)
# ===================================================================


# - A function, which is called in another function, should do ONLY ONE THING!
# ===========================================================================
# Bad example
def diddle_the_lines1(input_file_path: str, output_file_path: str) -> None:
    """
    In this bad example we read the file, then
    print a pretty line and write another formatted line.

    This function should be broken down into various sub functions.
    """
    with open(input_file_path, "r", encoding="UTF-8") as input_file:
        content_lines: list[str] = input_file.readlines()
        content_without_empty_lines: Iterator[str] = filter(None, content_lines)
        lines_without_comment: Iterator[str] = filter(
            lambda x: not x.startswith("#"), content_without_empty_lines
        )

    output_file: TextIOWrapper = open(output_file_path, "w")
    for index, line in enumerate(lines_without_comment):
        new_pretty_line: str = f"{index} -> {line}"
        new_line_to_write: str = f"{index} ===> {line}"
        print(new_pretty_line)
        output_file.write(new_line_to_write)
    output_file.close()


# Good example
def get_filtered_file_lines(input_file_path: str) -> tuple[str, ...]:
    with open(input_file_path, "r", encoding="UTF-8") as input_file:
        content_lines: list[str] = input_file.readlines()
        content_without_empty_lines: Iterator[str] = filter(None, content_lines)
        lines_without_comment: Iterator[str] = filter(
            lambda x: not x.startswith("#"), content_without_empty_lines
        )
    return tuple(lines_without_comment)


def write_output_file(content_lines: Iterable[str], output_file_path: str) -> None:
    with open(output_file_path, "w", encoding="UTF-8") as output_file:
        for index, line in enumerate(content_lines):
            output_file.write(f"{index} ===> {line}")


def pretty_print_filtered_lines(content_lines: Iterable[str]) -> None:
    for index, line in enumerate(content_lines):
        new_pretty_line: str = f"{index} -> {line}"
        print(new_pretty_line)


def diddle_the_lines2(input_file_path: str, output_file_path: str) -> None:
    filtered_lines: tuple[str, ...] = get_filtered_file_lines(input_file_path)
    write_output_file(filtered_lines, output_file_path)
    pretty_print_filtered_lines(filtered_lines)


# ===========================================================================
