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
    def __init__(self, agent):
        self.agent = agent
        self.assigned_task = None
        self.location = None
        self.energy = 100
        self.current_task = None        # Assigned task (if any)
        self.turn_counter = 0           # Number of turns since the agent was created
        self.known_survivors = set()    # Create empty set for known survivors
        self.completed_tasks = set()    # Create empty set for completed tasks
        self.messages_received = []     # List to store received messages
        self.assignments = {}           # Dictionary to store assignments (agent_id -> location)
        self.agent_locations = {}       # Maps agent IDs to their locations

    def set_turn_counter(self, turn_counter):
        """Set the turn counter for the agent."""
        self.turn_counter = turn_counter
    
    def get_turn_counter(self):
        """Get the current turn counter for the agent."""
        return self.turn_counter

    def update_location(self, x, y):
        """Update the agent's location."""
        self.location = (x, y)

    def get_location(self):
        """Get the agent's current location."""
        return self.location

    def receive_message(self, message):
        """Store a received message in the agent's memory."""
        self.messages_received.append(message)

    def get_messages(self):
        """Retrieve all received messages."""
        return self.messages_received

    def add_found_location(self, x, y):
        """Add a found survivor location to the agent's memory."""
        self.known_survivors.add((x, y))

    def get_found_locations(self):
        """Get all known survivor locations."""
        return self.known_survivors

    def add_done_location(self, x, y):
        """Add a completed task location to the agent's memory."""
        self.completed_tasks.add((x, y))

    def get_done_locations(self):
        """Get all completed task locations."""
        return self.completed_tasks

    def set_current_task(self, agent_id, x, y):
        """Set the current task for the agent and add it to assignments."""
        self.agent_id = agent_id
        self.current_task = (x, y)
        self.add_assignment(self.agent_id, x, y)

    def get_current_task(self):
        """Get the current task assigned to the agent."""
        return self.current_task

    def clear_current_task(self):
        """Clear the current task assigned to the agent."""
        self.current_task = None

    def add_assignment(self, agent_id, x, y):
        """Add an assignment to the agent's memory."""
        self.assignments[agent_id] = (x, y)

    def get_assignments(self):
        """Get all assignments stored in the agent's memory."""
        return self.assignments
    
    def mark_cell_as_observed(self, current_location):
        """Mark the cell as observed by adding it to the known survivors set."""
        self.known_survivors.add(current_location)
        
    def is_cell_observed(self, current_location):
        """Check if the cell has been observed by the agent."""
        return current_location in self.known_survivors

    def get_assigned_task(self):
        """Retrieve the currently assigned task."""
        return self.assigned_task

    def set_assigned_task(self, task):
        """Set a new assigned task."""
        self.assigned_task = task

    def update_agent_location(self, agent_id, location):
        """Update the location of a specific agent."""
        self.agent_locations[agent_id] = location

    def get_agent_location(self, agent_id):
        """Get the location of a specific agent."""
        return self.agent_locations.get(agent_id, None)

    def get_all_agents(self):
        """
        Retrieve a list of all agent IDs currently tracked.
        :return: A list of agent IDs.
        """
        return list(self.agent_locations.keys())