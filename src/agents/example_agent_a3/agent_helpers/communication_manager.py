"""
CommunicationManager: Responsible for formatting and parsing inter-agent
messages for coordination and task updates.
"""

class CommunicationManager:
    def __init__(self, memory):
        self.memory = memory

    def generate_found_message(self, location):
        pass

    def generate_done_message(self, location):
        pass

    def generate_assignment_message(self, agent_id, location):
        pass

    def parse_messages(self):
        pass
