"""
Class CommunicationManager: Responsible for formatting and parsing inter-agent
messages for coordination and task updates.

Authors: 
Chantal del Carmen, Zainab Majid, Mohammad Akif Hasan, Vincent Iyegbuye

Course: CPSC 383 - Winter 2025 | T05
Assignment 3 - Multi-Agent Systems
Mar 30, 2025

"""

import re


class CommunicationManager:
    def __init__(self, memory):
        self.memory = memory

    def generate_found_message(self, location):
        """
        Generate message to inform other agents about discovered task or rubble
        :param location: (x, y) coordinates of the discovered task as a tuple
        :return: A formatted string message, eg. "FOUND (x, y)"
        """
        return f"FOUND {location[0]} {location[1]}"  # returning the x and y coordinates of the found agents

    def generate_done_message(self, location):
        """
        Generate message to notify other agents that a task is completed
        :param location: (x, y) coordinates of the completed task as a tuple
        :return: formatted string message, eg. "DONE (x, y)"
        """
        return f"DONE {location[0]} {location[1]}"

    def generate_assignment_message(self, agent_id, location):
        """
        Generate message to assign an agent to a task
        :param agent_id: ID of the agent being assigned
        :param location: (x, y) coordinates of the task as a tuple
        :return: A formatted string message, eg. "ASSIGN agent_id (x, y)"
        """
        return f"ASSIGN {agent_id} {location[0]} {location[1]}"

    def parse_messages(self, messages):
        """
        Parse incoming messages and update memory or task manager
        :param messages: A list of incoming message strings
        :return: A list of parsed message dictionaries
        """
        parsed_messages = []
        for i in messages:
            # Check if the message is in the expected format
            # x and y coordinates of the found agents
            found_match = re.match(r"FOUND (\d+) (\d+)", i)
            # x and y coordinates of the completed task
            done_match = re.match(r"DONE (\d+) (\d+)", i)
            # agent_id, x and y coordinates of the task
            assign_match = re.match(r"ASSIGN (\d+) (\d+) (\d+)", i)
            if found_match:
                # x and y coordinates of the found agents
                x, y = map(int, found_match.groups())
                parsed_messages.append({"type": "FOUND", "location": (x, y)})
            elif done_match:
                x, y = map(int, done_match.groups())
                parsed_messages.append({"type": "DONE", "location": (x, y)})
            elif assign_match:
                agent_id, x, y = map(int, assign_match.groups())
                parsed_messages.append(
                    {"type": "ASSIGN", "agent_id": agent_id, "location": (x, y)})
            else:
                print(f"Unknown message format: {i}")
                # Handle unknown message format
        self.agent_memory.messages_received.clear()

        # pass
