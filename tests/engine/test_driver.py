import pytest

from conway3d.datamodel import CellBlock, IVector, cubic_neighbor_model
from ..mocks.mock_driver import MockDriver

class TestDriver:
    @pytest.fixture(autouse=True)
    def setup(self):
        self._size = (4, 4, 4)
        self._cells = CellBlock(self._size)
        self._driver = MockDriver(self._cells)
        self._empty = self._driver.empty_state
        self._driver.populate()

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
        assert self._driver.get_neighbor_count(location) == expected

    @pytest.mark.parametrize(
        'size, expected',
        [
            ((4, 4, 4), 32),
            ((3, 3, 3), 13),
            ((3, 4, 5), 30)
        ]
    )
    def test_population(self, size: IVector, expected: int):
        cells = CellBlock(size)
        driver = MockDriver(cells)
        driver.populate()

        assert driver.population == expected

    @pytest.mark.parametrize(
        'size, expected',
        [
            ((4, 4, 4), 0.5),
            ((3, 3, 3), (13 / 27)),
            ((3, 4, 5), 0.5)
        ]
    )
    def test_density(self, size: IVector, expected: float):
        cells = CellBlock(size)
        driver = MockDriver(cells)
        driver.populate()

        assert driver.density == expected
