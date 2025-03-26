from typing import override

from aegis.common.commands.aegis_command import AegisCommand


class ROUND_END(AegisCommand):
    """Represents the end of a round."""

    @override
    def __str__(self) -> str:
        return self.STR_ROUND_END
