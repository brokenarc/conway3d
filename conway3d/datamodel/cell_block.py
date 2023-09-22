from __future__ import annotations

from functools import reduce
from typing import Any, Generator, Generic, Iterator

from .neighbors import NeighborModel
from .types import IVector, T_state


def generate_locations(size: IVector) -> Generator[IVector]:
    """Generates every location within a space of the given ``size``.

    Args:
        size: The (x, y, z) size of the space to generate locations for.

    Yields:
        The next location.
    """
    sx, sy, sz = size

    for z in range(0, sz):
        for y in range(0, sy):
            for x in range(0, sx):
                yield x, y, z


class CellBlock(Generic[T_state]):
    __slots__ = ('_size', '_neighbors', '_empty', '_capacity', '_cells')

    def __init__(self,
        size: IVector,
        neighbors: NeighborModel,
        empty: T_state
    ):
        """
        Args:
            size: The (x, y, z) dimensions of the cell block.
            neighbors: The function used to determine any given cell's
                neighboring cells.
            empty: The state that each cell will be initialized to and
                that should be considered empty.
        """
        self._size = size
        self._neighbors = neighbors
        self._capacity = size[0] * size[1] * size[2]
        self._empty = empty
        self._cells = {xyz: empty for xyz in generate_locations(size)}

    def __len__(self) -> int:
        return self.capacity

    def __contains__(self, location: IVector) -> bool:
        """Returns ``True`` if the given location is inside this cell block.
        """
        x, y, z = location
        sx, sy, sz = self._size

        return (0 <= x < sx) and (0 <= y < sy) and (0 <= z < sz)

    def __getitem__(self, location: IVector) -> T_state:
        if location in self:
            return self._cells[location]

        raise KeyError

    def __setitem__(self, location: IVector, state: T_state):
        if location in self:
            self._cells[location] = state
        else:
            raise KeyError

    def __iter__(self) -> Iterator:
        return generate_locations(self._size)

    def copy(self) -> CellBlock:
        other = CellBlock(self._size, self._neighbors, self._empty)
        other._cells.update(self._cells)

        return other

    def get(self, location, default: Any) -> T_state:
        if location in self:
            return self[location]

        return default

    def keys(self):
        return self._cells.keys()

    def values(self):
        return self._cells.values()

    def update(self, other: CellBlock[T_state]) -> None:
        if self.size == other._size:
            self._cells.update(other._cells)
        else:
            raise ValueError('CellBlock sizes do not match.')

        return None

    @property
    def empty(self) -> T_state:
        """The cell state that this cell block considers to be empty."""
        return self._empty

    @property
    def size(self) -> IVector:
        """The size of this block as an (x, y, z) tuple."""
        return self._size

    @property
    def capacity(self) -> int:
        """The maximum number of cells this block can have."""
        return self._capacity

    @property
    def population(self) -> int:
        """The number of cells in the block that are not "empty."

        A cell is considered empty if its state is equal to the state
        returned by the driver's ``empty_state()`` method.

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

        This is the ratio of populated (not "empty") cells to the block's
        capacity. The returned value will be from 0 to 1.
        """
        return self.population / self._capacity

    def get_neighbor_locations(self, location: IVector) -> list[IVector]:
        """Returns the grid coordinates of the neighbors of the given
        ``location``.

        Coordinates that fall outside the block's boundary are filtered out.
        """

        # Filter out invalid locations.
        neighbors = filter(
            lambda xyz: xyz in self,
            self._neighbors(location)
        )

        return list(neighbors)

    def get_neighbors(self, location: IVector) -> dict[IVector, T_state]:
        """Get a cell's neighboring cells.

        Args:
            location: The location of the cell.

        Returns:
            A dictionary with neighbor locations (``IVector``) as keys
            and the cell states (``T_state``) as values. This will also
            include cells that are empty.
        """
        return {
            loc: self[loc]
            for loc in self.get_neighbor_locations(location)
        }

    def get_neighbor_count(self, location: IVector) -> int:
        """Returns the number of non-empty cells that are neighbors to the
        given location.
        """
        return reduce(
            lambda x, state: x + (0 if state == self._empty else 1),
            self.get_neighbors(location).values(), 0
        )
