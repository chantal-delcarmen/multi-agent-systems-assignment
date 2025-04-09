import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the `src` directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, "../src"))
if src_dir not in sys.path:
    sys.path.append(src_dir)
    
from aegis import (
    END_TURN,
    SAVE_SURV,
    SEND_MESSAGE_RESULT,
    OBSERVE_RESULT,
    TEAM_DIG,
    MOVE,
    Rubble,
    Survivor,
    Direction,
)
from aegis.common.world.info import CellInfo
from aegis.api.location import create_location
from src.agents.example_agent_a3.example_agent import ExampleAgent


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
        patcher.start()

        # Initialize the ExampleAgent
        self.agent = ExampleAgent()
        self.agent.memory = self.mock_memory
        self.agent.comms = self.mock_comms
        self.agent.team_task_manager = self.mock_team_task_manager
        self.agent.leader_coordinator = self.mock_leader_coordinator

    def test_handle_observe_result_with_rubble(self):
        # Mock a rubble cell
        mock_cell_info = MagicMock(spec=CellInfo)
        mock_cell_info.top_layer = Rubble(remove_agents=3)
        mock_cell_info.location = create_location(3, 4)

        # Mock OBSERVE_RESULT
        observe_result = OBSERVE_RESULT(energy_level=100, cell_info=mock_cell_info, life_signals=MagicMock())
        observe_result.life_signals.size.return_value = 0

        # Call handle_observe_result
        self.agent.handle_observe_result(observe_result)

        # Verify that the task was added to the TeamTaskManager
        self.mock_team_task_manager.add_task.assert_called_once_with((3, 4), 3)
        self.mock_agent.log.assert_any_call("Added rubble task at (3, 4) requiring 3 agents.")

    def test_handle_observe_result_with_life_signals(self):
        # Mock a cell with life signals
        mock_cell_info = MagicMock(spec=CellInfo)
        mock_cell_info.top_layer = None
        mock_cell_info.location = create_location(5, 6)

        # Mock OBSERVE_RESULT
        observe_result = OBSERVE_RESULT(energy_level=100, cell_info=mock_cell_info, life_signals=MagicMock())
        observe_result.life_signals.size.return_value = 2
        observe_result.life_signals.get.side_effect = [10, 20]

        # Call handle_observe_result
        self.agent.handle_observe_result(observe_result)

        # Verify that life signals were logged
        self.mock_agent.log.assert_any_call("Detected 2 life signals at ( X 5 , Y 6 ).")
        self.mock_agent.log.assert_any_call("Survivor detected with energy level 10 at ( X 5 , Y 6 ).")
        self.mock_agent.log.assert_any_call("Survivor detected with energy level 20 at ( X 5 , Y 6 ).")

    def test_think_with_no_world(self):
        # Mock get_world to return None
        self.agent.get_world = MagicMock(return_value=None)

        # Call think
        self.agent.think()

        # Debugging: Print the actual calls to self.mock_agent.send
        print("Actual calls to send:", self.mock_agent.send.call_args_list)

        # Verify that the agent logged the correct message
        self.mock_agent.log.assert_any_call("World is None. Moving to CENTER.")

        # Verify that the MOVE command was sent with Direction.CENTER
        move_call = self.mock_agent.send.call_args_list[0][0][0]
        assert isinstance(move_call, MOVE)
        assert move_call.direction == Direction.CENTER

        # Verify that the END_TURN command was sent
        end_turn_call = self.mock_agent.send.call_args_list[1][0][0]
        assert isinstance(end_turn_call, END_TURN)

    def test_think_with_rubble(self):
        # Mock the world and cell with rubble
        mock_world = MagicMock()
        mock_cell = MagicMock()
        mock_cell.get_top_layer.return_value = Rubble(remove_agents=4)  # Simulate rubble requiring 4 agents
        mock_cell.location = create_location(7, 8)
        self.mock_agent.get_location.return_value = create_location(7, 8)
        mock_world.get_cell_at.return_value = mock_cell
        self.agent.get_world = MagicMock(return_value=mock_world)

        # Mock TeamTaskManager to simulate task coordination
        self.mock_team_task_manager.coordinate_team_dig.return_value = True

        # Call think
        self.agent.think()

        # Debugging: Print the actual calls to self.mock_agent.send
        print("Actual calls to send:", self.mock_agent.send.call_args_list)

        # Verify that the agent attempted to coordinate a TEAM_DIG task
        self.mock_team_task_manager.coordinate_team_dig.assert_called_once_with(self.mock_agent.get_id(), (7, 8))
        self.mock_agent.log.assert_any_call("Rubble detected at (7, 8). Coordinating TEAM_DIG.")

        # Verify that the TEAM_DIG command was sent
        team_dig_call = self.mock_agent.send.call_args_list[0][0][0]
        assert isinstance(team_dig_call, TEAM_DIG)

        # Verify that the END_TURN command was sent
        end_turn_call = self.mock_agent.send.call_args_list[1][0][0]
        assert isinstance(end_turn_call, END_TURN)

    def test_think_with_survivor(self):
        # Mock the world and cell with a survivor
        mock_world = MagicMock()
        mock_cell = MagicMock()
        mock_cell.get_top_layer.return_value = Survivor()  # Simulate a survivor
        mock_cell.location = create_location(9, 10)
        self.mock_agent.get_location.return_value = create_location(9, 10)
        mock_world.get_cell_at.return_value = mock_cell
        self.agent.get_world = MagicMock(return_value=mock_world)

        # Call think
        self.agent.think()

        # Debugging: Print the actual calls to self.mock_agent.send
        print("Actual calls to send:", self.mock_agent.send.call_args_list)

        # Verify that the agent logged the correct message
        self.mock_agent.log.assert_any_call("Survivor detected. Sending SAVE_SURV command.")

        # Verify that the SAVE_SURV command was sent
        save_surv_call = self.mock_agent.send.call_args_list[0][0][0]
        assert isinstance(save_surv_call, SAVE_SURV)

        # Verify that the END_TURN command was sent
        end_turn_call = self.mock_agent.send.call_args_list[1][0][0]
        assert isinstance(end_turn_call, END_TURN)


if __name__ == "__main__":
    unittest.main()