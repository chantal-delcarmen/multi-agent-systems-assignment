from typing import override

from aegis.common.commands.aegis_command import AegisCommand


class ROUND_START(AegisCommand):
    """Represents the start of a round."""

    @override
    def __str__(self) -> str:
        return self.STR_ROUND_START
