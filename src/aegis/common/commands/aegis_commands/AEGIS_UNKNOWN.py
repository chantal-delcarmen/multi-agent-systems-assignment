from typing import override

from aegis.common.commands.aegis_command import AegisCommand


class AEGIS_UNKNOWN(AegisCommand):
    """Represents an unknown command in AEGIS."""

    @override
    def __str__(self) -> str:
        return self.STR_UNKNOWN
