# pyright: reportImportCycles = false
# pyright: reportMissingTypeStubs = false
# pyright: reportUnknownMemberType = false
from __future__ import annotations

import sys
from collections import deque

import numpy as np
from aegis import (
    END_TURN,
    AgentCommand,
    AgentID,
    Direction,
    SurroundInfo,
)
from aegis.api import Location
from aegis.common.commands.agent_commands import CONNECT
from aegis.common.location import InternalLocation
from aegis.common.network.aegis_socket import AegisSocket
from aegis.common.network.aegis_socket_exception import AegisSocketException
from a3.aegis_parser import AegisParser
from aegis.common.parsers.aegis_parser_exception import AegisParserException
from aegis.common.world.world import InternalWorld
from numpy.typing import NDArray

import a3.agent.brain
from a3.agent.agent_states import AgentStates


class BaseAgent:
    """Represents a base agent that connects to and interacts with AEGIS."""

    AGENT_PORT: int = 6001
    _agent: BaseAgent | None = None

    def __init__(self) -> None:
        """Initializes a BaseAgent instance."""
        self._round: int = 0
        self._agent_state: AgentStates = AgentStates.CONNECTING
        self._id: AgentID = AgentID(-1, -1)
        self._location: InternalLocation = InternalLocation(-1, -1)
        self._brain: a3.agent.brain.Brain | None = None
        self._energy_level: int = -1
        self._aegis_socket: AegisSocket | None = None
        self._prediction_info: deque[
            tuple[int, NDArray[np.float32] | None, NDArray[np.int64] | None]
        ] = deque()
        self._did_end_turn: bool = False

    @staticmethod
    def get_agent() -> BaseAgent:
        if BaseAgent._agent is None:
            BaseAgent._agent = BaseAgent()
        return BaseAgent._agent

    def update_surround(
        self, surround_info: SurroundInfo, world: InternalWorld | None
    ) -> None:
        if world is None:
            return

        for dir in Direction:
            cell_info = surround_info.get_surround_info(dir)
            if cell_info is None:
                continue

            cell = world.get_cell_at(cell_info.location)
            if cell is None:
                continue

            cell.move_cost = cell_info.move_cost
            cell.set_top_layer(cell_info.top_layer)

    def set_agent_state(self, agent_state: AgentStates) -> None:
        self._agent_state = agent_state

        if agent_state == AgentStates.READ_MAIL:
            self._round += 1

        self.log(f"New State: {self._agent_state}")

    def get_agent_state(self) -> AgentStates:
        return self._agent_state

    def get_round_number(self) -> int:
        """Returns the current round number of the simulation."""
        return self._round

    def get_agent_id(self) -> AgentID:
        """Returns the ID of the base agent."""
        return self._id

    def set_agent_id(self, id: AgentID) -> None:
        self._id = id
        self.log(f"New ID: {self._id}")

    def get_location(self) -> Location:
        """Returns the location of the base agent."""
        return self._location  # pyright: ignore[reportReturnType]

    def set_location(self, location: InternalLocation) -> None:
        self._location = location
        self.log(f"New Location: {self._location}")

    def get_energy_level(self) -> int:
        """Returns the energy level of the base agent."""
        return self._energy_level

    def set_energy_level(self, energy_level: int) -> None:
        self._energy_level = energy_level
        self.log(f"New Energy: {self._energy_level}")

    def get_prediction_info_size(self) -> int:
        """Returns the size of the prediction info queue."""
        return len(self._prediction_info)

    def get_prediction_info(
        self,
    ) -> tuple[int, NDArray[np.float32] | None, NDArray[np.int64] | None]:
        """Returns a prediction info from the queue."""

        if len(self._prediction_info) == 0:
            return -1, None, None
        return self._prediction_info.popleft()

    def add_prediction_info(
        self,
        prediction_info: tuple[
            int, NDArray[np.float32] | None, NDArray[np.int64] | None
        ],
    ) -> None:
        self._prediction_info.append(prediction_info)
        self.log("New Prediction Info!")

    def clear_prediction_info(self) -> None:
        self._prediction_info.clear()
        self.log("Cleared Prediction Info")

    def get_brain(self) -> a3.agent.brain.Brain | None:
        return self._brain

    def set_brain(self, brain: a3.agent.brain.Brain) -> None:
        self._brain = brain
        self.log("New Brain")

    def start_test(self, brain: a3.agent.brain.Brain) -> None:
        self.start("localhost", "test", brain)

    def start_with_group_name(
        self, group_name: str, brain: a3.agent.brain.Brain
    ) -> None:
        self.start("localhost", group_name, brain)

    def start(self, host: str, group_name: str, brain: a3.agent.brain.Brain) -> None:
        if self._agent_state == AgentStates.CONNECTING:
            self._brain = brain
            if self._connect_to_aegis(host, group_name):
                self._run_base_agent_states()
            else:
                self.log("Failed to connect to AEGIS.")
        else:
            self.log("Multiple calls made to start method, ( call ignored )")

    def _connect_to_aegis(self, host: str, group_name: str) -> bool:
        result: bool = False
        for _ in range(5):
            self.log("Trying to connect to AEGIS...")
            try:
                self._aegis_socket = AegisSocket()
                self._aegis_socket.connect(host, self.AGENT_PORT)
                self._aegis_socket.send_message(str(CONNECT(group_name)))
                message = self._aegis_socket.read_message()
                if message is not None and self._brain is not None:
                    self._brain.handle_aegis_command(
                        AegisParser.parse_aegis_command(message)
                    )
                if self.get_agent_state() == AgentStates.CONNECTED:
                    result = True
            except AegisParserException as e:
                print(f"Can't parse/find WorldInfoFile.out -> {e}")
                sys.exit(1)
            except AegisSocketException as e:
                print(f"Can't connect to AEGIS -> {e}")
                sys.exit(1)
            if result:
                break
            else:
                self.log("Failed to connect")
        if result:
            self.log("Connected")
        _ = sys.stdout.flush()
        return result

    def _run_base_agent_states(self) -> None:
        end: bool = False
        while not end:
            try:
                aegis_socket = self._aegis_socket
                if aegis_socket is not None:
                    message = aegis_socket.read_message()
                    try:
                        if message is not None:
                            aegis_command = AegisParser.parse_aegis_command(message)
                            if self._brain is not None:
                                self._brain.handle_aegis_command(aegis_command)
                                agent_state = self._agent_state
                                if agent_state == AgentStates.THINK:
                                    self._brain.think()
                                    self._did_end_turn = False
                                elif agent_state == AgentStates.SHUTTING_DOWN:
                                    end = True
                    except AegisParserException as e:
                        self.log(
                            f"Got AegisParserException '{e}'",
                        )
            except AegisSocketException as e:
                self.log(f"Got AegisSocketException '{e}', shutting down.")
                end = True
            _ = sys.stdout.flush()

        if self._aegis_socket is not None:
            self._aegis_socket.disconnect()

    def send(self, agent_action: AgentCommand) -> None:
        """
        Sends an action command to the AEGIS system.

        Args:
            agent_action: The action command to send.
        """
        if self._aegis_socket is not None and not self._did_end_turn:
            try:
                self._aegis_socket.send_message(str(agent_action))
                if isinstance(agent_action, END_TURN):
                    self._did_end_turn = True
            except AegisSocketException:
                self.log(f"Failed to send {agent_action}")

    def log(self, message: str) -> None:
        """
        Logs a message with the agent's ID and the round number.

        Args:
            message: The message to log.
        """

        agent = self.get_agent()
        agent_id = agent.get_agent_id()
        id_str = f"[Agent#({agent_id.id}:{agent_id.gid})]@{agent.get_round_number()}"
        print(f"{id_str}: {message}")
