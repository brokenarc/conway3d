from typing import Generic

from .driver import CellDriver
from ..datamodel import CellBlock, T_state, generate_locations


class CellController(Generic[T_state]):
    __slots__ = ('_generation', '_cells', '_driver')

    def __init__(self,
        cells: CellBlock[T_state],
        driver: CellDriver[T_state]
    ):
        self._generation = 0
        self._cells = cells
        self._driver = driver

    @property
    def generation(self) -> int:
        """The number of generations that have passed."""
        return self._generation

    @property
    def driver(self) -> CellDriver[T_state]:
        return self._driver

    @property
    def cells(self) -> CellBlock[T_state]:
        return self._cells

    def populate(self) -> None:
        """Populates each cell in the cell block with an initial state
        defined by the driver provided to the constructor.
        """
        for xyz in generate_locations(self._cells.size):
            self._cells[xyz] = self._driver.first_state(
                xyz, self._cells
            )

    def next_generation(self):
        """Progress this block to its next generation.

        The existing cell block will be updated in-place with new cell states.
        This means that existing references to the cell block will have
        access to the most current state.
        """
        current = self._cells.copy()

        for xyz in generate_locations(self._cells.size):
            self._cells[xyz] = self._driver.next_state(xyz, current)

        self._generation += 1
