from collections.abc import Iterable
from typing import Any

import bpy

C = bpy.context
D = bpy.data

def deselect_all() -> None:
    bpy.ops.object.select_all(action='DESELECT')

def find_3d_view() -> Any:
    """Returns the first screen area with type 'VIEW_3D'

    Returns:
        A reference to the 3D view.
    """
    for area in D.window_managers[0].windows[0].screen.areas:
        if area.type == "VIEW_3D":
            return area.spaces[0]

    return C.space_data

def get_child_by_name(root: Any, name: str):
    """Search an object's children for an item with the given ``name``.

    The algorithm will recursively search the given object's ``children`` attribute and each of
    their ``children`` attributes.

    Args:
        root: any item that has both ``children`` and ``name`` attributes
        name: the item name to search for

    Returns:
        The first item found with the given ``name``, or ``None`` if no item was found.
    """
    if getattr(root, 'name', None) == name:
        return root

    children = getattr(root, 'children', None)
    if isinstance(children, Iterable):
        for child in children:
            found = get_child_by_name(child, name)
            if found:
                return found

    return None


def get_layer_collection(name: str) -> Any:
    """Gets the layer collection identified by ``name``.

    The layer collections will be traversed recursively, and the first one found matching ``name``
    sill be returned.

    Args:
        name: the name of the collection to make active.

    Returns:
        A reference to the named layer collection, or ``None`` if no layer collection was found
        with ``name``.
    """
    return get_child_by_name(C.view_layer.layer_collection, name)


def set_active_layer_collection(name: str) -> Any:
    """Sets the active layer collection to the one identified by ``name``.

    Args:
        name: the name of the collection to make active.

    Returns:
        A reference to the layer collection that is now active, or ``None`` if no layer collection
        was found with ``name``.
    """
    layer_collection = get_layer_collection(name)

    if layer_collection:
        C.view_layer.active_layer_collection = layer_collection

    return layer_collection
