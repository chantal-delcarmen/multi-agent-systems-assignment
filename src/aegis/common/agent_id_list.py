from __future__ import annotations

from collections.abc import Iterator
from typing import override

from aegis.common.agent_id import AgentID


class AgentIDList:
    """Represents a list of AgentID instances."""

    def __init__(self, agent_id_list: list[AgentID] | None = None) -> None:
        """
        Initializes an AgentIDList with the provided list of AgentID instances.

        Args:
            agent_id_list: An optional list of AgentID instances.
        """
        self._agent_id_list = agent_id_list or []

    def add(self, agent_id: AgentID) -> None:
        """
        Add an AgentID instance to the list if not already present.

        Args:
            agent_id: An AgentID instance.
        """
        if agent_id not in self._agent_id_list:
            self._agent_id_list.append(agent_id)

    def add_all(self, agent_id_list: list[AgentID] | AgentIDList) -> None:
        """
        Adds all AgentID instances from another list or AgentIDList to the current list.

        Args:
            agent_id_list: A list of AgentID instances or an AgentIDList.
        """
        for agent_id in agent_id_list:
            self.add(agent_id)

    def remove(self, agent_id: AgentID) -> None:
        """
        Removes an AgentID instance from the list if it exists.

        Args:
            agent_id: The AgentID instance to remove.
        """
        self._agent_id_list.remove(agent_id)

    def remove_all(self, agent_id_list: list[AgentID]) -> None:
        """
        Removes all specified AgentID instances from the list.

        Args:
            agent_id_list: A list of AgentID instances to remove.
        """
        for agent_id in agent_id_list:
            self.remove(agent_id)

    def size(self) -> int:
        """Returns the number of AgentID instances in the list."""
        return len(self._agent_id_list)

    def clone(self) -> AgentIDList:
        """
        Creates and returns a copy of the current AgentIDList instance.

        Returns:
            A new AgentIDList object with same AgentID instances as the current instance.
        """
        copy = AgentIDList()
        for agent in self._agent_id_list:
            copy.add(agent.clone())
        return copy

    @override
    def __str__(self) -> str:
        if not self._agent_id_list:
            return "( )"
        return f"( {' , '.join(str(agent_id) for agent_id in self._agent_id_list)} )"

    @override
    def __repr__(self) -> str:
        return self.__str__()

    def proc_string(self) -> str:
        if not self._agent_id_list:
            return "all"
        return f"({', '.join(str(agent_id.proc_string()) for agent_id in self._agent_id_list)})"

    def __iter__(self) -> Iterator[AgentID]:
        return iter(self._agent_id_list)

    def is_empty(self) -> bool:
        """
        Checks if the AgentIDList is empty.

        Returns:
            True if the AgentIDList is empty, False otherwise.
        """
        return not self._agent_id_list

    def clear(self) -> None:
        """Clears all AgentID instances from the list."""
        self._agent_id_list.clear()

    def remove_at(self, index: int) -> AgentID:
        """
        Removes and returns the AgentID instance at the given index.

        Args:
            index: The index of the AgentID instance to remove

        Returns:
            The AgentID instance at the given index.
        """
        return self._agent_id_list.pop(index)
