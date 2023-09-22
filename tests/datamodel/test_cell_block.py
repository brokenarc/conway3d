from enum import Enum

import pytest

from conway3d.datamodel import CellBlock, IVector, generate_locations, simple_neighbor_model, cubic_neighbor_model
from .datamodel_mocks import MockState, MockDriver
from conway3d.engine import CellController

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

00 01 02   09 10 11   18 19 20
03 04 05   12 13 14   21 22 23
06 07 08   15 16 17   24 25 26

00 01 02   12 13 14   24 25 26
03 04 05   15 16 17   27 28 29
06 07 08   18 19 20   30 31 32
09 10 11   21 22 23   33 34 35
math.floor
"""

@pytest.mark.parametrize(
    'size, locations',
    [
        ((3,3,3), [
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
def test_generate_locations(size: IVector, locations: list[IVector]):
    assert set(generate_locations(size)) == set(locations)

class TestCellBlock:
    @pytest.fixture(autouse=True)
    def setup(self):
        self._size = (4, 4, 4)
        self._driver = MockDriver(cubic_neighbor_model, MockState.EMPTY)
        self._empty = self._driver.empty_state()
        self._cells = CellBlock(self._size,
                                cubic_neighbor_model,
                                self._empty)
        self._controller = CellController(self._cells, self._driver)
        self._controller.populate()

    @pytest.mark.parametrize(
        'location, expected',
        [
            ((0, 0, 0), 4),
            ((1, 1, 2), 8),
            ((3, 0, 1), 5),
            ((3, 3, 3), 3)
        ]
    )
    def test_get_neighbor_count(self, location: IVector, expected: int):
        assert self._cells.get_neighbor_count(location) == expected

    @pytest.mark.parametrize(
        'size, expected',
        [
            ((4, 4, 4), 32),
            ((3, 3, 3), 13),
            ((3, 4, 5), 30)
        ]
    )
    def test_population(self, size: IVector, expected: int):
        cells = CellBlock(size, cubic_neighbor_model, self._empty)
        ctrl = CellController(cells, self._driver)
        ctrl.populate()
        assert cells.population == expected

    @pytest.mark.parametrize(
        'size, expected',
        [
            ((4, 4, 4), 0.5),
            ((3, 3, 3), (13 / 27)),
            ((3, 4, 5), 0.5)
        ]
    )
    def test_density(self, size: IVector, expected: float):
        cells = CellBlock(size, cubic_neighbor_model, self._empty)
        ctrl = CellController(cells, self._driver)
        ctrl.populate()
        assert cells.density == expected

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
