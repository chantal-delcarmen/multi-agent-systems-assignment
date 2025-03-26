from typing import Protocol, runtime_checkable

from aegis.api.cell import Cell
from aegis.api.location import Location


# This class only exposes what students can use for World.
# The autocomplete/LSP will only use functions here.
@runtime_checkable
class World(Protocol):
    """
    Represents a 2D grid of cells.

    Examples:
        >>> loc = Location(1, 1)
        >>> cell = world.get_cell_at(loc)
        >>> cell
        Cell ( (1,1), Move_Cost 1)
                        {
                        }
        >>> for row in world.get_world_grid():
        ...     for cell in row:
        ...         print(cell)
        ...
        Cell ( (0,0), Move_Cost 1)
                        {
                        }
        Cell ( (0,1), Move_Cost 1)
                        {
                        }
        ...
        Cell ( (2,2), Move_Cost 1)
                        {
                        }
        >>> world.on_map(Location(3,3))
        False
        >>> world.on_map(Location(1,1))
        True
        >>>

    Attributes:
        width (int): The width of the world.
        height (int): The height of the world.
    """

    width: int
    """The width of the world."""
    height: int
    """The height of the world."""

    def get_world_grid(self) -> list[list[Cell]]:
        """Returns the 2D grid representing the world."""
        ...

    def get_cell_at(self, location: Location) -> Cell | None:
        """
        Returns the cell at the given location if it exists.

        Args:
            location: The location of the cell.
        """
        ...

    def on_map(self, location: Location) -> bool:
        """
        Checks if a given location is on the map.

        Args:
            location: The location to check.

        Returns:
            True if the location is on the map, False otherwise.
        """
        ...
