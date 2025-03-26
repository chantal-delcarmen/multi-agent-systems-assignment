from typing import cast, override

from aegis.common.world.objects.world_object import WorldObject
from aegis.parsers.helper.world_file_type import StackContent


class SurvivorGroup(WorldObject):
    """
    Represents a survivor group layer in a cell.

    Attributes:
        id (int): The id of the survivor group.
        number_of_survivors (int): The number of survivors in the group.
    """

    def __init__(
        self, id: int = -1, energy_level: int = 1, number_of_survivors: int = 1
    ) -> None:
        """
        Initializes a SurvivorGroup instance.

        Args:
            id: The id of the survivor instance.
            energy_level: The energy_level of the survivor group.
            number_of_survivors: The number of survivors in the group.
        """
        super().__init__()
        self._state = self.State.ALIVE
        self.id = id
        self.number_of_survivors = number_of_survivors
        self.set_energy_level(energy_level)

    def get_energy_level(self) -> int:
        """Returns the energy level of the survivor group."""
        return self._energy_level

    def set_energy_level(self, energy_level: int) -> None:
        self._energy_level = energy_level
        if energy_level <= 0:
            self.set_dead()
        else:
            self.set_alive()

    def remove_energy(self, remove_energy: int) -> None:
        if remove_energy < self._energy_level:
            self._energy_level -= remove_energy
        else:
            self._energy_level = 0
            self.set_dead()

    @override
    def __str__(self) -> str:
        return f"SURVIVOR_GROUP ( ID {self.id} , NUM_SV {self.number_of_survivors} , ENG_LV {self._energy_level} )"

    @override
    def __repr__(self) -> str:
        return self.__str__()

    @override
    def get_name(self) -> str:
        return "Survivor Group"

    @override
    def get_life_signal(self) -> int:
        return self._energy_level

    @override
    def file_output_string(self) -> str:
        return f"SVG({self._energy_level},{self.number_of_survivors})"

    @override
    def string_information(self) -> list[str]:
        string_information = super().string_information()
        string_information.append(f"Energy Level = {self._energy_level}")
        string_information.append(f"Number of SV = {self.number_of_survivors}")
        return string_information

    @override
    def clone(self) -> WorldObject:
        survivor_group = cast(SurvivorGroup, super().clone())
        survivor_group._energy_level = self._energy_level
        survivor_group.number_of_survivors = self.number_of_survivors
        return survivor_group

    @override
    def json(self) -> StackContent:
        return {
            "type": "svg",
            "arguments": {
                "energy_level": self._energy_level,
                "number_of_survivors": self.number_of_survivors,
            },
        }
