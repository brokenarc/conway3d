import bpy

from . import Configuration
from .blendutil import deselect_all, find_3d_view
from .conway import ConwayCellView, UncertainConwayDriver
from .datamodel import CellBlock

C = bpy.context
D = bpy.data

CONFIG = Configuration


def setup_renderer():
    C.scene.render.engine = 'BLENDER_EEVEE'
    C.scene.eevee.use_bloom = True

    space = find_3d_view()
    space.shading.type = 'RENDERED'
    space.overlay.show_floor = False
    space.overlay.show_axis_x = False
    space.overlay.show_axis_y = False
    space.overlay.show_cursor = False
    space.overlay.show_object_origins = False


def setup_scene():
    D.worlds['World'].node_tree.nodes['Background'].inputs[0].default_value = (0.03, 0.0, 0.06, 1)
    deselect_all()
    # TODO - configure lights and camera


def setup_animation(start_frame: int, end_frame: int):
    C.scene.frame_start = start_frame
    C.scene.frame_end = end_frame
    C.scene.frame_current = start_frame


FRAMES = 200


def create_animation():
    driver = UncertainConwayDriver(CellBlock(CONFIG.grid_size), uncertainty=0.05)
    cell_view = ConwayCellView(driver.cells, CONFIG.block_name, CONFIG.cell_size,
                               CONFIG.cell_padding)

    setup_renderer()
    setup_scene()
    setup_animation(0, FRAMES)

    driver.populate()
    cell_view.update()

    for frame in range(0, FRAMES, 10):
        bpy.context.scene.frame_set(frame)
        cell_view.update()
        driver.next_generation()
