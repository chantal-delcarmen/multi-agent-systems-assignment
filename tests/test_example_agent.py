# import pytest
# from unittest.mock import MagicMock
# import sys
# import os
# # from src.agents.example_agent_a3.agent_helpers.team_task_manager import TeamTaskManager
# from src.agents.example_agent_a3.example_agent import ExampleAgent
# from src.agents.example_agent_a3.agent_helpers.agent_memory import AgentMemory

# def test_agent_memory_initialization():
#     # Mock the AgentController and its get_agent_id method
#     mock_agent_controller = MagicMock()
#     mock_agent_id = MagicMock()
#     mock_agent_id.id = "test_agent_id"  # Mock the ID of the agent
#     mock_agent_controller.get_agent_id.return_value = mock_agent_id

#     # Mock the BaseAgent.get_agent() to return the mocked agent controller
#     with pytest.MonkeyPatch.context() as monkeypatch:
#         monkeypatch.setattr("example_agent_a3.example_agent.BaseAgent.get_agent", lambda: mock_agent_controller)

#         # Initialize the ExampleAgent
#         agent = ExampleAgent()

#         # Assert that AgentMemory was initialized with the correct agent ID
#         assert isinstance(agent.memory, AgentMemory)
#         assert agent.memory.agent_id == "test_agent_id"

#         # Verify that get_agent_id was called
#         mock_agent_controller.get_agent_id.assert_called_once()