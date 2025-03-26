from __future__ import annotations

from typing import Protocol, runtime_checkable

from aegis.common.direction import Direction
from aegis.common.location import InternalLocation


# This class only exposes what students can use for Location.
# The autocomplete/LSP will only use functions here.
@runtime_checkable
class Location(Protocol):
    """
    Represents a location in the world.

    Examples:
        >>> loc
        ( X 3 , Y 3 )
        >>> new_loc = loc.add(Direction.NORTH)
        >>> new_loc
        ( X 3 , Y 4 )
        >>> loc.direction_to(new_loc)
        NORTH
        >>> loc.x
        3

    Attributes:
        x (int): The x-coordinate of the location.
        y (int): The y-coordinate of the location.
    """

    x: int
    """The x-coordinate of the location."""
    y: int
    """The y-coordinate of the location."""

    def add(self, direction: Direction) -> Location:
        """
        Adds the given direction to the current location.

        Args:
            direction: The direction to add to the current location.

        Returns:
            A new Location object one unit away in the given direction.
        """
        ...

    def direction_to(self, location: Location) -> Direction:
        """
        Returns the direction from this location to the target location.

        Args:
            location: The target location.

        Returns:
            The direction to the target location.
        """
        ...

    def distance_to(self, location: Location) -> int:
        """
        Calculates the squared distance between the current location
        and the given location.

        Args:
            location: The location to which the distance is calculated.

        Returns:
            The squared distance to the given location.
        """
        ...


def create_location(x: int, y: int) -> Location:
    """
    Create a new Location object.

    Args:
        x: The x-coordinate
        y: The y-coordinate

    Returns:
        A Location object at the specified coordinates
    """
    return InternalLocation(x, y)  # pyright: ignore[reportReturnType]
