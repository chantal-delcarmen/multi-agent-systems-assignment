
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
        # Task Format: 
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