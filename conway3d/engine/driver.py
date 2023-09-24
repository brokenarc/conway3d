from abc import ABC, abstractmethod
from functools import reduce
from typing import Generic

from ..datamodel import CellBlock, IVector, NeighborModel, T_state


class CellDriver(ABC, Generic[T_state]):
    """A cell driver provides the rules that determines what the next state of any given cell
    within a block should be.
    """
    __slots__ = ('_generation', '_cells', '_neighbors', '_empty',)

    def __init__(self, cells: CellBlock[T_state], neighbors: NeighborModel, empty_state: T_state):
        """
        Args:
            neighbors: The function this driver should use to determine how many neighbors a cell
                has.
            empty_state: The state that indicates that a cell is empty and should not be counted in
                the population.
        """
        self._generation = 0
        self._cells = cells
        self._neighbors = neighbors
        self._empty = empty_state

    @property
    def generation(self) -> int:
        """The number of generations that have passed.

        In essence, this is the number of times ``next_generation`` has been invoked.
        """
        return self._generation

    @property
    def cells(self) -> CellBlock[T_state]:
        """The cell block this driver is controlling."""
        return self._cells

    @property
    def empty_state(self) -> T_state:
        """The state that indicates that a cell is empty and should not be counted in the
        population.
        """
        return self._empty

    @property
    def neighbors(self) -> NeighborModel:
        """The function this driver should use to determine how many neighbors a cell has."""
        return self._neighbors

    def get_neighbor_locations(self, location: IVector) -> list[IVector]:
        """Returns the grid coordinates of the neighbors of the given ``location``.

        Coordinates that fall outside the cell block's boundary are filtered out.

        Args:
            location: The location of the cell to inspect.
        """
        if location not in self._cells:
            raise ValueError('Given location is not inside cell block boundaries.')

        # Filter out invalid locations.
        neighbors = filter(
            lambda xyz: xyz in self._cells,
            self._neighbors(location)
        )

        return list(neighbors)

    def get_neighbors(self, location: IVector) -> dict[IVector, T_state]:
        """Get a cell's neighboring cells.

        Args:
            location: The location of the cell to inspect.

        Returns:
            A dictionary with neighbor locations (``IVector``) as keys and the cell states
            (``T_state``) as values. This will also include cells that are empty.
        """
        return {
            loc: self._cells[loc]
            for loc in self.get_neighbor_locations(location)
        }

    def get_neighbor_count(self, location: IVector) -> int:
        """Returns the number of non-empty cells that are neighbors to the given location.
        """
        return reduce(
            lambda x, state: x + (0 if state == self._empty else 1),
            self.get_neighbors(location).values(), 0
        )

    @property
    def population(self) -> int:
        """The number of cells in the block that are not "empty."

        A cell is considered empty if its state is equal to the state returned by the driver's
        ``empty_state()`` method. Subclasses may override this method to customize how the
        population is counted.

        Returns:
            The population count.
        """
        return reduce(
            lambda p, c: p + (1 if c != self._empty else 0),
            self._cells.values(), 0
        )

    @property
    def density(self) -> float:
        """The population density of this cell block.

        Returns:
            A value from 0 to 1 representing the ratio of populated (not "empty") cells to the cell
            block's capacity.
        """
        return self.population / self._cells.capacity

    def populate(self) -> None:
        """Populates each cell in the cell block with an initial state determined by the
        implementation.

        Implementations may override this method to customize the initial population.
        """
        for xyz in self._cells:
            self._cells[xyz] = self.first_state(xyz, self._cells)

    def next_generation(self):
        """Progress this block to its next generation.

        The existing cell block will be updated in-place with new cell states. This means that
        existing references to the cell block will have access to the most current state.
        """
        current = self._cells.copy()

        for xyz in self._cells:
            self._cells[xyz] = self.next_state(xyz, current)

        self._generation += 1

    def reset(self):
        """Sets the generation count to 0 and invokes ``populate``."""
        self._generation = 0
        self.populate()

    @abstractmethod
    def first_state(self, location: IVector, cells: CellBlock[T_state]) -> T_state:
        """Determines the initial state for a cell.

        Args:
            location: The cell's grid coordinate
            cells: A reference to the cell block invoking the method

        Returns:
            The initial state for the cell at the given coordinates.
        """

    @abstractmethod
    def next_state(self, location: IVector, cells: CellBlock[T_state]) -> T_state:
        """Determines the next state for a cell.

        Args:
            location: The cell's grid coordinate
            cells: A reference to the cell block invoking the method

        Returns:
            The next state for the cell.
        """
