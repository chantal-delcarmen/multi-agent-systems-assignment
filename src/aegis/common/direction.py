from __future__ import annotations

import random
from enum import Enum
from typing import override


class Direction(Enum):
    """
    Enum representing different directions.

    Examples:
        >>> Direction.NORTH
        NORTH
        >>> Direction.SOUTH
        SOUTH
        >>> for dir in Direction:
        ...     print(dir)
        NORTH_WEST
        NORTH
        NORTH_EAST
        EAST
        SOUTH_EAST
        SOUTH
        SOUTH_WEST
        WEST
        CENTER


    Attributes:
        dx (int): The change in the x-coordinate when moving in this direction.
        dy (int): The change in the y-coordinate when moving in this direction.
    """

    NORTH_WEST = (-1, 1)
    """Direction that points northwest (up and left)."""
    NORTH = (0, 1)
    """Direction that points north (up)."""
    NORTH_EAST = (1, 1)
    """Direction that points northeast (up and right)."""
    EAST = (1, 0)
    """Direction that points east (right)."""
    SOUTH_EAST = (1, -1)
    """Direction that points southeast (down and right)."""
    SOUTH = (0, -1)
    """Direction that points south (down)."""
    SOUTH_WEST = (-1, -1)
    """Direction that points southwest (down and left)."""
    WEST = (-1, 0)
    """Direction that points west (left)."""
    CENTER = (0, 0)
    """Direction that points center (not moving)."""

    def __init__(
        self,
        dx: int,
        dy: int,
    ) -> None:
        """
        Initializes a Direction instance.

        Args:
            dx: The change in the x-coordinate when moving in this direction.
            dy: The change in the y-coordinate when moving in this direction.
        """
        self.dx = dx
        self.dy = dy

    @staticmethod
    def get_random_direction() -> Direction:
        """Returns a random Direction."""
        return random.choice(list(Direction))

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return self.__str__()
