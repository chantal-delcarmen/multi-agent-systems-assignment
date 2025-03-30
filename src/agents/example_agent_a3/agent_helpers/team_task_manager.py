
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