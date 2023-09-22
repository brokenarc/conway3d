from enum import Enum
from random import random

from .driver import CellDriver
from ..datamodel import CellBlock, IVector


class ConwayCellState(Enum):
    DEAD = 0
    ALIVE = 1


class BasicConwayDriver(CellDriver[ConwayCellState]):
    """Provides a basic implementation of Conway's rules expanded for a
    three-dimensional grid.

    The rules for this driver are:
      - An alive cell with 4 to 6 neighbors stays alive.
      - A dead cell with 6 neighbors becomes alive.
      - All other cells die or remain dead.
    """

    def __init__(self):
        super().__init__(ConwayCellState.DEAD)

    def first_state(self,
        location: IVector,
        cells: CellBlock[ConwayCellState]
    ) -> ConwayCellState:
        return ConwayCellState.DEAD

    def next_state(self,
        location: IVector,
        cells: CellBlock[ConwayCellState]
    ) -> ConwayCellState:
        """Determine the next cell state for the given parameters.

        Args:
            location: The cell's grid coordinate
            cells: A reference to the cell block invoking the method

        Returns:
            The next cell state.
        """
        state = cells[location]
        neighbor_count = cells.get_neighbor_count(location)

        if (state == ConwayCellState.ALIVE) and (3 < neighbor_count < 7):
            return ConwayCellState.ALIVE
        elif (state == ConwayCellState.DEAD) and (neighbor_count == 6):
            return ConwayCellState.ALIVE
        else:
            return ConwayCellState.DEAD


class UncertainConwayDriver(BasicConwayDriver):
    """A variant of the Conway driver that provides random fluctuations to
    the rules.

    These adjustments are made if the ``uncertainty`` property is greater
    than 0:
      - A dead cell with less than 3 neighbors has a chance to become alive.
      - Any living cell has a chance to keep its current state.
    """

    __slots__ = ('_uncertainty',)

    def __init__(self, uncertainty: float = 0):
        """
        Args:
            uncertainty: The probability (0.0 to 1.0) that rule fluctuations
                will be applied.
        """
        super().__init__()
        self._uncertainty = uncertainty

    def next_state(self,
        location: IVector,
        cells: CellBlock[ConwayCellState]
    ) -> ConwayCellState:
        state = cells[location]
        neighbor_count = cells.get_neighbor_count(location)

        if random() <= self._uncertainty:
            if (state == self.empty_state) and (neighbor_count < 3):
                return ConwayCellState.ALIVE
            else:
                return state
        else:
            return super().next_state(location, cells)
