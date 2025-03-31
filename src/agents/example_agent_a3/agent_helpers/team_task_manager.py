
"""
Class team_task_manager.py

Description:
This module manages coordination for multi-agent tasks that require teamwork,
such as TEAM_DIG actions that need two agents to dig simultaneously at the same location.

Responsibilities:
- Track locations where team dig is required
- Assign agents to team dig tasks
- Determine when enough agents have arrived to initiate TEAM_DIG
- Coordinate the timing of synchronized actions
- Update and remove completed tasks
- Support replanning once a shared task is complete

Communicates with:
- agent_helpers/communication_manager.py (message formatting and parsing)
- agent_helpers/agent_memory.py (stores agent state and messages)
- example_agent.py (coordinating actions based on parsed messages)

This module is used by example_agent.py to support cooperative behavior in the AEGIS simulation.

Authors: 
Chantal del Carmen, Zainab Majid, Mohammad Akif Hasan, Vincent Iyegbuye

Course: CPSC 383 - Winter 2025 | T05
Assignment 3 - Multi-Agent Systems
Mar 30, 2025

"""

class TeamTaskManager:
    def __init__(self):
        # Initialize dictionary to store team dig tasks
        # Task Format: {location: {assigned_agents, required_agents, completed, planned_turn, dig_count}}
        self.team_dig_tasks = {}
        self.current_task = None

    def add_task(self, location, current_turn, estimated_travel_time):
        """
        Add a new team dig task to the manager.
        """

        buffer_time = 2  # Buffer time to account for travel delays

        # Check if the task already exists
        if location not in self.team_dig_tasks:
            self.team_dig_tasks[location] = {
                'assigned_agents': set(),       # Set of agents assigned to the task
                'required_agents': 2,           # Number of agents required for TEAM_DIG
                'completed': False,             # Flag to check if task is completed
                'planned_turn': (               # Turn when the task is planned to be executed
                    current_turn + estimated_travel_time + buffer_time
                ),
                'dig_count': 0                  # Counter for # of digs completed
            }
    
    # Check if TEAM_DIG is needed at the location
    def is_team_dig_needed(self, location):
        """
        Check if a team dig task is needed at the given location
        """
        # Check if the location is in the task list
        if location in self.team_dig_tasks:
            # Check if the task is not completed
            task = self.team_dig_tasks[location]
            return task['completed'] == False
        # If location is not in team_dig_tasks list, return False (TEAM_DIG not needed)
        return False
    
    def is_enough_agents(self, location):
        """
        Check if enough agents are available for TEAM_DIG at the location
        """
        if location in self.team_dig_tasks:
            task = self.team_dig_tasks[location]
            return len(task['assigned_agents']) >= task['required_agents']
        return False

    # Coordinate agents to dig at the same time at correct locations
    def coordinate_team_dig(self, agent_id, location):
        """
        Coordinate agents to dig at the same time at the specified location
        """
        if location in self.team_dig_tasks:
            task = self.team_dig_tasks[location]

            #If task already completed, skip it
            if task['completed']:
                return False
            
            if agent_id not in task['assigned_agents']:
                task['assigned_agents'].add(agent_id)  # Add agent to the assigned agents set
                task['dig_count'] += 1  # Increment the dig count

            # Check if enough agents have arrived to initiate TEAM_DIG
            if self.is_enough_agents(location):
                self.current_task = location # Set the current task to the location
                task['completed'] = True    # Mark task as completed
                return True                 # Indicate that the team dig can proceed

        return False  # Not enough agents yet


    
    # Implement task coordination logic (eg. “meet at (x, y)”)
    # Handle multi-agent decisions based on messages
    # Replan when a shared goal is completed