from typing import override

# If you need to import anything, add it to the import below.
from aegis import (
    END_TURN,
    SEND_MESSAGE_RESULT,
    MOVE,
    OBSERVE_RESULT,
    PREDICT_RESULT,
    SAVE_SURV,
    SAVE_SURV_RESULT,
    SEND_MESSAGE,
    TEAM_DIG,
    AgentCommand,
    AgentIDList,
    Direction,
    Rubble,
    Survivor,
)
from a3.agent import BaseAgent, Brain, AgentController


class ExampleAgent(Brain):
    def __init__(self) -> None:
        super().__init__()
        self._agent: AgentController = BaseAgent.get_agent()

    @override
    def handle_send_message_result(self, smr: SEND_MESSAGE_RESULT) -> None:
        self._agent.log(f"SEND_MESSAGE_RESULT: {smr}")
        self._agent.log(f"{smr}")
        print("#--- You need to implement handle_send_message_result function! ---#")

    @override
    def handle_observe_result(self, ovr: OBSERVE_RESULT) -> None:
        self._agent.log(f"OBSERVE_RESULT: {ovr}")
        self._agent.log(f"{ovr}")
        print("#--- You need to implement handle_observe_result function! ---#")

    @override
    def handle_save_surv_result(self, ssr: SAVE_SURV_RESULT) -> None:
        self._agent.log(f"SAVE_SURV_RESULT: {ssr}")
        self._agent.log(f"{ssr}")
        print("#--- You need to implement handle_save_surv_result function! ---#")

    @override
    def handle_predict_result(self, prd: PREDICT_RESULT) -> None:
        self._agent.log(f"PREDICT_RESULT: {prd}")
        self._agent.log(f"{prd}")

    @override
    def think(self) -> None:
        self._agent.log("Thinking")

        # Send a message to other agents in my group.
        # Empty AgentIDList will send to group members.
        self._agent.send(
            SEND_MESSAGE(
                AgentIDList(), f"Hello from agent {self._agent.get_agent_id().id}"
            )
        )

        # Retrieve the current state of the world.
        world = self.get_world()
        if world is None:
            self.send_and_end_turn(MOVE(Direction.CENTER))
            return

        # Fetch the cell at the agent’s current location. If the location is outside the world’s bounds,
        # return a default move action and end the turn.
        cell = world.get_cell_at(self._agent.get_location())
        if cell is None:
            self.send_and_end_turn(MOVE(Direction.CENTER))
            return

        # Get the top layer at the agent’s current location.
        top_layer = cell.get_top_layer()

        # If a survivor is present, save it and end the turn.
        if isinstance(top_layer, Survivor):
            self.send_and_end_turn(SAVE_SURV())
            return

        # If rubble is present, clear it and end the turn.
        if isinstance(top_layer, Rubble):
            self.send_and_end_turn(TEAM_DIG())
            return

        # Default action: Move the agent north if no other specific conditions are met.
        self.send_and_end_turn(MOVE(Direction.NORTH))

    def send_and_end_turn(self, command: AgentCommand):
        """Send a command and end your turn."""
        self._agent.log(f"SENDING {command}")
        self._agent.send(command)
        self._agent.send(END_TURN())
