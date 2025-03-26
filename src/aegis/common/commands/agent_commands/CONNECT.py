from typing import override

from aegis.common.commands.agent_command import AgentCommand


class CONNECT(AgentCommand):
    """
    Represents an agent currently connecting to AEGIS.

    Attributes:
        group_name (str): The group name for the agent.
    """

    def __init__(self, group_name: str) -> None:
        """
        Initializes a CONNECT instance.

        Args:
            group_name: The group name for the agent.
        """
        self.group_name = group_name

    @override
    def __str__(self) -> str:
        return f"{self.STR_CONNECT} ( {self.group_name} )"

    @override
    def proc_string(self) -> str:
        return f"{self._agent_id.proc_string()}#Connect"
