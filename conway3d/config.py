from typing import Type


class Configuration:
    grid_size = (8, 8, 8)
    """The size of the Conway grid measured in number of cells."""

    uncertainty = 0.1
    """The uncertainty factor to use for drivers that support rule fluctuations"""

    cell_size = 1.0
    """The size of each rendered cell in Blender units."""

    cell_padding = 0.25
    """The padding on each side of the cell, in Blender units."""

    cell_name = 'Cell-{:02d}{:02d}{:02d}'
    """The template for canonical name of a cell at a given location. This should accept three
    integer values: z, y, and x grid space coordinates."""

    block_name = 'CellBlock001'
    """The name of the Blender collection that will contain the cells."""


ConfigType = Type[Configuration]
