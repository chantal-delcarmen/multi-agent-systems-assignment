from typing import override

from aegis.agent_control.agent_control import AgentControl


class AgentGroup:
    def __init__(self, gid: int, group_name: str) -> None:
        self.GID: int = gid
        self.id_counter: int = 1
        self.name = group_name
        self.agent_list: list[AgentControl] = []
        self.number_saved_alive: int = 0
        self.number_saved_dead: int = 0
        self.number_saved: int = 0
        self.number_predicted_right: int = 0
        self.number_predicted_wrong: int = 0
        self.number_predicted: int = 0
        self.score: int = 0

    @override
    def __eq__(self, other: object) -> bool:
        if isinstance(other, AgentGroup):
            return self.GID == other.GID
        return False

    @override
    def __hash__(self) -> int:
        hash = 7
        hash = 67 * hash + self.GID
        return hash
