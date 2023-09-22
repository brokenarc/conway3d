from abc import ABC, abstractmethod
from typing import Any

import bpy
from mathutils import Vector

from ..config import ConfigType
from conway3d.datamodel.types import IVector

C = bpy.context
D = bpy.data


class CellFactory(ABC):
    @abstractmethod
    def add_cell(self, location: IVector) -> Any:
        """Adds a cell at the given grid space coordinates.

        All other details about the cell are left to the implementation.

        Args:
            location: The cell's grid coordinate

        Returns:
            A reference to the newly created mesh object.
        """

    @abstractmethod
    def add_all_cells(self) -> dict[str, Any]:
        """Creates a cell for each cell block coordinate.

        Returns:
            A dictionary mapping the cell name to the cell's Blender object.
        """


class CubeCellFactory(CellFactory):
    __slots__ = ('_block_size', '_cell_size', '_spacing', '_cell_box',
                 '_center', '_offset', '_cell_name')

    def __init__(self,
        block_size: IVector,
        cell_size: float,
        spacing: float,
        config: ConfigType
    ):
        self._block_size = block_size
        self._cell_size = cell_size
        self._spacing = spacing
        self._cell_name = config.cell_name
        self._cell_box = cell_size + (spacing * 2)

        block_x, block_y, block_z = self._block_size
        self._center = Vector((
            (block_x * self._cell_box) / 2,
            (block_y * self._cell_box) / 2,
            (block_z * self._cell_box) / 2
        ))

        self._offset = Vector((
            (self._cell_box / 2) - self._center.x,
            (self._cell_box / 2) - self._center.y,
            (self._cell_box / 2) - self._center.z,
        ))

    def add_cell(self, location: IVector) -> Any:
        """Adds a cell at the given grid space coordinates.

        The cell is added to the active layer collection.

        Args:
            location: The cell's grid coordinate

        Returns:
            A reference to the newly created mesh object.
        """
        grid_x, grid_y, grid_z = location
        x = (grid_x * self._cell_box) + self._offset.x
        y = (grid_y * self._cell_box) + self._offset.y
        z = (grid_z * self._cell_box) + self._offset.z
        bpy.ops.mesh.primitive_cube_add(size=self._cell_size,
                                        location=Vector((x, y, z)))
        cell = C.object
        cell.name = self._cell_name.format(grid_x, grid_y, grid_z)

        return cell

    def add_all_cells(self) -> dict[str, Any]:
        """Creates a cell for each cell block coordinate.

        Cells are added to the active layer collection.

        Returns:
            A dictionary mapping the cell name to the cell's Blender object.
        """
        block_x, block_y, block_z = self._block_size
        cells = {}
        for z in range(0, block_z):
            for y in range(0, block_y):
                for x in range(0, block_x):
                    cell = self.add_cell((x, y, z))
                    cells[cell.name] = cell

        return cells
