"""
Class AgentMemory: Stores per-agent state like location, energy level,
assigned task, known survivor locations, and received messages.

Authors: 
Chantal del Carmen, Zainab Majid, Mohammad Akif Hasan, Vincent Iyegbuye

Course: CPSC 383 - Winter 2025 | T05
Assignment 3 - Multi-Agent Systems
Mar 30, 2025

"""

class AgentMemory:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.location = None
        self.energy = 100
        self.task = None
        self.known_survivors = set()
        self.messages_received = []
        self.turn_counter = 0

    def set_turn_counter(self, turn_counter):
        self.turn_counter = turn_counter
    
    def get_turn_counter(self):
        return self.turn_counter

    def update_location(self, x, y):
        pass

    def receive_message(self, message):
        self.messages_received.append(message)
        #pass


    def get_messages(self):
        """ Retrieve all received messages. """
        return self.messages_received
