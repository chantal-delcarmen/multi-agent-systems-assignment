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
        self.current_task = None                # Assigned task (if any)
        self.turn_counter = 0           # Number of turns since the agent was created
        self.known_survivors = set()    # Create empty set for known survivors
        self.completed_tasks = set()    # Create empty set for completed tasks
        self.messages_received = []     # List to store received messages
        self.assignments = {}           # Dictionary to store assignments (agent_id -> location)

    def set_turn_counter(self, turn_counter):
        """"
        Set the turn counter for the agent.
        :param turn_counter: The current turn number
        """
        self.turn_counter = turn_counter
    
    def get_turn_counter(self):
        """
        Get the current turn counter for the agent."
        :return: The current turn number
        """
        return self.turn_counter

    def update_location(self, x, y):
        """
        Update the agent's location."
        :param x: x-coordinate of the agent's new location
        :param y: y-coordinate of the agent's new location
        """
        self.location = (x, y)

    def get_location(self):
        """
        Get the agent's current location."
        :return: The agent's current location as a tuple (x, y)
        """
        return self.location

    def receive_message(self, message):
        """
        Store a received message in the agent's memory."
        :param message: The message to be stored
        """
        self.messages_received.append(message)

    def get_messages(self):
        """ Retrieve all received messages. """
        return self.messages_received
    
    # def get_agent_id(self):
    #     """
    #     Get the agent's ID."
    #     :return: The agent's ID
    #     """
    #     return self.agent_id

    def add_found_location(self, x, y):
        """
        Add a found survivor location to the agent's memory.
        :param x: x-coordinate of the survivor's location
        :param y: y-coordinate of the survivor's location
        """
        self.known_survivors.add((x, y))

    def get_found_locations(self):
        """
        Get all known survivor locations.
        :return: A set of survivor locations as (x, y) tuples
        """
        return self.known_survivors

    def add_done_location(self, x, y):
        """
        Add a completed task location to the agent's memory.
        :param x: x-coordinate of the completed task's location
        :param y: y-coordinate of the completed task's location
        """
        self.completed_tasks.add((x, y))

    def get_done_locations(self):
        """
        Get all completed task locations.
        :return: A set of completed task locations as (x, y) tuples
        """
        return self.completed_tasks

    def set_current_task(self, x, y):
        """
        Set the current task for the agent and add it to assignments.
        :param x: x-coordinate of the task's location
        :param y: y-coordinate of the task's location
        """
        self.current_task = (x, y)
        self.add_assignment(self.agent_id, x, y)

    def get_current_task(self):
        """
        Get the current task assigned to the agent.
        :return: The current task as a tuple (x, y), or None if no task is assigned.
        """
        return self.current_task

    def clear_current_task(self):
        """
        Clear the current task assigned to the agent.
        """
        self.current_task = None

    def add_assignment(self, agent_id, x, y):
        """
        Add an assignment to the agent's memory.
        :param agent_id: The ID of the agent assigned to the task
        :param x: x-coordinate of the task's location
        :param y: y-coordinate of the task's location
        """
        self.assignments[agent_id] = (x, y)

    def get_assignments(self):
        """
        Get all assignments stored in the agent's memory.
        :return: A dictionary of assignments (agent_id -> location)
        """
        return self.assignments