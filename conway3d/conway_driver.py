from enum import Enum
from random import random

from .cell_logic import CellBlock, CellDriver


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

    def default_state(self) -> ConwayCellState:
        return ConwayCellState.DEAD

    def next_state(self, x: int, y: int, z: int,
                   cell_block: CellBlock) -> ConwayCellState:
        """Determine the next cell state for the given parameters.

        Args:
            x: the cell's x coordinate
            y: the cell's y coordinate
            z: the cell's z coordinate
            cell_block: a reference to the cell block invoking the method

        Returns:
            The next cell state.
        """
        state = cell_block.get_cell(x, y, z)
        neighbor_count = cell_block.get_neighbor_count(x, y, z)

        if (state == ConwayCellState.ALIVE) and (3 < neighbor_count < 7):
            return ConwayCellState.ALIVE
        elif (state == ConwayCellState.DEAD) and (neighbor_count == 6):
            return ConwayCellState.ALIVE
        elif ((state == ConwayCellState.DEAD) and (neighbor_count == 0) and
              (self._quantum > 0)):
            if random() < self._quantum:
                return ConwayCellState.ALIVE

        return ConwayCellState.DEAD
