from typing import override

from aegis.common.commands.agent_command import AgentCommand


class SAVE_SURV(AgentCommand):
    """
    Represents a command for an agent to save a survivor

    Examples:
        >>> SAVE_SURV()
        SAVE_SURV
    """

    @override
    def __str__(self) -> str:
        return self.STR_SAVE_SURV

    @override
    def proc_string(self) -> str:
        return f"{self._agent_id.proc_string()}#Save SV"
