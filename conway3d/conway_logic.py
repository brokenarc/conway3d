from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from functools import reduce
from random import random
from typing import Generic, TypeVar, cast

from .types import Vec3

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
    def first_state(self, location: Vec3[int], cell_block: CellBlock) -> TCS:
        """Determines the initial state for a cell.

        Args:
            location: the cell's grid coordinate
            cell_block: a reference to the cell block invoking the method

        Returns:
            The initial state for the cell at the given coordinates.
        """

    @abstractmethod
    def next_state(self, location: Vec3[int], cell_block: CellBlock) -> TCS:
        """Determines the next state for a cell.

        Args:
            location: the cell's grid coordinate
            cell_block: a reference to the cell block invoking the method

        Returns:
            The next state for the cell.
        """


class CellBlock(Generic[TCS]):
    __slots__ = ('_x_size', '_y_size', '_z_size', '_cells',
                 '_driver', '_empty', '_generation')

    def __init__(self, size: Vec3[int], driver: CellDriver[TCS]):
        self._x_size = size[0]
        self._y_size = size[1]
        self._z_size = size[2]
        self._driver = driver
        self._empty = driver.empty_state()
        self._generation = 0
        self._cells = [self._empty] * (
            self._x_size * self._y_size * self._z_size
        )
        self._populate()

    def __len__(self) -> int:
        return len(self._cells)

    def __getitem__(self, item):
        return self._cells[item]

    def _populate(self):
        for z in range(0, self._z_size):
            for y in range(0, self._y_size):
                for x in range(0, self._x_size):
                    i = self._get_index((x, y, z))
                    self._cells[i] = self._driver.first_state((x, y, z), self)

    def _get_index(self, location: Vec3) -> int:
        """Compute the cell array index from x, y, z coordinates.

        Returns:
            The index of the cell at the given coordinates, or -1 if the
            coordinates are outside the bounds of the block.
        """
        x, y, z = location
        if ((0 <= x < self._x_size) and (0 <= y < self._y_size) and
            (0 <= z < self.z_size)):
            return x + (y * self._x_size) + (z * self._x_size * self._y_size)

        return -1

    @property
    def size(self) -> Vec3:
        """The size of this block as an (x, y, z) tuple."""
        return self._x_size, self._y_size, self._z_size

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

    def get_cell(self, location: Vec3) -> TCS:
        return self._cells[self._get_index(location)]

    def is_empty(self, location: Vec3) -> bool:
        return self.get_cell(location) == self._empty

    def get_neighbor_indexes(self, location: Vec3) -> tuple[int]:
        cell = self._get_index(location)
        x, y, z = location
        indexes = [
            self._get_index((xx, yy, zz))
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

    def get_neighbor_count(self, location: Vec3) -> int:
        # TODO filter based on non-empty cells (true neighbors)
        return len(self.get_neighbor_indexes(location))

    def next_generation(self):
        """Progress this block to its next generation.
        """
        cells = [self._empty] * len(self._cells)

        for z in range(0, self._z_size):
            for y in range(0, self._y_size):
                for x in range(0, self._x_size):
                    i = self._get_index((x, y, z))
                    cells[i] = self._driver.next_state((x, y, z), self)

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


class ConwayCellState(Enum):
    DEAD = 0
    ALIVE = 1


class BasicConwayDriver(CellDriver[ConwayCellState]):
    """Provides a basic implementation of Conway's rules expanded for a
    three-dimensional grid.

    The rules for this driver are:
      - An alive cell with 4 to 6 neighbors stays alive.
      - A dead cell with 6 neighbors becomes alive.
      - A dead cell with 0 neighbors has a chance to become alive if the
        ``quantum`` property is greater than 0.0.
      - All other cells die or remain dead.
    """
    __slots__ = ('_quantum',)

    def __init__(self, quantum: float = 0):
        """
        Args:
            quantum: The probability (0.0 to 1.0) that a dead cell with no
                neighbors will spontaneously become alive.
        """
        self._quantum = quantum

    def empty_state(self) -> ConwayCellState:
        return ConwayCellState.DEAD

    def first_state(self, location: Vec3, cell_block: CellBlock) -> ConwayCellState:
        return self.empty_state()

    def next_state(self, location: Vec3, cell_block: CellBlock) -> ConwayCellState:
        """Determine the next cell state for the given parameters.

        Args:
            location: the cell's grid coordinate
            cell_block: a reference to the cell block invoking the method

        Returns:
            The next cell state.
        """
        state = cell_block.get_cell(location)
        neighbor_count = cell_block.get_neighbor_count(location)

        if (state == ConwayCellState.ALIVE) and (3 < neighbor_count < 7):
            return ConwayCellState.ALIVE
        elif (state == ConwayCellState.DEAD) and (neighbor_count == 6):
            return ConwayCellState.ALIVE
        elif ((state == ConwayCellState.DEAD) and (neighbor_count == 0) and
              (self._quantum > 0)):
            if random() < self._quantum:
                return ConwayCellState.ALIVE

        return ConwayCellState.DEAD
