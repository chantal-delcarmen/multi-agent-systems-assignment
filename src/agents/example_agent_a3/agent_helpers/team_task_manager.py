"""
Class team_task_manager.py

Description:
This module manages the execution and coordination of multi-agent tasks that require teamwork, 
such as TEAM_DIG actions where multiple agents must dig simultaneously at the same location.

Responsibilities:
- Track and manage team dig tasks, including their status and assigned agents.
- Assign agents to team dig tasks and ensure enough agents are present to initiate TEAM_DIG.
- Coordinate the timing of synchronized actions for TEAM_DIG operations.
- Notify agents to meet at specific locations for collaborative tasks.
- Remove completed tasks from the task list and reset the current task.
- Communicate task completion to the LeaderCoordinator for high-level replanning.

Communicates with:
- agent_helpers/communication_manager.py (for sending notifications to agents).
- agent_helpers/agent_memory.py (for storing agent state and task-related information).
- example_agent.py (for coordinating actions based on parsed messages).
- leader_coordinator.py (for notifying task completion and enabling high-level task replanning).

This module is used by example_agent.py to support cooperative behavior in the AEGIS simulation.

Authors: 
Chantal del Carmen, Zainab Majid, Mohammad Akif Hasan, Vincent Iyegbuye

Course: CPSC 383 - Winter 2025 | T05
Assignment 3 - Multi-Agent Systems
Mar 30, 2025

"""

from .communication_manager import CommunicationManager

class TeamTaskManager:
    def __init__(self, leader_coordinator, comms):
        """
        Initialize the TeamTaskManager.

        Args:
            leader_coordinator: The LeaderCoordinator instance for high-level coordination.
            comms: The CommunicationManager instance for sending and receiving messages.
        """
        self.team_dig_tasks = {}  # Task Format: {location: {assigned_agents, required_agents, completed, dig_count}}
        self.current_task = None
        self.leader_coordinator = leader_coordinator
        self.comms: CommunicationManager = comms  # CommunicationManager instance

    def notify_task_completed(self, location):
        """
        Notify the LeaderCoordinator and agents that a task has been completed.
        """
        if location in self.team_dig_tasks:
            # Notify the LeaderCoordinator
            self.leader_coordinator.notify_task_completed(location)

            # Notify agents via the messaging system
            message = f"TASK_COMPLETED {location[0]} {location[1]}"
            self.comms.send_message_to_all(message)
            self.leader_coordinator.agent.log(f"Task at {location} marked as completed and agents notified.")

    def add_task(self, location, required_agents):
        """
        Add a new team dig task to the manager and notify agents.

        Args:
            location: The location of the task.
            required_agents: The number of agents required for the task.
        """
        if location not in self.team_dig_tasks:
            self.team_dig_tasks[location] = {
                "assigned_agents": set(),
                "required_agents": required_agents,
                "completed": False,
                "dig_count": 0,
            }
            # Log the addition of the new task
            self.leader_coordinator.agent.log(
                f"Added new task at location {location} requiring {required_agents} agents."
            )
            # Notify agents about the new task
            self.notify_agents_about_task(location, required_agents)
        else:
            # Log if the task already exists
            self.leader_coordinator.agent.log(
                f"Task at location {location} already exists. Skipping addition."
            )

    def notify_agents_about_task(self, location, required_agents):
        """
        Notify agents about a new task.

        Args:
            location: The location of the task.
            required_agents: The number of agents required for the task.
        """
        message = f"TASK {location[0]} {location[1]} {required_agents}"
        self.comms.send_message_to_all(message)
        self.leader_coordinator.agent.log(f"Notified agents about task at {location} requiring {required_agents} agents.")

    def call_agents_to_meet(self, location):
        """
        Notify agents to meet at a specific location for a task.

        Args:
            location: The location where agents should meet.
        """
        message = f"MEET {location[0]} {location[1]}"
        self.comms.send_message_to_all(message)
        self.leader_coordinator.agent.log(f"Called agents to meet at {location}.")

    def handle_task_message(self, message):
        """
        Handle a message related to tasks.

        Args:
            message: The parsed message to handle.
        """
        if message["type"] == "TASK_COMPLETED":
            location = message["location"]
            self.mark_task_completed(location)
        elif message["type"] == "MEET":
            location = message["location"]
            self.leader_coordinator.agent.log(f"Received MEET message for location {location}.")

    def mark_task_completed(self, location):
        """
        Mark a task as completed and notify the LeaderCoordinator.

        Args:
            location: The location of the completed task.
        """
        if location in self.team_dig_tasks:
            self.team_dig_tasks[location]["completed"] = True
            self.notify_task_completed(location)

    def is_enough_agents(self, location):
        """
        Check if enough agents are available for TEAM_DIG at the location.
        """
        if location in self.team_dig_tasks:
            task = self.team_dig_tasks[location]
            return len(task["assigned_agents"]) >= task["required_agents"]
        return False

    def coordinate_team_dig(self, agent_id, location):
        """
        Coordinate agents to dig at the same time at the specified location.
        """
        if location in self.team_dig_tasks:
            task = self.team_dig_tasks[location]

            # If task already completed, skip it
            if task["completed"]:
                return False

            if agent_id not in task["assigned_agents"]:
                task["assigned_agents"].add(agent_id)  # Add agent to the assigned agents set
                self.call_agents_to_meet(location)  # Notify agents to meet at the location
                task["dig_count"] += 1  # Increment the dig count

            # Check if enough agents have arrived to initiate TEAM_DIG
            if self.is_enough_agents(location):
                self.current_task = location  # Set the current task to the location
                task["completed"] = True  # Mark task as completed
                self.notify_task_completed(location)  # Notify completion
                return True  # Indicate that the team dig can proceed

        return False  # Not enough agents yet