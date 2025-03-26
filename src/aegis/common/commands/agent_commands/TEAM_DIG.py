from typing import override

from aegis.common.commands.agent_command import AgentCommand


class TEAM_DIG(AgentCommand):
    """
    Represents a command for an agent to dig rubble.

    If a piece of rubble needs more then one agent to remove it then
    all the needed agents need to move onto the cell and send the
    TEAM_DIG command during the same round.
    """

    @override
    def __str__(self) -> str:
        return self.STR_TEAM_DIG

    @override
    def proc_string(self) -> str:
        return f"{self._agent_id.proc_string()}#Team Dig"
