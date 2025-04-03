import unittest
from unittest.mock import MagicMock
from src.agents.example_agent_a3.agent_helpers.communication_manager import CommunicationManager

'''
To run pytests, cd into root aegis folder
cd "c:\your\path\aegis-v3.0.1-a3-tauri\aegis"
Then run the following command:
pytest tests/test_communication_manager.py
This will run all the tests in the file.
'''

class TestCommunicationManager(unittest.TestCase):
    def setUp(self):
        # Create a mock memory object
        mock_memory = MagicMock()
        
        # Initialize the CommunicationManager with the mock memory
        self.comms = CommunicationManager(memory=mock_memory)

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


if __name__ == "__main__":
    unittest.main()