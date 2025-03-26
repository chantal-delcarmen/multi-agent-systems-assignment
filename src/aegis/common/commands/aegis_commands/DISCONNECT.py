from typing import override

from aegis.common.commands.aegis_command import AegisCommand


class DISCONNECT(AegisCommand):
    """Represents if the agent has disconnected and the system has shutdown."""

    @override
    def __str__(self) -> str:
        return self.STR_DISCONNECT
