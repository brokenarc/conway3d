import pytest

from conway3d.datamodel import CellBlock, IVector

"""
Test functions use this test (x,y,z) data:
z=0           z=1           z=2           z=3
00 01 02 03   16 17 18 19   32 33 34 35   48 49 50 51
04 05 06 07   20 21 22 23   36 37 38 39   52 53 54 55
08 09 10 11   24 25 26 27   40 41 42 43   56 57 58 59
12 13 14 15   28 29 30 31   44 45 46 47   60 61 62 63

z=0       z=1       z=2       z=3
0 1 0 1   0 1 0 1   0 1 0 1   0 1 0 1
0 1 0 1   0 1 0 1   0 1 0 1   0 1 0 1
0 1 0 1   0 1 0 1   0 1 0 1   0 1 0 1
0 1 0 1   0 1 0 1   0 1 0 1   0 1 0 1

Even indexes will be TestState.EMPTY, odd indexes will be TestState.FULL
"""


class TestCellBlock:
    @pytest.fixture(autouse=True)
    def setup(self):
        self._size = (4, 4, 4)
        self._cells = CellBlock(self._size)

    @pytest.mark.parametrize(
        'location, expected',
        [
            ((0, 0, 0), True),
            ((-1, 1, 1), False),
            ((1, -1, 1), False),
            ((1, 1, -1), False),
            ((3, 3, 3), True),
            ((4, 3, 3), False),
            ((3, 4, 3), False),
            ((3, 3, 4), False),
            ((4, 4, 4), False)
        ]
    )
    def test_contains(self, location: IVector, expected: bool):
        assert (location in self._cells) == expected

    @pytest.mark.parametrize(
        'size, locations',
        [
            ((3, 3, 3), [
                (0, 0, 0), (1, 0, 0), (2, 0, 0),
                (0, 1, 0), (1, 1, 0), (2, 1, 0),
                (0, 2, 0), (1, 2, 0), (2, 2, 0),

                (0, 0, 1), (1, 0, 1), (2, 0, 1),
                (0, 1, 1), (1, 1, 1), (2, 1, 1),
                (0, 2, 1), (1, 2, 1), (2, 2, 1),

                (0, 0, 2), (1, 0, 2), (2, 0, 2),
                (0, 1, 2), (1, 1, 2), (2, 1, 2),
                (0, 2, 2), (1, 2, 2), (2, 2, 2),
            ])
        ]
    )
    def test_iter(self, size: IVector, locations):
        cells = CellBlock(size)
        assert set([xyz for xyz in cells]) == set(locations)
