from abc import ABC, abstractmethod

from aegis.common.commands.aegis_command import AegisCommand
from aegis.common.commands.aegis_commands import (
    AEGIS_UNKNOWN,
    CMD_RESULT_END,
    CMD_RESULT_START,
    CONNECT_OK,
    DEATH_CARD,
    DISCONNECT,
    MESSAGES_END,
    MESSAGES_START,
    MOVE_RESULT,
    OBSERVE_RESULT,
    PREDICT_RESULT,
    ROUND_END,
    ROUND_START,
    SAVE_SURV_RESULT,
    SEND_MESSAGE_RESULT,
    SLEEP_RESULT,
    TEAM_DIG_RESULT,
)
from a3.aegis_parser import AegisParser
from aegis.common.world.info.cell_info import CellInfo
from aegis.common.world.world import InternalWorld
from aegis.api import World

import a3.agent.base_agent
from a3.agent.agent_states import AgentStates


class Brain(ABC):
    """Represents the brain of an agent."""

    def __init__(self) -> None:
        """Initializes the Brain instance with no world information."""
        self._world: World | None = None

    def get_world(self) -> World | None:
        """Returns the current world information associated with the brain."""
        return self._world

    @abstractmethod
    def handle_send_message_result(self, smr: SEND_MESSAGE_RESULT) -> None:
        """
        Handles the SEND_MESSAGE_RESULT command.

        Args:
            smr: The SEND_MESSAGE_RESULT command to handle.
        """
        pass

    @abstractmethod
    def handle_save_surv_result(self, ssr: SAVE_SURV_RESULT) -> None:
        """
        Handles the SAVE_SURV_RESULT command.

        Args:
            ssr: The SAVE_SURV_RESULT command to handle.
        """
        pass

    @abstractmethod
    def handle_predict_result(self, prd: PREDICT_RESULT) -> None:
        pass

    @abstractmethod
    def handle_observe_result(self, ovr: OBSERVE_RESULT) -> None:
        """
        Handles the OBSERVE_RESULT command.

        Args:
            ovr: The OBSERVE_RESULT command to handle.
        """
        pass

    @abstractmethod
    def think(self) -> None:
        """
        Contains the logic for the brain to make decisions based
        on the current state of the world.
        """
        pass

    def handle_aegis_command(self, aegis_command: AegisCommand) -> None:
        """
        Processes a command received from AEGIS.

        Args:
            aegis_command: The command received from AEGIS.
        """
        base_agent = a3.agent.base_agent.BaseAgent.get_agent()
        if isinstance(aegis_command, CONNECT_OK):
            connect_ok: CONNECT_OK = aegis_command
            base_agent.set_agent_id(connect_ok.new_agent_id)
            base_agent.set_energy_level(connect_ok.energy_level)
            base_agent.set_location(connect_ok.location)
            self._world = InternalWorld(
                AegisParser.build_world(connect_ok.world_filename)
            )  # pyright: ignore[reportAttributeAccessIssue]
            base_agent.set_agent_state(AgentStates.CONNECTED)
            base_agent.log("Connected Successfully")

        elif isinstance(aegis_command, DEATH_CARD):
            base_agent.set_agent_state(AgentStates.SHUTTING_DOWN)

        elif isinstance(aegis_command, DISCONNECT):
            base_agent.set_agent_state(AgentStates.SHUTTING_DOWN)

        elif isinstance(aegis_command, SEND_MESSAGE_RESULT):
            self.handle_send_message_result(aegis_command)

        elif isinstance(aegis_command, MESSAGES_END):
            base_agent.set_agent_state(AgentStates.IDLE)

        elif isinstance(aegis_command, MESSAGES_START):
            base_agent.set_agent_state(AgentStates.READ_MAIL)

        elif isinstance(aegis_command, MOVE_RESULT):
            move_result: MOVE_RESULT = aegis_command
            move_result_current_info: CellInfo = (
                move_result.surround_info.get_current_info()
            )
            base_agent.set_energy_level(move_result.energy_level)
            base_agent.set_location(move_result_current_info.location)
            base_agent.update_surround(move_result.surround_info, self.get_world())  # pyright: ignore[reportArgumentType]

        elif isinstance(aegis_command, ROUND_END):
            base_agent.set_agent_state(AgentStates.IDLE)

        elif isinstance(aegis_command, ROUND_START):
            base_agent.set_agent_state(AgentStates.THINK)

        elif isinstance(aegis_command, SAVE_SURV_RESULT):
            save_surv_result: SAVE_SURV_RESULT = aegis_command
            save_surv_result_current_info = (
                save_surv_result.surround_info.get_current_info()
            )
            base_agent.set_energy_level(save_surv_result.energy_level)
            base_agent.set_location(save_surv_result_current_info.location)
            if save_surv_result.has_pred_info():
                surv_id, image, labels = (
                    save_surv_result.surv_saved_id,
                    save_surv_result.image_to_predict,
                    save_surv_result.all_unique_labels,
                )
                base_agent.add_prediction_info((surv_id, image, labels))

            self.handle_save_surv_result(save_surv_result)
            base_agent.update_surround(save_surv_result.surround_info, self.get_world())  # pyright: ignore[reportArgumentType]

        elif isinstance(aegis_command, PREDICT_RESULT):
            pred_req: PREDICT_RESULT = aegis_command
            self.handle_predict_result(pred_req)

        elif isinstance(aegis_command, SLEEP_RESULT):
            sleep_result: SLEEP_RESULT = aegis_command
            if sleep_result.was_successful:
                base_agent.set_energy_level(sleep_result.charge_energy)
        elif isinstance(aegis_command, OBSERVE_RESULT):
            ovr: OBSERVE_RESULT = aegis_command
            self.handle_observe_result(ovr)

        elif isinstance(aegis_command, TEAM_DIG_RESULT):
            team_dig_result: TEAM_DIG_RESULT = aegis_command
            team_dig_result_current_info: CellInfo = (
                team_dig_result.surround_info.get_current_info()
            )
            base_agent.set_energy_level(team_dig_result.energy_level)
            base_agent.set_location(team_dig_result_current_info.location)
            base_agent.update_surround(team_dig_result.surround_info, self.get_world())  # pyright: ignore[reportArgumentType]

        elif isinstance(aegis_command, AEGIS_UNKNOWN):
            base_agent.log("Brain: Got Unknown command reply from AEGIS.")

        elif isinstance(aegis_command, CMD_RESULT_START):
            base_agent.set_agent_state(AgentStates.GET_CMD_RESULT)

        elif isinstance(aegis_command, CMD_RESULT_END):
            base_agent.set_agent_state(AgentStates.IDLE)

        else:
            base_agent.log(
                f"Brain: Got unrecognized reply from AEGIS: {aegis_command.__class__.__name__}.",
            )
