from typing import override

from aegis.common.commands.agent_command import AgentCommand


class SLEEP(AgentCommand):
    """
    Represents a command for an agent to sleep and recharge energy.

    This command must be called on a charging grid when the `Sleep_On_Every` setting is set to false.
    """

    @override
    def __str__(self) -> str:
        return self.STR_SLEEP

    @override
    def proc_string(self) -> str:
        return f"{self._agent_id.proc_string()}#Sleep"
