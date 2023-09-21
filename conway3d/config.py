from typing import Type


class Configuration:
    grid_size = (8, 8, 8)
    """The size of the Conway grid measured in number of cells."""

    cell_size = 1.0
    """The size of each rendered cell in Blender units."""

    cell_spacing = 0.5
    """The spacing between each cell in Blender units."""

    cell_name = 'Cell-{:02d}{:02d}{:02d}'
    """The template for the cell name object in Blender. This should accept
    three integer values: x, y, and z grid space coordinates."""

    block_name = 'CellBlock001'
    """The name of the Blender collection that will contain the cells."""


ConfigType = Type[Configuration]
