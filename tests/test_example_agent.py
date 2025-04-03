import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the `src` directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, "../src"))
if src_dir not in sys.path:
    sys.path.append(src_dir)

from src.agents.example_agent_a3.example_agent import ExampleAgent
from aegis import (
    END_TURN,
    SAVE_SURV,
    OBSERVE_RESULT,
    SEND_MESSAGE_RESULT,
    SAVE_SURV_RESULT,
    TEAM_DIG,
    MOVE,
    Rubble,
    Survivor,
    Direction,
)
from aegis.common.world.info import CellInfo
from aegis.api.location import create_location


class TestExampleAgent(unittest.TestCase):
    def setUp(self):
        # Mock the agent controller and dependencies
        self.mock_agent = MagicMock()
        self.mock_memory = MagicMock()
        self.mock_comms = MagicMock()
        self.mock_team_task_manager = MagicMock()
        self.mock_leader_coordinator = MagicMock()

        # Patch BaseAgent.get_agent to return the mock agent
        patcher = patch("src.agents.example_agent_a3.example_agent.BaseAgent.get_agent", return_value=self.mock_agent)
        self.addCleanup(patcher.stop)
        self.mock_get_agent = patcher.start()

        # Initialize the ExampleAgent
        self.agent = ExampleAgent()
        self.agent.memory = self.mock_memory
        self.agent.comms = self.mock_comms
        self.agent.team_task_manager = self.mock_team_task_manager
        self.agent.leader = self.mock_leader_coordinator

    def test_handle_observe_result_with_rubble(self):
        # Mock a rubble cell
        mock_cell_info = MagicMock(spec=CellInfo)
        mock_cell_info.top_layer = Rubble()  # Set top_layer directly
        mock_cell_info.location = create_location(3, 4)

        # Mock OBSERVE_RESULT
        observe_result = OBSERVE_RESULT(energy_level=100, cell_info=mock_cell_info, life_signals=MagicMock())
        observe_result.life_signals.size.return_value = 0  # No life signals

        # Call handle_observe_result
        self.agent.handle_observe_result(observe_result)

        # Verify that the task was added to the TeamTaskManager
        self.mock_team_task_manager.add_task.assert_called_once_with((3, 4), 2)
        self.mock_agent.log.assert_any_call("Added rubble task at (3, 4) requiring 2 agents.")

    def test_handle_observe_result_with_life_signals(self):
        # Mock a cell with life signals
        mock_cell_info = MagicMock(spec=CellInfo)
        mock_cell_info.top_layer = None  # No top layer
        mock_cell_info.location = create_location(5, 6)

        # Mock OBSERVE_RESULT
        observe_result = OBSERVE_RESULT(energy_level=100, cell_info=mock_cell_info, life_signals=MagicMock())
        observe_result.life_signals.size.return_value = 1  # Life signals detected

        # Call handle_observe_result
        self.agent.handle_observe_result(observe_result)

        # Verify that life signals were logged
        self.mock_agent.log.assert_any_call("Detected life signals at ( X 5 , Y 6 ).")

    def test_handle_send_message_result(self):
        # Mock an AgentIDList with a size method
        mock_agent_id_list = MagicMock()
        mock_agent_id_list.size.return_value = 0  # No agents in the list

        # Mock SEND_MESSAGE_RESULT with a valid message
        smr = SEND_MESSAGE_RESULT(from_agent_id="Agent1", agent_id_list=mock_agent_id_list, msg="TASK_COMPLETED 3 4")

        # Mock parsed messages
        self.mock_comms.parse_messages.return_value = [{"type": "TASK_COMPLETED", "location": (3, 4)}]

        # Call handle_send_message_result
        self.agent.handle_send_message_result(smr)

        # Verify that the message was handled by the TeamTaskManager
        self.mock_team_task_manager.handle_task_message.assert_called_once_with({"type": "TASK_COMPLETED", "location": (3, 4)})

    def test_think_with_rubble(self):
        # Mock the world and cell with rubble
        mock_world = MagicMock()
        mock_cell = MagicMock()
        mock_cell.top_layer = Rubble()  # Set top_layer directly
        mock_cell.location = create_location(7, 8)
        self.mock_agent.get_location.return_value = create_location(7, 8)
        mock_world.get_cell_at.return_value = mock_cell
        self.agent.get_world = MagicMock(return_value=mock_world)

        # Mock TeamTaskManager to indicate not enough agents
        self.mock_team_task_manager.coordinate_team_dig.return_value = False

        # Call think
        self.agent.think()

        # Verify that the agent attempted to coordinate a TEAM_DIG task
        self.mock_team_task_manager.coordinate_team_dig.assert_called_once_with(self.mock_agent.get_id(), (7, 8))
        self.mock_agent.send.assert_any_call(MOVE(Direction.CENTER))
        self.mock_agent.send.assert_any_call(END_TURN())

    def test_think_with_enough_agents_for_team_dig(self):
        # Mock the world and cell with rubble
        mock_world = MagicMock()
        mock_cell = MagicMock()
        mock_cell.top_layer = Rubble()  # Set top_layer directly
        mock_cell.location = create_location(7, 8)
        self.mock_agent.get_location.return_value = create_location(7, 8)
        mock_world.get_cell_at.return_value = mock_cell
        self.agent.get_world = MagicMock(return_value=mock_world)

        # Mock TeamTaskManager to indicate successful coordination
        self.mock_team_task_manager.coordinate_team_dig.return_value = True

        # Call think
        self.agent.think()

        # Verify that the agent sent the TEAM_DIG command
        self.mock_agent.send.assert_any_call(TEAM_DIG())
        self.mock_agent.send.assert_any_call(END_TURN())

    def test_think_with_survivor(self):
        # Mock the world and cell with a survivor
        mock_world = MagicMock()
        mock_cell = MagicMock()
        mock_cell.top_layer = Survivor()  # Set top_layer directly
        mock_cell.location = create_location(9, 10)
        self.mock_agent.get_location.return_value = create_location(9, 10)
        mock_world.get_cell_at.return_value = mock_cell
        self.agent.get_world = MagicMock(return_value=mock_world)

        # Call think
        self.agent.think()

        # Verify that the agent sent the SAVE_SURV command
        self.mock_agent.send.assert_any_call(SAVE_SURV())
        self.mock_agent.send.assert_any_call(END_TURN())

    def test_think_with_no_world(self):
        # Mock get_world to return None
        self.agent.get_world = MagicMock(return_value=None)

        # Call think
        self.agent.think()

        # Verify that the agent stayed in place
        self.mock_agent.send.assert_any_call(MOVE(Direction.CENTER))
        self.mock_agent.send.assert_any_call(END_TURN())


if __name__ == "__main__":
    unittest.main()