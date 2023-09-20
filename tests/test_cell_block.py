from enum import Enum

import pytest

from conway3d.logic import CellBlock, CellDriver

"""
Test functions use this test (x,y,z) data:
z=0           z=1           z=2           z=3
00 01 02 03   16 17 18 19   32 33 34 35   48 49 50 51
04 05 06 07   20 21 22 23   36 37 38 39   52 53 54 55
08 09 10 11   24 25 26 27   40 41 42 43   56 57 58 59
12 13 14 15   28 29 30 31   44 45 46 47   60 61 62 63
"""


class TestState(Enum):
    IDENTITY = 0


class TestDriver(CellDriver):
    def empty_state(self) -> TestState:
        return TestState.IDENTITY

    def first_state(self, x: int, y: int, z: int,
                    cell_block: CellBlock) -> TestState:
        return TestState.IDENTITY

    def next_state(self, state: TestState, **kwargs) -> TestState:
        return TestState.IDENTITY


@pytest.mark.parametrize(
    "x, y, z, expected",
    [
        (0, 0, 0, 0),
        (1, 1, 2, 37),
        (2, 3, 1, 30),
        (0, 2, 3, 56),
        (-1, 2, 2, -1),
        (2, -1, 2, -1),
        (2, 2, -1, -1),
        (4, 2, 2, -1),
        (2, 4, 2, -1),
        (2, 2, 4, -1),
    ]
)
def test_cell_block_get_index(x: int, y: int, z: int, expected: int):
    cb = CellBlock(4, 4, 4, TestDriver())
    assert cb._get_index(x, y, z) == expected


@pytest.mark.parametrize(
    "x, y, z, expected",
    [
        (0, 0, 0, (1, 4, 5, 16, 17, 20, 21)),
        (1, 1, 2, (
            16, 17, 18, 20, 21, 22, 24, 25, 26, 32, 33, 34, 36, 38, 40, 41,
            42, 48, 49, 50, 52, 53, 54, 56, 57, 58)),
        (3, 0, 1, (2, 3, 6, 7, 18, 22, 23, 34, 35, 38, 39)),
        (3, 3, 3, (42, 43, 46, 47, 58, 59, 62))
    ]
)
def test_cell_block_get_neighbor_indexes(x: int, y: int, z: int,
                                         expected: tuple[int]):
    cb = CellBlock(4, 4, 4, TestDriver())
    assert cb.get_neighbor_indexes(x, y, z) == expected


@pytest.mark.parametrize(
    "x, y, z, expected",
    [
        (0, 0, 0, 7),
        (1, 1, 2, 26),
        (3, 0, 1, 11),
        (3, 3, 3, 7)
    ]
)
def test_cell_block_get_neighbor_count(x: int, y: int, z: int, expected: int):
    cb = CellBlock(4, 4, 4, TestDriver())
    assert cb.get_neighbor_count(x, y, z) == expected
