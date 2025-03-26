from __future__ import annotations

from typing import cast, override

from aegis.common.world.objects.world_object import WorldObject
from aegis.parsers.helper.world_file_type import StackContent


class Rubble(WorldObject):
    """
    Represents a rubble layer in a cell.

    Attributes:
        id (int): The id of the rubble.
        remove_energy (int): The amount of energy to remove the rubble.
        remove_agents (int): The amount of agents to remove the rubble.
    """

    def __init__(
        self, id: int = -1, remove_energy: int = 1, remove_agents: int = 1
    ) -> None:
        """
        Initializes a Rubble instance.

        Args:
            id: The id of the rubble.
            remove_energy: The amount of energy to remove the rubble.
            remove_agents: The amount of agents to remove the rubble.
        """
        super().__init__()
        self.id = id
        self.remove_energy = remove_energy
        self.remove_agents = remove_agents

    @override
    def __str__(self) -> str:
        return f"RUBBLE ( ID {self.id} , NUM_TO_RM {self.remove_agents} , RM_ENG {self.remove_energy} )"

    @override
    def __repr__(self) -> str:
        return self.__str__()

    @override
    def get_name(self) -> str:
        return "Rubble"

    @override
    def get_life_signal(self) -> int:
        return 0

    @override
    def file_output_string(self) -> str:
        return f"RB({self.remove_energy},{self.remove_agents})"

    @override
    def string_information(self) -> list[str]:
        string_information = super().string_information()
        string_information.append(f"Remove Energy = {self.remove_energy}")
        string_information.append(f"Remove Agents = {self.remove_agents}")
        return string_information

    @override
    def clone(self) -> Rubble:
        rubble = cast(Rubble, super().clone())
        rubble.remove_energy = self.remove_energy
        rubble.remove_agents = self.remove_agents
        return rubble

    @override
    def json(self) -> StackContent:
        return {
            "type": "rb",
            "arguments": {
                "remove_energy": self.remove_energy,
                "remove_agents": self.remove_agents,
            },
        }
