from typing import override

from aegis.common import InternalLocation
from aegis.common.commands.agent_command import AgentCommand


class OBSERVE(AgentCommand):
    """
    Represents a command for an agent to observe a cell in the world.

    Attributes:
        location (Location): The location to observe.
    """

    def __init__(self, location: InternalLocation) -> None:
        """
        Initializes a OBSERVE instance.

        Args:
            location: The location to observe.
        """
        self.location: InternalLocation = location

    @override
    def __str__(self) -> str:
        return f"{self.STR_OBSERVE} {self.location}"

    @override
    def proc_string(self) -> str:
        return f"{self._agent_id.proc_string()}#Observe {self.location.proc_string()}"
