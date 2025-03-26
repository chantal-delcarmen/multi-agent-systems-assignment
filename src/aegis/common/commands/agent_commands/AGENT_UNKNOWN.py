from typing import override

from aegis.common.commands.agent_command import AgentCommand


class AGENT_UNKNOWN(AgentCommand):
    """Represents an unknown agent command."""

    @override
    def __str__(self) -> str:
        return self.STR_UNKNOWN

    @override
    def proc_string(self) -> str:
        return f"{self._agent_id.proc_string()}#??"
