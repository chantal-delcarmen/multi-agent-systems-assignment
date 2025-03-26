from typing import override

from aegis.common.commands.aegis_command import AegisCommand


class DEATH_CARD(AegisCommand):
    """Represents if the agent has died."""

    @override
    def __str__(self) -> str:
        return self.STR_DEATH_CARD
