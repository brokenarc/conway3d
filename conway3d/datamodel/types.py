from enum import Enum
from typing import TypeVar

IVector = tuple[int, int, int]
"""A three-dimensional vector of integers."""

T_state = TypeVar('T_state', bound=Enum, covariant=True)
"""Defines a type parameter for cell states such that they must be Enums."""
