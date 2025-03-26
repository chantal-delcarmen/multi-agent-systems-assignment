"""
AgentMemory: Stores per-agent state like location, energy level,
assigned task, known survivor locations, and received messages.
"""

class AgentMemory:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.location = None
        self.energy = 100
        self.task = None
        self.known_survivors = set()
        self.messages_received = []

    def update_location(self, x, y):
        pass

    def receive_message(self, message):
        pass
