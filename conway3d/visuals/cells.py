from dataclasses import dataclass
from typing import Any

import bpy
from mathutils import Vector

from .cell_factory import CubeCellFactory
from ..blendutil import set_active_layer_collection
from ..config import ConfigType
from ..datamodel import CellBlock, T_state

C = bpy.context
D = bpy.data

class CellBlockView:
    __slots__ = ('_collection', '_cells')

    def __init__(self, cell_block: CellBlock[T_state], config: ConfigType):
        # Create a collection for the cell block and set it active
        self._collection = D.collections.new(config.block_name)
        set_active_layer_collection(config.block_name)

        # Create the individual cells
        factory = CubeCellFactory(cell_block.size, config.cell_size,
                                  config.cell_spacing, config)
        self._cells = factory.add_all_cells()

    @property
    def collection(self) -> Any:
        return self._collection

    @property
    def cells(self) -> dict[str, Any]:
        return self._cells

    def update(self):
        """Update the cells to match the states in the cell block."""
        pass
