from typing import Protocol, runtime_checkable

from aegis.api.location import Location
from aegis.common.world.objects.world_object import WorldObject


# This class only exposes what students can use for Cell.
# The autocomplete/LSP will only use functions here.
@runtime_checkable
class Cell(Protocol):
    """
    Represents a cell in the world.

    Examples:
        >>> top_layer = cell.get_top_layer()
        >>> top_layer
        None    # Will return None when there are no layers.
        >>> cell.is_normal_cell()
        True
        >>> cell.is_fire_cell()
        False
        >>> cell.is_killer_cell()
        False
        >>> cell.is_charging_cell()
        False

    Attributes:
        move_cost (int): The movement cost associated with the cell.
        location (Location): The location of the cell on the map.
        has_survivors (bool): If there are survivors in the cell.
    """

    move_cost: int
    """The movement cost associated with the cell."""
    location: Location
    """The location of the cell on the map."""
    has_survivors: bool
    """If there are survivors in the cell."""

    def get_top_layer(self) -> WorldObject | None:
        """
        Returns the top layer of the cell without removing it if the cell has layers.

        Returns:
            The top layer, or None if the cell has no layers.
        """
        ...

    def is_charging_cell(self) -> bool:
        """
        Checks if the cell is of type CHARGING_CELL.

        Returns:
            True if the cell type is CHARGING_CELL, False otherwise.
        """
        ...

    def is_fire_cell(self) -> bool:
        """
        Checks if the cell is of type FIRE_CELL.

        Returns:
            True if the cell type is FIRE_CELL, False otherwise.
        """
        ...

    def is_killer_cell(self) -> bool:
        """
        Checks if the cell is of type KILLER_CELL.

        Returns:
            True if the cell type is KILLER_CELL, False otherwise.
        """
        ...

    def is_normal_cell(self) -> bool:
        """
        Checks if the cell is of type NORMAL_CELL.

        Returns:
            True if the cell type is NORMAL_CELL, False otherwise.
        """
        ...
