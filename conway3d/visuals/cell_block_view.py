from abc import ABC, abstractmethod
from typing import Any, Generic

import bpy
from mathutils import Vector

from ..blendutil import set_active_layer_collection
from ..datamodel import CellBlock, IVector, T_state

C = bpy.context
D = bpy.data


class CellBlockView(ABC, Generic[T_state]):
    __slots__ = (
        '_cells', '_block_name', '_cell_size', '_padding', '_collection', '_meshes')

    def __init__(self,
        cells: CellBlock[T_state],
        block_name: str,
        size: float,
        padding: float
    ):
        self._cells = cells
        self._block_name = block_name
        self._cell_size = size
        self._padding = padding
        self._meshes: dict[IVector, Any] = {}

        # Create a collection for the cell block and set it active
        self._collection = D.collections.new(block_name)
        C.scene.collection.children.link(self._collection)
        set_active_layer_collection(block_name)

        # Create the individual cells
        self.make_meshes()

    def make_meshes(self):
        """Creates a mesh for each cell in the cell block.

        Cells are added to the currently active layer collection.
        """
        sx, sy, sz = self._cells.size
        box = self._cell_size + (self._padding * 2)
        center = Vector((
            (sx * box) / 2,
            (sy * box) / 2,
            (sz * box) / 2
        ))
        offset = Vector((
            (box / 2) - center.x,
            (box / 2) - center.y,
            (box / 2) - center.z
        ))

        for xyz in self._cells:
            grid_x, grid_y, grid_z = xyz
            x = (grid_x * box) + offset.x
            y = (grid_y * box) + offset.y
            z = (grid_z * box) + offset.z
            self.add_cell_view(self._cell_size, Vector((x, y, z)))
            cube = C.object
            cube.name = self._cells.name_of(xyz)
            self._meshes[xyz] = cube

    @property
    def cells(self) -> CellBlock[T_state]:
        return self._cells

    @property
    def name(self) -> str:
        return self._block_name

    @property
    def collection(self) -> Any:
        return self._collection

    @property
    def meshes(self) -> dict[IVector, Any]:
        return self._meshes

    def update(self):
        """Update the cells to match the states of the backing cell block."""
        for (xyz, mesh) in self._meshes.items():
            state = self._cells[xyz]
            self.update_cell_view(mesh, state)

    @abstractmethod
    def add_cell_view(self, size: float, location: Vector) -> None:
        """Adds a Blender object to the active layer collection that will
        represent a grid cell.

        Args:
            size: The size of the object in Blender units.
            location: The location of the object in Blender space.
        """

    @abstractmethod
    def update_cell_view(self, cell_view: Any, state: T_state) -> None:
        """Updates the given Blender object using the given ``state``.

        Args:
            cell_view: The Blender object to adjust.
            state: The state to inform the adjustment.
        """
