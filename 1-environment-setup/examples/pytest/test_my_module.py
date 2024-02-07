#!/usr/bin/env python3
import pytest

from my_module import add_numbers
from my_module import divide_numbers
from my_module import filter_even_numbers
from my_module import invert_dictionary


@pytest.mark.parametrize("a, b, expected", [(2, 3, 5), (-2, 3, 1)])
def test_add_numbers_parametrized(a: int, b: int, expected: int):
    result = add_numbers(a, b)
    assert result == expected


def test_add_numbers():
    result = add_numbers(2, 3)
    assert result == 5


def test_add_numbers_negative():
    result = add_numbers(-2, 3)
    assert result == 1


def test_divide_numbers():
    result = divide_numbers(10, 2)
    assert result == (5.0, 0.0)


def test_divide_numbers_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide_numbers(10, 0)


def test_filter_even_numbers():
    result = filter_even_numbers([1, 2, 3, 4, 5, 6])
    assert result == [2, 4, 6]


def test_filter_even_numbers_empty_list():
    result = filter_even_numbers([])
    assert result == []


def test_invert_dictionary():
    input_dict = {"one": 1, "two": 2, "three": 3}
    result = invert_dictionary(input_dict)
    assert result == {1: "one", 2: "two", 3: "three"}


def test_invert_dictionary_empty_dict():
    result = invert_dictionary({})
    assert result == {}


def test_invert_dictionary():
    input_dict = {"one": 1, "two": 2, "three": 3}
    result = invert_dictionary(input_dict)
    assert result == {1: "one", 2: "two", 3: "three"}


def test_invert_dictionary_empty_dict():
    result = invert_dictionary({})
    assert result == {}
