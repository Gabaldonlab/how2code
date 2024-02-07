#!/usr/bin/env python3

# - Class names must start capitalized, and shouldn't use abbreviations.
# - If using docstrings, don't write what the class or function is, rather explain what it does.
# ===================================================================

# Bad example.
from typing import Optional, TypedDict


class lib:
    """
    lib class
    """

    pass


# Good example.
class Library:
    """
    Represent the collection of books.
    """

    pass


# ===================================================================


# - Don't the return types, except if it can return None (or return number or string, not both.).
# - Avoid "else" as much as possible.
# - Annotate your variables, functions, returns.
# - If the shape of your returns may vary, then just use a dictionary.
# - Try to use descriptive function and variable names all the time. Prefer them over comments and docstrings!
#   Documentation can lie, but the code cannot!
# ===================================================================


# Bad example.
def roots(a, b, c):
    """Dániel Májer - 3:56 05/02/2023"""
    d = b**2 - 4 * a * c
    if d > 0:
        root1 = (-b + d**0.5) / (2 * a)
        root2 = (-b - d**0.5) / (2 * a)
        return root1, root2
    elif d == 0:
        root = -b / (2 * a)
        return root
    else:
        return "No real roots"


# Good example.
class QuadraticRoots(TypedDict):
    root1: float
    root2: Optional[float]


def calculate_quadratic_roots(
    coefficient_a: float, coefficient_b: float, coefficient_c: float
) -> QuadraticRoots:
    """
    Calculate the roots of a quadratic equation of the form ax^2 + bx + c.
    """

    discriminant: float = coefficient_b**2 - 4 * coefficient_a * coefficient_c

    if discriminant < 0:
        raise ValueError("No real roots.")

    if discriminant == 0:
        return {"root1": -coefficient_b / (2 * coefficient_a), "root2": None}

    return {
        "root1": (-coefficient_b + discriminant**0.5) / (2 * coefficient_a),
        "root2": (-coefficient_b - discriminant**0.5) / (2 * coefficient_a),
    }


# ===================================================================
