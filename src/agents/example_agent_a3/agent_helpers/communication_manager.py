"""
Class CommunicationManager: Responsible for formatting and parsing inter-agent
messages for coordination and task updates.

Authors: 
Chantal del Carmen, Zainab Majid, Mohammad Akif Hasan, Vincent Iyegbuye

Course: CPSC 383 - Winter 2025 | T05
Assignment 3 - Multi-Agent Systems
Mar 30, 2025

"""

class CommunicationManager:
    def __init__(self, memory):
        self.memory = memory

    def generate_found_message(self, location):
        """
        Generate message to inform other agents about discovered task or rubble
        :param location: (x, y) coordinates of the discovered task as a tuple
        :return: A formatted string message, eg. "FOUND (x, y)"
        """
        return f"FOUND {location}"

    def generate_done_message(self, location):
        """
        Generate message to notify other agents that a task is completed
        :param location: (x, y) coordinates of the completed task as a tuple
        :return: formatted string message, eg. "DONE (x, y)"
        """
        return f"DONE {location}"

    def generate_assignment_message(self, agent_id, location):
        """
        Generate message to assign an agent to a task
        :param agent_id: ID of the agent being assigned
        :param location: (x, y) coordinates of the task as a tuple
        :return: A formatted string message, eg. "ASSIGN agent_id (x, y)"
        """
        return f"ASSIGN {agent_id} {location}"


    def parse_messages(self):
        """
        Parse incoming messages and update memory or task manager
        :param messages: A list of incoming message strings
        :return: A list of parsed message dictionaries
        """
        pass
