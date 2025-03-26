from aegis.common import Constants, InternalLocation
from aegis.common.world.cell import InternalCell


class InternalWorld:
    """
    Represents a 2D grid of cells.

    Attributes:
        width (int): The width of the world.
        height (int): The height of the world.

    Raises:
        ValueError: If both initializing methods are None or both were passed or if invalid dimensions are provided during initialization.
    """

    def __init__(
        self,
        world: list[list[InternalCell]] | None = None,
        width: int = 0,
        height: int = 0,
    ) -> None:
        """
        Initializes a World instance.

        The world can be initialized with either an existing grid or with
        specific dimensions to create an empty grid.

        Args:
            world: An optional 2D grid to initialize the world.
            width: The width of the world if initializing with dimensions.
            height: The height of the world if initializing with dimensions.

        Raises:
            ValueError: If both initializing methods are None or both were passed.
        """
        if world is not None and (width == 0 and height == 0):
            self.height: int = len(world[0])
            self.width: int = len(world)
            self._world: list[list[InternalCell]] = world
        elif width > 0 and height > 0 and world is None:
            self.height = height
            self.width = width
            self._world = [
                [InternalCell(x, y) for y in range(height)] for x in range(width)
            ]
        else:
            raise ValueError(
                "Either 'world' OR 'width and height' must be passed into the class"
            )

        self._isValidMap()

    def _isValidMap(self) -> None:
        """
        Validates that the map dimesions are within the allowed range.

        Raises:
            ValueError: If the dimensions are not within the allowed range.
        """
        if self.width < Constants.WORLD_MIN:
            raise ValueError(f"World width must be larger than {Constants.WORLD_MIN}")

        if self.width > Constants.WORLD_MAX:
            raise ValueError(f"World width must be beneath {Constants.WORLD_MAX}")

        if self.height < Constants.WORLD_MIN:
            raise ValueError(f"World height must be larger than {Constants.WORLD_MIN}")

        if self.height > Constants.WORLD_MAX:
            raise ValueError(f"World height must be beneath {Constants.WORLD_MAX}")

    def get_world_grid(self) -> list[list[InternalCell]]:
        """Returns the 2D grid representing the world."""
        return self._world

    def set_world_grid(self, world: list[list[InternalCell]]) -> None:
        self.height = len(world[0])
        self.width = len(world)
        self._world = world

    def on_map(self, location: InternalLocation) -> bool:
        """
        Checks if a given location is on the map.

        Args:
            location: The location to check.

        Returns:
            True if the location is on the map, False otherwise.
        """
        return (
            location.x >= 0
            and location.y >= 0
            and location.x < self.width
            and location.y < self.height
        )

    def set_cell_at(self, location: InternalLocation, cell: InternalCell) -> None:
        if self.on_map(location):
            self._world[location.x][location.y] = cell

    def get_cell_at(self, location: InternalLocation) -> InternalCell | None:
        """
        Returns the cell at the given location if it exists.

        Args:
            location: The location of the cell.
        """
        if not self.on_map(location):
            return None
        return self._world[location.x][location.y]
