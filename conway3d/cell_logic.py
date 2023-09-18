from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Generic, TypeVar, cast

T_CELL_STATE = TypeVar('T_CELL_STATE', bound=Enum)


class CellDriver(ABC, Generic[T_CELL_STATE]):
    """A cell driver provides the logic that determines what the next state
    of any given cell within a block should be.
    """

    @abstractmethod
    def default_state(self) -> T_CELL_STATE:
        """The default state value to initialize cell populations with.
        """

    @abstractmethod
    def next_state(self, x: int, y: int, z: int,
                   cell_block: CellBlock) -> T_CELL_STATE:
        """Determines the next state for a cell.

        Args:
            x: the cell's x coordinate
            y: the cell's y coordinate
            z: the cell's z coordinate
            cell_block: a reference to the cell block invoking the method

        Returns:
            The next state for the cell.
        """


class CellBlock(Generic[T_CELL_STATE]):
    __slots__ = ('_x_size', '_y_size', '_z_size', '_cells',
                 '_driver',)

    def __init__(self, x_size: int, y_size: int, z_size: int,
                 driver: CellDriver[T_CELL_STATE]):
        self._x_size = x_size
        self._y_size = y_size
        self._z_size = z_size
        self._driver = driver
        self._cells = [driver.default_state()] * (x_size * y_size * z_size)

    def __len__(self) -> int:
        return len(self._cells)

    def __getitem__(self, item):
        return self._cells[item]

    @property
    def x_size(self) -> int:
        return self._x_size

    @property
    def y_size(self) -> int:
        return self._y_size

    @property
    def z_size(self) -> int:
        return self._z_size

    def _get_index(self, x: int, y: int, z: int) -> int:
        """Compute the cell array index from x, y, z coordinates.

        Returns:
            The index of the cell at the given coordinates, or -1 if the
            coordinates are outside the bounds of the block.
        """
        if ((0 <= x < self._x_size) and (0 <= y < self._y_size) and
            (0 <= z < self.z_size)):
            return x + (y * self._x_size) + (z * self._x_size * self._y_size)

        return -1

    def get_cell(self, x: int, y: int, z: int) -> T_CELL_STATE:
        return self._cells[self._get_index(x, y, z)]

    def get_neighbor_indexes(self, x: int, y: int, z: int) -> tuple[int]:
        cell = self._get_index(x, y, z)
        indexes = [
            self._get_index(xx, yy, zz)
            for zz in (z - 1, z, z + 1)
            for yy in (y - 1, y, y + 1)
            for xx in (x - 1, x, x + 1)
        ]

        # filter out the negative indexes and the original cell
        neighbors = filter(
            lambda i: (i != cell) and (0 <= i < len(self._cells)),
            indexes
        )

        return cast(tuple[int], tuple(neighbors))

    def get_neighbor_count(self, x: int, y: int, z: int) -> int:
        return len(self.get_neighbor_indexes(x, y, z))

    def next_generation(self):
        """Progress this block to its next generation.
        """
        cells = self._cells.copy()

        for z in range(0, self._z_size):
            for y in range(0, self._y_size):
                for x in range(0, self._x_size):
                    i = self._get_index(x, y, z)
                    cells[i] = self._driver.next_state(x, y, z, self)

        self._cells = cells
