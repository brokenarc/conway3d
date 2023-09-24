from enum import Enum

from conway3d.datamodel import CellBlock, IVector, cubic_neighbor_model
from conway3d.engine import CellDriver


class MockState(Enum):
    EMPTY = 0
    FULL = 1


class MockDriver(CellDriver):

    def __init__(self, cells: CellBlock[MockState]):
        super().__init__(cells, cubic_neighbor_model, MockState.EMPTY)

    def first_state(self, location: IVector, cells: CellBlock) -> MockState:
        """Even locations ((0, 0, 0), (2, 0, 0),...) are ``EMPTY``, odd
        locations ((1, 0, 0), (3, 0, 0),...) are ``FULL``.
        """
        x, y, z = location
        sx, sy, sz = cells.size
        i = x + (y * sx) + (z * sx * sy)

        return MockState.FULL if i % 2 else MockState.EMPTY

    def next_state(self, location: IVector, cells: CellBlock) -> MockState:
        return self.first_state(location, cells)
