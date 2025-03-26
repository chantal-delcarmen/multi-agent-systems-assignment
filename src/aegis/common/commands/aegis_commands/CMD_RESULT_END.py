from typing import override

from aegis.common.commands.aegis_command import AegisCommand


class CMD_RESULT_END(AegisCommand):
    """
    Represents the end of the phase where results from
    the agent's last command are returned.
    """

    @override
    def __str__(self) -> str:
        return self.STR_CMD_RESULT_END
