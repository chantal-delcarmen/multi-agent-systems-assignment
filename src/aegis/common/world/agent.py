from __future__ import annotations

from typing import override

from aegis.common import AgentID, Constants, Direction, InternalLocation


class Agent:
    """
    Represents an agent in the simulation.

    Attributes:
        agent_id (AgentID): The unique AgentID of the agent.
        location (InternalLocation): The starting location of the agent.
        orientation (Direction): The current orientation of the agent.
        command_sent (str): The last command sent by the agent.
    """

    def __init__(
        self,
        agent_id: AgentID,
        location: InternalLocation,
        energy_level: int = Constants.DEFAULT_MAX_ENERGY_LEVEL,
    ) -> None:
        """
        Initializes an Agent instance.

        Args:
            agent_id: The unique AgentID of the agent.
            location: The starting location of the agent.
            energy_level: The starting energy level of the agent.
        """
        self.agent_id: AgentID = agent_id
        self.location: InternalLocation = location
        self._energy_level: int = energy_level
        self.orientation: Direction = Direction.CENTER
        self.command_sent: str = "None"
        self.steps_taken: int = 0

    def get_energy_level(self) -> int:
        """Returns the energy level of the agent."""
        return self._energy_level

    def set_energy_level(self, energy_level: int) -> None:
        """
        Sets the energy level of the agent.

        If the specified energy level is less than or equal to zero, the agent's
        state will be set to DEAD. Otherwise, the agent will be deemed ALIVE.

        Args:
            energy_level: The new energy level of the agent.
        """
        self._energy_level = energy_level

    def add_energy(self, energy: int) -> None:
        """
        Adds the specified amount of energy to the agent's current energy level.

        The amount of energy added must be non-negative. If a negative value is
        passed, it will be ignored and the agent's energy level will remain unchanged.

        Args:
            energy: The amount of energy to add.
        """
        if energy >= 0:
            self._energy_level += energy

    def remove_energy(self, energy: int) -> None:
        """
        Removes the specified amount of energy from the agent's current energy level.

        If the specified amount of energy to remove is greater than or equal to the
        current energy level, the agent is deemed DEAD.

        Args:
            energy: The amount of energy to remove.
        """
        if energy < self._energy_level:
            self._energy_level -= energy
        else:
            self._energy_level = 0

    def add_step_taken(self) -> None:
        """Increments the number of steps taken by the agent."""
        self.steps_taken += 1

    @override
    def __str__(self) -> str:
        return str(self.agent_id)

    def string_information(self) -> list[str]:
        """Returns a list of strings representing the agent's attributes."""
        return [
            f"AgentID       = {self.agent_id}",
            f"Location      = {self.location}",
            f"Energy Level  = {self._energy_level}",
            f"Command Sent  = {self.command_sent}",
        ]

    def clone(self) -> Agent:
        """
        Creates and returns a new Agent instance with the same attributes as the current instance.

        Returns:
            Agent: A new Agent object with the same ID, location, energy level, state, orientation, and command history.
        """
        agent = Agent(self.agent_id, self.location, self._energy_level)
        agent.orientation = self.orientation
        agent.command_sent = self.command_sent
        return agent
