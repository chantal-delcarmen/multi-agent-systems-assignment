from typing import override

from aegis.common import AgentIDList
from aegis.common.commands.agent_command import AgentCommand


class SEND_MESSAGE(AgentCommand):
    """
    Represents a command for an agent to send a message to other agents.

    Message is not sent until the beginning of the next round.

    Attributes:
        agent_id_list (AgentIDList): The list of agents to send a message to.
        message (str): The content of the message.
    """

    def __init__(self, agent_id_list: AgentIDList, message: str) -> None:
        """
        Initializes a SEND_MESSAGE instance.

        Args:
            agent_id_list: The list of agents to send a message to.
            message: The content of the message.
        """
        self.agent_id_list = agent_id_list
        self.message = message

    @override
    def __str__(self) -> str:
        return f"{self.STR_SEND_MESSAGE} ( NumTo {self.agent_id_list.size()} , MsgSize {len(self.message)} , ID_List {self.agent_id_list} , MSG {self.message} )"

    @override
    def proc_string(self) -> str:
        return f"{self._agent_id.proc_string()}#Send {self.message} to {self.agent_id_list.proc_string()}"
