from enum import Enum

from conway3d.datamodel import CellBlock, IVector
from conway3d.engine import CellDriver


class MockState(Enum):
    EMPTY = 0
    FULL = 1


class MockDriver(CellDriver):
    def empty_state(self) -> MockState:
        return MockState.EMPTY

    def first_state(self, location: IVector,
                    cells: CellBlock) -> MockState:
        x, y, z = location
        sx, sy, sz = cells.size
        i = x + (y * sx) + (z * sx * sy)

        return MockState.FULL if i % 2 else MockState.EMPTY

    def next_state(self, location: IVector,
                   cells: CellBlock) -> MockState:
        return self.first_state(location, cells)
