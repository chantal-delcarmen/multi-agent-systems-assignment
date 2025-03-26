from typing import override

from aegis.agent_control.network.agent_socket import AgentSocket
from aegis.common.agent_id import AgentID
from aegis.common.commands.aegis_command import AegisCommand
from aegis.common.commands.aegis_commands import SEND_MESSAGE_RESULT


class AgentControl:
    def __init__(self, agent_id: AgentID) -> None:
        self.agent_id: AgentID = agent_id
        self.agent_socket: AgentSocket | None = None
        self.mailbox1: list[SEND_MESSAGE_RESULT] = []
        self.mailbox2: list[SEND_MESSAGE_RESULT] = []
        self.result_of_command: AegisCommand | None = None

    @override
    def __eq__(self, other: object) -> bool:
        if isinstance(other, AgentControl):
            return self.agent_id == other.agent_id
        return False

    @override
    def __hash__(self) -> int:
        return hash(self.agent_id)

    def __del__(self):
        try:
            if self.agent_socket is not None:
                self.agent_socket.disconnect()
        except Exception as e:
            print(f"Error while disconnecting socket: {str(e)}")
