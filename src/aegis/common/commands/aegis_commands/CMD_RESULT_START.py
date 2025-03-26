from typing import override

from aegis.common.commands.aegis_command import AegisCommand


class CMD_RESULT_START(AegisCommand):
    """
    Represents the start of the phase where results from
    the agent's last command are returned.

    Attributes:
        results (int): The number of results from the agents last command.
    """

    def __init__(self, results: int) -> None:
        """
        Initializes a CMD_RESULT_START instance.

        Args:
            results: The number of results from the agents last command.
        """
        self.results = results

    @override
    def __str__(self) -> str:
        return f"{self.STR_CMD_RESULT_START} ( {self.results} )"
