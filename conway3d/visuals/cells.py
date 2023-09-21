from abc import ABC, abstractmethod
from math import trunc
from typing import Any

import bpy
from mathutils import Vector

from ..blendutil import set_active_layer_collection
from ..config import ConfigType
from ..conway_logic import CellBlock

C = bpy.context
D = bpy.data


class CellFactory(ABC):
    @abstractmethod
    def add_cell(self, grid_x: int, grid_y: int, grid_z: int) -> Any:
        """Adds a cell at the given grid space coordinates.

        All other details about the cell are left to the implementation.

        Args:
            grid_x:
            grid_y:
            grid_z:

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

    def __init__(self, block_size: Vector, cell_size: float, spacing: float,
                 config: ConfigType):
        self._block_size = block_size
        self._cell_size = cell_size
        self._spacing = spacing
        self._cell_name = config.cell_name
        self._cell_box = cell_size + (spacing * 2)
        self._center = Vector((
            (self._block_size.x * self._cell_box) / 2,
            (self._block_size.y * self._cell_box) / 2,
            (self._block_size.z * self._cell_box) / 2
        ))
        self._offset = Vector((
            (self._cell_box / 2) - self._center.x,
            (self._cell_box / 2) - self._center.y,
            (self._cell_box / 2) - self._center.z,
        ))

    def add_cell(self, grid_x: int, grid_y: int, grid_z: int) -> Any:
        """Adds a cell at the given grid space coordinates.

        The cell is added to the active layer collection.

        Args:
            grid_x:
            grid_y:
            grid_z:

        Returns:
            A reference to the newly created mesh object.
        """
        x = (grid_x * self._cell_box) + self._offset.x
        y = (grid_y * self._cell_box) + self._offset.y
        z = (grid_z * self._cell_box) + self._offset.z
        bpy.ops.mesh.primitive_cube_add(size=self._cell_size,
                                        location=Vector((x, y, z)))
        cell = bpy.context.object
        cell.name = self._cell_name.format(grid_x, grid_y, grid_z)

        return cell

    def add_all_cells(self) -> dict[str, Any]:
        """Creates a cell for each cell block coordinate.

        Cells are added to the active layer collection.

        Returns:
            A dictionary mapping the cell name to the cell's Blender object.
        """
        cells = {}
        for z in range(0, trunc(self._block_size.z)):
            for y in range(0, trunc(self._block_size.y)):
                for x in range(0, trunc(self._block_size.x)):
                    cell = self.add_cell(x, y, z)
                    cells[cell.name] = cell

        return cells


def build_cell_block_visual(cell_block: CellBlock, cell_size: float,
                            spacing: float, config: ConfigType):
    factory = CubeCellFactory(Vector(cell_block.size), cell_size, spacing,
                              config)
    collection = D.collections.new(config.block_name)
    set_active_layer_collection(config.block_name)

    cells = factory.add_all_cells()

    return collection, cells
