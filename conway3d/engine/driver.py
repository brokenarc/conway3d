from abc import ABC, abstractmethod
from typing import Generic

from ..datamodel import CellBlock, IVector, T_state, NeighborModel

class CellDriver(ABC, Generic[T_state]):
    """A cell driver provides the rules that determines what the next state
    of any given cell within a block should be.
    """

    __slots__ = ('_neighbors', '_empty_state',)

    def __init__(self, neighbors: NeighborModel, empty_state: T_state):
        """
        Args:
            neighbors: The function this driver should use to determine how
                many neighbors a cell has.
            empty_state: The state that indicates that a cell is empty and
                should not be counted in the population.
        """
        self._neighbors = neighbors
        self._empty_state = empty_state

    @property
    def empty_state(self) -> T_state:
        """The state that indicates that a cell is empty and should not be
        counted in the population.
        """
        return self._empty_state

    @property
    def neighbors(self) -> NeighborModel:
        """The function this driver should use to determine how many
        neighbors a cell has."""
        return self._neighbors

    @abstractmethod
    def first_state(self,
        location: IVector,
        cells: CellBlock[T_state]
    ) -> T_state:
        """Determines the initial state for a cell.

        Args:
            location: The cell's grid coordinate
            cells: A reference to the cell block invoking the method

        Returns:
            The initial state for the cell at the given coordinates.
        """

    @abstractmethod
    def next_state(self,
        location: IVector,
        cells: CellBlock[T_state]
    ) -> T_state:
        """Determines the next state for a cell.

        Args:
            location: The cell's grid coordinate
            cells: A reference to the cell block invoking the method

        Returns:
            The next state for the cell.
        """
