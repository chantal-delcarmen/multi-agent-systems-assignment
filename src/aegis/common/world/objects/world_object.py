from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from enum import Enum
from typing import override

from aegis.parsers.helper.world_file_type import StackContent


class WorldObject(ABC):
    """
    Represents an object in the world.

    Attributes:
        id (int): The id of the world object.

    Raises:
        RuntimeError: If there is an issue while cloning the world object.
    """

    class State(Enum):
        """Enum for the state of a world object."""

        EXIST = 1
        ALIVE = 2
        DEAD = 3

    def __init__(self) -> None:
        """Initializes a WorldObject instance."""
        self._state = self.State.EXIST
        self.id: int = -1

    def is_exist(self) -> bool:
        """
        Checks if the world object is in the EXIST state.

        Returns:
            True if the object is in the EXIST state, False otherwise.
        """
        return self._state == self.State.EXIST

    def is_alive(self) -> bool:
        """
        Checks if the world object is in the ALIVE state.

        Returns:
            True if the object is in the ALIVE state, False otherwise.
        """
        return self._state == self.State.ALIVE

    def is_dead(self) -> bool:
        """
        Checks if the world object is in the DEAD state.

        Returns:
            True if the object is in the DEAD state, False otherwise.
        """
        return self._state == self.State.DEAD

    def set_exist(self) -> None:
        self._state = self.State.EXIST

    def set_alive(self) -> None:
        self._state = self.State.ALIVE

    def set_dead(self) -> None:
        self._state = self.State.DEAD

    @abstractmethod
    @override
    def __str__(self) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_life_signal(self) -> int:
        pass

    @abstractmethod
    def file_output_string(self) -> str:
        pass

    @abstractmethod
    def json(self) -> StackContent:
        pass

    def string_information(self) -> list[str]:
        return [f"State = {self._state}", f"ID = {self.id}"]

    def clone(self) -> WorldObject:
        """
        Creates and returns a deep copy of the world object.

        Returns:
            A new instance of WorldObject with the same attributes.

        Raises:
            RuntimeError: If an error occurs during cloning.
        """
        try:
            copy_object = copy.deepcopy(self)
            copy_object._state = self._state
            copy_object.id = self.id
            return copy_object
        except Exception as e:
            raise RuntimeError(f"Internal error when cloning WorldObject: {e}")
