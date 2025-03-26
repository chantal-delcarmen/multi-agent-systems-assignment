from typing import override

from aegis.common import AgentID, InternalLocation
from aegis.common.commands.aegis_command import AegisCommand


class CONNECT_OK(AegisCommand):
    """
    Represents the result of the agent successfully connecting to AEGIS.

    Attributes:
        new_agent_id (AgentID): The unique AgentID of the new agent.
        energy_level (int): The start energy level of the new agent.
        location (Location): The start location of the new agent.
        world_filename (str): The world file being used.
    """

    def __init__(
        self,
        new_agent_id: AgentID,
        energy_level: int,
        location: InternalLocation,
        world_filename: str,
    ) -> None:
        """
        Initializes a CONNECT_OK instance.

        Args:
            new_agent_id: The unique AgentID of the new agent.
            energy_level: The start energy level of the new agent.
            location: The start location of the new agent.
            world_filename: The world file being used.
        """
        self.new_agent_id: AgentID = new_agent_id
        self.energy_level: int = energy_level
        self.location: InternalLocation = location
        self.world_filename: str = world_filename

    @override
    def __str__(self) -> str:
        return f"{self.STR_CONNECT_OK} ( ID {self.new_agent_id.id} , GID {self.new_agent_id.gid} , ENG_LEV {self.energy_level} , LOC {self.location} , FILE {self.world_filename} )"
