from __future__ import annotations

from typing import Any, Generator, Generic

from .types import IVector, T_state

CELL_NAME = 'Cell-{:02d}{:02d}{:02d}'
"""The template for canonical name of a cell at a given location."""


class CellBlock(Generic[T_state]):
    __slots__ = ('_size', '_neighbors', '_empty', '_capacity', '_cells', '_cell_name')

    def __init__(self,
        size: IVector,
        cell_name: str = CELL_NAME
    ):
        """
        Args:
            size: The (x, y, z) dimensions of the cell block.
            cell_name: Optional. The template for canonical name of a cell at a given location.
                This should accept three integer values: z, y, and x grid space coordinates.
                Defaults to ``CELL_NAME``.
        """
        self._size = size
        self._capacity = size[0] * size[1] * size[2]
        self._cell_name = cell_name
        self._cells = {xyz: None for xyz in self}

    def __len__(self) -> int:
        return self.capacity

    def __contains__(self, location: IVector) -> bool:
        """Returns ``True`` if the given location is inside this cell block.
        """
        x, y, z = location
        sx, sy, sz = self._size

        return (0 <= x < sx) and (0 <= y < sy) and (0 <= z < sz)

    def __getitem__(self, location: IVector) -> T_state | None:
        if location in self:
            return self._cells[location]

        raise KeyError

    def __setitem__(self, location: IVector, state: T_state):
        if location in self:
            self._cells[location] = state
        else:
            raise KeyError

    def __iter__(self) -> Generator[IVector]:
        """Yields every location within this cell block as an ``IVector``.

        Locations are traversed in z, y, x order starting from 0 on each axis.

        Yields:
            The next location as an (x, y, z) ``IVector``.
        """
        sx, sy, sz = self._size

        for z in range(0, sz):
            for y in range(0, sy):
                for x in range(0, sx):
                    yield x, y, z

    def copy(self) -> CellBlock[T_state]:
        other = CellBlock(self._size, self._cell_name)
        other._cells.update(self._cells)

        return other

    def get(self, location, default: Any) -> T_state | None:
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
    def size(self) -> IVector:
        """The size of this block as an (x, y, z) tuple."""
        return self._size

    @property
    def capacity(self) -> int:
        """The maximum number of cells this block can have."""
        return self._capacity

    def name_of(self, location: IVector) -> str:
        """Returns the canonical cell name for the given location in this cell block."""
        x, y, z = location
        return self._cell_name.format(z, y, x)
