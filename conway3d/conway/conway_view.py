from typing import Any

import bpy
from mathutils import Vector

from .conway_driver import ConwayCellState
from ..visuals import CellBlockView

ALIVE_SCALE = Vector((1.0, 1.0, 1.0))
DEAD_SCALE = Vector((0.01, 0.01, 0.01))


class ConwayCellView(CellBlockView[ConwayCellState]):

    def add_cell_view(self, size: float, location: Vector) -> None:
        """Adds a cube of ``size`` at ``location``."""
        bpy.ops.mesh.primitive_cube_add(size=size, location=location)

    def update_cell_view(self, cell_view: Any, state: ConwayCellState) -> None:
        """Changes the scale of the cube depending on the state."""
        cell_view.scale = DEAD_SCALE if state == ConwayCellState.DEAD else ALIVE_SCALE
        cell_view.keyframe_insert(data_path='scale')
