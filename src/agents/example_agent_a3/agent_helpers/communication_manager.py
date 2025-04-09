"""
Class CommunicationManager: Responsible for formatting and parsing inter-agent
messages for coordination and task updates.

Authors: 
Chantal del Carmen, Zainab Majid, Mohammad Akif Hasan, Vincent Iyegbuye

Course: CPSC 383 - Winter 2025 | T05
Assignment 3 - Multi-Agent Systems
Mar 30, 2025

"""

import sys
import os
import re

# Add the `src` directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, "../../../"))
if src_dir not in sys.path:
    sys.path.append(src_dir)

from aegis.common.commands.agent_commands.SEND_MESSAGE import SEND_MESSAGE
from aegis.common.agent_id_list import AgentIDList

class CommunicationManager:
    def __init__(self, memory, agent):
        self.memory = memory
        self.agent = agent

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
        Parse incoming messages and update memory or task manager.
        :param messages: A list of incoming message strings
        :return: A list of parsed message dictionaries
        """
        if not messages or not isinstance(messages, list):
            print("Error: Invalid or empty messages list.")
            return []

        parsed_messages = []
        for i in messages:
            if not isinstance(i, str):
                print(f"Error: Invalid message format (not a string): {i}")
                continue

            # Check if the message matches the expected formats
            found_match = re.match(r"FOUND (\d+) (\d+)", i)
            done_match = re.match(r"DONE (\d+) (\d+)", i)
            assign_match = re.match(r"ASSIGN (\d+) (\d+) (\d+)", i)

            if found_match:
                # Parse "FOUND" message
                x, y = map(int, found_match.groups())
                parsed_messages.append({"type": "FOUND", "location": (x, y)})
            elif done_match:
                # Parse "DONE" message
                x, y = map(int, done_match.groups())
                parsed_messages.append({"type": "DONE", "location": (x, y)})
            elif assign_match:
                # Parse "ASSIGN" message
                agent_id, x, y = map(int, assign_match.groups())
                parsed_messages.append({"type": "ASSIGN", "agent_id": agent_id, "location": (x, y)})
            else:
                # Handle unknown message format
                print(f"Warning: Unknown message format: {i}")

        return parsed_messages

    def handle_parsed_message(self, message, agent):
        """
        Handle a parsed message based on its type.
        :param message: The parsed message dictionary.
        :param agent: The agent instance for logging or additional actions.
        """
        message_type = message.get("type")
        if message_type == "FOUND":
            # Handle a "FOUND" message
            x, y = message["location"]
            agent.log(f"FOUND message received: Location ({x}, {y})")
            self.memory.add_found_location(x, y)
        elif message_type == "DONE":
            # Handle a "DONE" message
            x, y = message["location"]
            agent.log(f"DONE message received: Location ({x}, {y})")
            self.memory.add_done_location(x, y)
        elif message_type == "ASSIGN":
            # Handle an "ASSIGN" message
            agent_id = message["agent_id"]
            x, y = message["location"]
            agent.log(f"ASSIGN message received: Agent {agent_id} assigned to ({x}, {y})")
            self.memory.set_current_task(agent_id, x, y)
        else:
            # Handle unknown message types
            agent.log(f"Unknown message type: {message_type}")

    def send_message_to_all(self, message):
        """
        Send a message to all agents.
        :param message: The message to send.
        """
        recipient_list = AgentIDList()  # Empty list means broadcast to all
        self.agent.send(SEND_MESSAGE(recipient_list, message))
        self.agent.log(f"Message sent to all agents: {message}")
