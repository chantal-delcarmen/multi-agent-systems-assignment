from typing import override

from aegis.common import AgentID, AgentIDList
from aegis.common.commands.aegis_command import AegisCommand


class SEND_MESSAGE_RESULT(AegisCommand):
    """
    Represents a message that came from another agent.

    Attributes:
        from_agent_id (AgentID): The AgentID of the agent sending the message.
        agent_id_list (AgentIDList): The list of agents who are supposed to receive the message.
        msg (str): The content of the message.
    """

    def __init__(
        self, from_agent_id: AgentID, agent_id_list: AgentIDList, msg: str
    ) -> None:
        """
        Initializes a new SEND_MESSAGE_RESULT instance.

        Args:
            from_agent_id: The AgentID of the agent sending the message.
            agent_id_list: The list of agents who are supposed to receive the message.
            msg: The content of the message.
        """
        self.from_agent_id = from_agent_id
        self.agent_id_list = agent_id_list
        self.msg = msg
        self._number_left_to_read = agent_id_list.size()

    @override
    def __str__(self) -> str:
        return f"{self.STR_SEND_MESSAGE_RESULT} ( IDFrom ( {self.from_agent_id.id} , {self.from_agent_id.gid} ) , MsgSize {len(self.msg)} , NUM_TO {self.agent_id_list.size()} , IDS {self.agent_id_list} , MSG {self.msg} )"

    def get_number_left_to_read(self) -> int:
        return self._number_left_to_read

    def set_number_left_to_read(self, number_left_to_read: int) -> None:
        self._number_left_to_read = number_left_to_read

    def decrease_number_left_to_read(self) -> None:
        if self._number_left_to_read <= 0:
            return
        self._number_left_to_read -= 1

    def increase_number_left_to_read(self, number_read_inc: int) -> None:
        if number_read_inc > 0:
            self._number_left_to_read += number_read_inc
