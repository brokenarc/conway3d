from .controller import CellController
from .driver import CellDriver
from ..datamodel import CellBlock, IVector


class GameOfLife:
    """Creates a game that can be progressed by invoking the
    ``next_generation`` method.
    """

    __slots__ = ('_driver', '_cells', '_controller',)

    def __init__(self, size: IVector, driver: CellDriver):
        """
        Args:
            size: The size of the game in cells.
            driver: The rules that govern this game.
        """
        self._driver = driver
        self._cells = CellBlock(size, driver.neighbors, driver.empty_state)
        self._controller = CellController(self._cells, self._driver)
        self._controller.populate()

    @property
    def driver(self) -> CellDriver:
        return self._driver

    @property
    def cells(self) -> CellBlock:
        return self._cells

    @property
    def generation(self) -> int:
        return self._controller.generation

    def next_generation(self):
        self._controller.next_generation()
