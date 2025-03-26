from typing import override

from aegis.common.commands.agent_command import AgentCommand


class END_TURN(AgentCommand):
    """
    Represents a command that allows an agent to
    tell the server it is done with its turn.

    Examples:
        >>> END_TURN()
        END_TURN
    """

    @override
    def __str__(self) -> str:
        return self.STR_END_TURN

    @override
    def proc_string(self) -> str:
        return f"{self._agent_id.proc_string()}#End Turn"
