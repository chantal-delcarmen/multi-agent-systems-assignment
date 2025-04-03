import unittest
from unittest.mock import MagicMock
from src.agents.example_agent_a3.agent_helpers.communication_manager import CommunicationManager
from src.agents.example_agent_a3.agent_helpers.agent_memory import AgentMemory

class TestCommunicationManager(unittest.TestCase):
    def setUp(self):
        # Create a mock memory object
        self.mock_memory = MagicMock()
        self.mock_agent = MagicMock()  # Mock agent for logging and sending messages

        # Initialize the CommunicationManager with the mock memory and agent
        self.comms = CommunicationManager(memory=self.mock_memory)
        self.comms.agent = self.mock_agent  # Inject the mock agent

    def test_generate_found_message(self):
        # Test generating a "FOUND" message
        location = (3, 4)
        expected = "FOUND 3 4"
        result = self.comms.generate_found_message(location)
        self.assertEqual(result, expected)

    def test_generate_done_message(self):
        # Test generating a "DONE" message
        location = (5, 6)
        expected = "DONE 5 6"
        result = self.comms.generate_done_message(location)
        self.assertEqual(result, expected)

    def test_generate_assignment_message(self):
        # Test generating an "ASSIGN" message
        agent_id = 1
        location = (7, 8)
        expected = "ASSIGN 1 7 8"
        result = self.comms.generate_assignment_message(agent_id, location)
        self.assertEqual(result, expected)

    def test_parse_found_message(self):
        # Test parsing a "FOUND" message
        messages = ["FOUND 3 4"]
        expected = [{"type": "FOUND", "location": (3, 4)}]
        result = self.comms.parse_messages(messages)
        self.assertEqual(result, expected)

    def test_parse_done_message(self):
        # Test parsing a "DONE" message
        messages = ["DONE 5 6"]
        expected = [{"type": "DONE", "location": (5, 6)}]
        result = self.comms.parse_messages(messages)
        self.assertEqual(result, expected)

    def test_parse_assign_message(self):
        # Test parsing an "ASSIGN" message
        messages = ["ASSIGN 1 7 8"]
        expected = [{"type": "ASSIGN", "agent_id": 1, "location": (7, 8)}]
        result = self.comms.parse_messages(messages)
        self.assertEqual(result, expected)

    def test_parse_invalid_message(self):
        # Test parsing an invalid message
        messages = ["INVALID MESSAGE"]
        expected = []
        result = self.comms.parse_messages(messages)
        self.assertEqual(result, expected)

    def test_parse_mixed_messages(self):
        # Test parsing a mix of valid and invalid messages
        messages = [
            "FOUND 3 4",
            "DONE 5 6",
            "ASSIGN 1 7 8",
            "INVALID MESSAGE",
        ]
        expected = [
            {"type": "FOUND", "location": (3, 4)},
            {"type": "DONE", "location": (5, 6)},
            {"type": "ASSIGN", "agent_id": 1, "location": (7, 8)},
        ]
        result = self.comms.parse_messages(messages)
        self.assertEqual(result, expected)

    def test_handle_found_message(self):
        # Test handling a "FOUND" message
        message = {"type": "FOUND", "location": (3, 4)}
        self.comms.handle_parsed_message(message, self.mock_agent)

        # Verify that the memory and agent were updated correctly
        self.mock_memory.add_found_location.assert_called_once_with(3, 4)
        self.mock_agent.log.assert_called_once_with("FOUND message received: Location (3, 4)")

    def test_handle_done_message(self):
        # Test handling a "DONE" message
        message = {"type": "DONE", "location": (5, 6)}
        self.comms.handle_parsed_message(message, self.mock_agent)

        # Verify that the memory and agent were updated correctly
        self.mock_memory.add_done_location.assert_called_once_with(5, 6)
        self.mock_agent.log.assert_called_once_with("DONE message received: Location (5, 6)")

    def test_handle_assign_message(self):
        # Test handling an "ASSIGN" message
        message = {"type": "ASSIGN", "agent_id": 1, "location": (7, 8)}
        self.comms.handle_parsed_message(message, self.mock_agent)

        # Verify that the memory and agent were updated correctly
        self.mock_memory.set_current_task.assert_called_once_with(1, 7, 8)
        self.mock_agent.log.assert_called_once_with("ASSIGN message received: Agent 1 assigned to (7, 8)")

    def test_send_message_to_all(self):
        # Test sending a message to all agents
        message = "TEST_MESSAGE"
        self.comms.send_message_to_all(message)

        # Verify that the agent's send method was called with the correct arguments
        self.mock_agent.send.assert_called_once()
        args = self.mock_agent.send.call_args[0][0]
        self.assertEqual(args.message, message)
        self.mock_agent.log.assert_called_once_with(f"Message sent to all agents: {message}")

    def test_add_found_location(self):
        # Test that a FOUND message updates the memory correctly
        memory = AgentMemory(agent_id=1)
        self.comms.memory = memory  # Use the real memory object

        # Simulate handling a FOUND message
        message = {"type": "FOUND", "location": (3, 4)}
        self.comms.handle_parsed_message(message, MagicMock())

        # Verify that the location was added to known_survivors
        self.assertIn((3, 4), memory.get_found_locations())

    def test_add_done_location(self):
        # Test that a DONE message updates the memory correctly
        memory = AgentMemory(agent_id=1)
        self.comms.memory = memory  # Use the real memory object

        # Simulate handling a DONE message
        message = {"type": "DONE", "location": (5, 6)}
        self.comms.handle_parsed_message(message, MagicMock())

        # Verify that the location was added to completed_tasks
        self.assertIn((5, 6), memory.get_done_locations())

    def test_add_assignment(self):
        # Test that an ASSIGN message updates the memory correctly
        memory = AgentMemory(agent_id=1)
        self.comms.memory = memory  # Use the real memory object

        # Simulate handling an ASSIGN message
        message = {"type": "ASSIGN", "agent_id": 1, "location": (7, 8)}
        self.comms.handle_parsed_message(message, MagicMock())

        # Verify that the assignment was added to assignments
        self.assertEqual(memory.get_assignments()[1], (7, 8))


if __name__ == "__main__":
    unittest.main()