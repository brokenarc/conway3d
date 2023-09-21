from dataclasses import dataclass
from typing import Generic, TypeVar

Numeric = int | float
"""Shorthand type that covers numbers."""

NUM_TYPE = TypeVar('NUM_TYPE', bound=Numeric)

Vec2 = tuple[NUM_TYPE, NUM_TYPE]

Vec3 = tuple[NUM_TYPE, NUM_TYPE, NUM_TYPE]

# @dataclass(frozen=True, slots=True)
# class Vec2(Generic[NUM_TYPE]):
#     """A two-dimensional vector that can be typed to ``int`` or ``float``."""
#
#     x: NUM_TYPE
#     y: NUM_TYPE
#
#
# @dataclass(frozen=True, slots=True)
# class Vec3(Generic[NUM_TYPE]):
#     """A three-dimensional vector that can be typed to ``int`` or
#     ``float``."""
#
#     x: NUM_TYPE
#     y: NUM_TYPE
#     z: NUM_TYPE
