from abc import ABC, abstractmethod
from typing import Any

import bpy
from mathutils import Vector

from .blendutil import get_child_by_name

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


class CubeCellFactory(CellFactory):
    __slots__ = ('_block_size', '_cell_size', '_spacing', '_cell_box',
                 '_center', '_offset')

    def __init__(self, block_size: Vector, cell_size: float, spacing: float):
        self._block_size = block_size
        self._cell_size = cell_size
        self._spacing = spacing
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
        x = (grid_x * self._cell_box) + self._offset.x
        y = (grid_y * self._cell_box) + self._offset.y
        z = (grid_z * self._cell_box) + self._offset.z
        bpy.ops.mesh.primitive_cube_add(size=self._cell_size,
                                        location=Vector((x, y, z)))
        cell = bpy.context.object
        cell.name = 'Cell-{:02d}{:02d}{:02d}'.format(grid_x, grid_y, grid_z)

        return cell


def cell_block():
    collection = D.collections.new('CellBlock001')
    C.scene.collection.children.link(collection)
    # collection.objects.link(cell)
    #  C.view_layer.active_layer_collection = C.view_layer.layer_collection.children[-1]
    b = get_child_by_name(None, "test")


# https://blenderartists.org/t/how-do-i-set-a-collection-to-be-active/1445630/3
"""
import bpy
C = bpy.context
D = bpy.data

layer_collection = C.view_layer.layer_collection
for coll in layer_collection.collection.children_recursive:
    if not coll.hide_render:
        layerColl = recurLayerCollection(layer_collection, coll.name)
        C.view_layer.active_layer_collection = layerColl
        filename = C.blend_data.filepath.replace(".blend", "") + "_" + coll.name + ".glb"
        print("+" + filename)
        bpy.ops.export_scene.gltf(filepath=filename, use_active_collection=True, use_renderable=True,export_apply=True)
"""
