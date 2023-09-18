# from typing import Generic, cast
#
# from .cell_driver import CellDriver, T_CELL_STATE

#
# class CellBlock(Generic[T_CELL_STATE]):
#     __slots__ = ('_x_size', '_y_size', '_z_size', '_cells',
#                  '_driver',)
#
#     def __init__(self, x_size: int, y_size: int, z_size: int,
#                  driver: CellDriver[T_CELL_STATE]):
#         self._x_size = x_size
#         self._y_size = y_size
#         self._z_size = z_size
#         self._driver = driver
#         self._cells = [driver.default_state()] * (x_size * y_size * z_size)
#
#     def __len__(self) -> int:
#         return len(self._cells)
#
#     def __getitem__(self, item):
#         return self._cells[item]
#
#     @property
#     def x_size(self) -> int:
#         return self._x_size
#
#     @property
#     def y_size(self) -> int:
#         return self._y_size
#
#     @property
#     def z_size(self) -> int:
#         return self._z_size
#
#     def _get_index(self, x: int, y: int, z: int) -> int:
#         """Compute the cell array index from x, y, z coordinates.
#
#         Returns:
#             The index of the cell at the given coordinates, or -1 if the
#             coordinates are outside the bounds of the block.
#         """
#         if ((0 <= x < self._x_size) and (0 <= y < self._y_size) and
#             (0 <= z < self.z_size)):
#             return x + (y * self._x_size) + (z * self._x_size * self._y_size)
#
#         return -1
#
#     def get_cell(self, x: int, y: int, z: int):
#         return self._cells[self._get_index(x, y, z)]
#
#     def get_neighbor_indexes(self, x: int, y: int, z: int) -> tuple[int]:
#         cell = self._get_index(x, y, z)
#         indexes = [
#             self._get_index(xx, yy, zz)
#             for zz in (z - 1, z, z + 1)
#             for yy in (y - 1, y, y + 1)
#             for xx in (x - 1, x, x + 1)
#         ]
#
#         # filter out the negative indexes and the original cell
#         neighbors = filter(
#             lambda i: (i != cell) and (0 <= i < len(self._cells)),
#             indexes
#         )
#
#         return cast(tuple[int], tuple(neighbors))
#
#     def get_neighbor_count(self, x: int, y: int, z: int) -> int:
#         return len(self.get_neighbor_indexes(x, y, z))
#
#     def next_generation(self):
#         next_cells = self._cells.copy()
#
#         for z in range(0, self._z_size):
#             for y in range(0, self._y_size):
#                 for x in range(0, self._x_size):
#                     index = self._get_index(x, y, z)
#                     next_cells[index] = self._driver.next_state(
#                         self._cells[index],
#                         neighbor_count=self.get_neighbor_count(x, y, z),
#                         block=self
#                     )
#         self._cells = next_cells
