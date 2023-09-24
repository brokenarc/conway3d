from typing import Callable

from conway3d.datamodel.types import IVector

NeighborModel = Callable[[IVector], list[IVector]]
"""Defines the signature for a function that will accept a cell's location and then return the
locations of cells that are considered to be that cell's neighbors.

It is left to the user to determine if the returned locations are within any desired boundary
constraints.

Implementations must exclude the original cell's location from the resulting list of neighbor cell
locations.

Args:
    IVector: The cell location

Returns:
    list[IVector]: The locations of cells that are considered neighbors to the given cell.
"""


def simple_neighbor_model(location: IVector) -> list[IVector]:
    """Returns cells that share one side with the given cell.

    Args:
        location: The cell location

    Returns:
        The locations of cells that are neighbors to the given cell.
    """
    x, y, z = location
    return [
        (x - 1, y, z), (x + 1, y, z),
        (x, y - 1, z), (x, y + 1, z),
        (x, y, z + 1), (x, y, z - 1)
    ]


def cubic_neighbor_model(location: IVector) -> list[IVector]:
    """Returns cells that share one side or one corner with the given cell.

    Args:
        location: The cell location

    Returns:
        The locations of cells that are neighbors to the given cell.
    """
    x, y, z = location
    coords = [
        (xx, yy, zz)
        for zz in (z - 1, z, z + 1)
        for yy in (y - 1, y, y + 1)
        for xx in (x - 1, x, x + 1)
    ]
    coords.remove(location)

    return coords
