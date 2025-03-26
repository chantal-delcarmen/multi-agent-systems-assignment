from typing import override

from aegis.common.commands.aegis_command import AegisCommand


class MESSAGES_END(AegisCommand):
    """Represents the end of the message phase in AEGIS."""

    @override
    def __str__(self) -> str:
        return self.STR_MESSAGES_END
