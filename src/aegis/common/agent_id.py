from __future__ import annotations

from typing import override


class AgentID:
    """
    Represents an agent with a unique ID and group ID.

    Attributes:
        id (int): An integer that uniquely identifies the agent within a group.
        gid (int): An integer that represents the group identifier for the agent.
    """

    def __init__(self, id: int, gid: int) -> None:
        """
        Initializes an AgentID with the given ID and GID.

        Args:
            id: The unique identifier of the agent.
            gid: The group identifier of the agent.
        """
        self.id = id
        self.gid = gid

    @override
    def __str__(self) -> str:
        return f"[ ID {self.id} , GID {self.gid} ]"

    @override
    def __repr__(self) -> str:
        return self.__str__()

    def proc_string(self) -> str:
        return f"({self.id}, {self.gid})"

    def clone(self) -> AgentID:
        """
        Creates and returns a new AgentID with the same ID and GID.

        Returns:
            A new AgentID object with same ID and GID as the current instance.
        """
        return AgentID(self.id, self.gid)

    @override
    def __hash__(self) -> int:
        hash_code = 3
        hash_code = 89 * hash_code + self.id
        hash_code = 89 * hash_code + self.gid
        return hash_code

    @override
    def __eq__(self, other: object) -> bool:
        if isinstance(other, AgentID):
            return other.id == self.id and other.gid == self.gid
        return False

    @override
    def __ne__(self, other: object) -> bool:
        if isinstance(other, AgentID):
            return not self.__eq__(other)
        return False

    def __lt__(self, other: object) -> bool:
        if isinstance(other, AgentID):
            if self.gid < other.gid:
                return True
            elif self.gid == other.gid:
                return self.id < other.id
        return False

    def __gt__(self, other: object) -> bool:
        if isinstance(other, AgentID):
            if self.gid > other.gid:
                return True
            elif self.gid == other.gid:
                return self.id > other.id
        return False

    def __le__(self, other: object) -> bool:
        if isinstance(other, AgentID):
            return self.__lt__(other) or self.__eq__(other)
        return False

    def __ge__(self, other: object) -> bool:
        if isinstance(other, AgentID):
            return self.__gt__(other) or self.__eq__(other)
        return False
