from typing import override

from aegis.common.commands.aegis_command import AegisCommand
from aegis.common.world.info import SurroundInfo


class MOVE_RESULT(AegisCommand):
    """
    Represents the result of the agent moving.

    Attributes:
        energy_level (int): The energy_level of the agent.
        surround_info (SurroundInfo): The surrounding info of the agent.
    """

    def __init__(self, energy_level: int, surround_info: SurroundInfo) -> None:
        """
        Initializes a MOVE_RESULT instance.

        Args:
            energy_level: The energy_level of the agent.
            surround_info: The surrounding info of the agent.
        """
        self.energy_level = energy_level
        self.surround_info = surround_info

    @override
    def __str__(self) -> str:
        return f"{self.STR_MOVE_RESULT} ( ENG_LEV {self.energy_level} , {self.surround_info} )"
