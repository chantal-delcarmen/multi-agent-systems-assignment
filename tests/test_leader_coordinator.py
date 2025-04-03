import unittest
from unittest.mock import MagicMock
from src.agents.example_agent_a3.agent_helpers.leader_coordinator import LeaderCoordinator

class TestLeaderCoordinator(unittest.TestCase):
    def test_is_leader_true(self):
        # Mock the agent and its get_agent_id() method
        mock_agent = MagicMock()
        mock_agent.get_agent_id.return_value = MagicMock(id=1)  # Agent ID is 1 (leader)

        # Initialize the LeaderCoordinator with the mock agent
        leader_coordinator = LeaderCoordinator(mock_agent)

        # Assert that is_leader is True
        self.assertTrue(leader_coordinator.is_leader)

    def test_is_leader_false(self):
        # Mock the agent and its get_agent_id() method
        mock_agent = MagicMock()
        mock_agent.get_agent_id.return_value = MagicMock(id=2)  # Agent ID is not 1

        # Initialize the LeaderCoordinator with the mock agent
        leader_coordinator = LeaderCoordinator(mock_agent)

        # Assert that is_leader is False
        self.assertFalse(leader_coordinator.is_leader)

if __name__ == "__main__":
    unittest.main()