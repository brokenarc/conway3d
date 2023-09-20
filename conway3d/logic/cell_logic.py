from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from functools import reduce
from typing import Generic, TypeVar, cast

TCS = TypeVar('TCS', bound=Enum)


class CellDriver(ABC, Generic[TCS]):
    """A cell driver provides the logic that determines what the next state
    of any given cell within a block should be.
    """

    @abstractmethod
    def empty_state(self) -> TCS:
        """The state that indicates that a cell is empty and should not be
        counted in the population.
        """

    @abstractmethod
    def first_state(self, x: int, y: int, z: int,
                    cell_block: CellBlock) -> TCS:
        """Determines the initial state for a cell.

        Args:
            x: the cell's x coordinate
            y: the cell's y coordinate
            z: the cell's z coordinate
            cell_block: a reference to the cell block invoking the method

        Returns:
            The initial state for the cell at the given coordinates.
        """

    @abstractmethod
    def next_state(self, x: int, y: int, z: int,
                   cell_block: CellBlock) -> TCS:
        """Determines the next state for a cell.

        Args:
            x: the cell's x coordinate
            y: the cell's y coordinate
            z: the cell's z coordinate
            cell_block: a reference to the cell block invoking the method

        Returns:
            The next state for the cell.
        """


class CellBlock(Generic[TCS]):
    __slots__ = ('_x_size', '_y_size', '_z_size', '_cells',
                 '_driver', '_empty', '_generation')

    def __init__(self, x_size: int, y_size: int, z_size: int,
                 driver: CellDriver[TCS]):
        self._x_size = x_size
        self._y_size = y_size
        self._z_size = z_size
        self._driver = driver
        self._empty = driver.empty_state()
        self._generation = 0
        self._cells = [self._empty] * (x_size * y_size * z_size)
        self._populate()

    def __len__(self) -> int:
        return len(self._cells)

    def __getitem__(self, item):
        return self._cells[item]

    def _populate(self):
        for z in range(0, self._z_size):
            for y in range(0, self._y_size):
                for x in range(0, self._x_size):
                    i = self._get_index(x, y, z)
                    self._cells[i] = self._driver.first_state(x, y, z, self)

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

    @property
    def x_size(self) -> int:
        return self._x_size

    @property
    def y_size(self) -> int:
        return self._y_size

    @property
    def z_size(self) -> int:
        return self._z_size

    @property
    def generation(self) -> int:
        """The number of generations that have passed for the cell block."""
        return self._generation

    def get_cell(self, x: int, y: int, z: int) -> TCS:
        return self._cells[self._get_index(x, y, z)]

    def is_empty(self, x: int, y: int, z: int) -> bool:
        return self.get_cell(x, y, z) == self._empty

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
        # TODO filter based on non-empty cells (true neighbors)
        return len(self.get_neighbor_indexes(x, y, z))

    def next_generation(self):
        """Progress this block to its next generation.
        """
        cells = [self._empty] * len(self._cells)

        for z in range(0, self._z_size):
            for y in range(0, self._y_size):
                for x in range(0, self._x_size):
                    i = self._get_index(x, y, z)
                    cells[i] = self._driver.next_state(x, y, z, self)

        for i, state in enumerate(cells):
            self._cells[i] = state

        self._generation += 1

    def get_population(self) -> int:
        """Determines the number of cells in the block that are not 'empty.'

        A cell is considered empty if its state is equal to the state
        returned by the driver's ``empty_state`` method.

        Returns:
            The population count.
        """
        empty = self._driver.empty_state()

        return reduce(lambda p, c: 1 if c != empty else 0, self._cells, 0)
