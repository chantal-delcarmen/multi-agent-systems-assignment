"""
Class LeaderCoordinator: Used by the leader to assign tasks, track survivor
assignments, coordinate task completion, and replan tasks when necessary.

Responsibilities:
- Assign agents to tasks or goals based on the current state of the environment.
- Track task assignments and ensure tasks are completed efficiently.
- Replan tasks when shared goals are completed or when tasks require reassignment.
- Track the status of survivors and coordinate their rescue.
- Communicate with TeamTaskManager instances to manage task execution.

Authors: 
Chantal del Carmen, Zainab Majid, Mohammad Akif Hasan, Vincent Iyegbuye

Course: CPSC 383 - Winter 2025 | T05
Assignment 3 - Multi-Agent Systems
Mar 30, 2025
"""

class LeaderCoordinator:
    def __init__(self, agent):
        """
        Initialize the LeaderCoordinator.

        Args:
            agent: The agent instance that acts as the leader.
        """
        self.agent = agent  # Use the passed-in agent instance
        self.is_leader = self.agent.get_agent_id().id == 1  # Leader is agent with ID 1
        self.assignments = {}  # Tracks agent assignments (agent_id -> task)
        self.survivors_remaining = set()  # Tracks locations of unsaved survivors
        self.team_task_managers = []  # List of TeamTaskManager instances

    def should_lead(self):
        """
        Determine if this agent should act as the leader.
        :return: True if the agent is the leader, False otherwise.
        """
        return self.is_leader

    def assign_agents_to_goals(self, agents, survivor_cells):
        pass  # to be implemented

    def find_closest_agent(self, agents, target_location):
        """
        Find the closest available agent to a target location.

        Args:
            agents: List of available agents.
            target_location: The location to find the closest agent to.

        :return: The ID of the closest agent, or None if no agents are available.
        """
        pass  # to be implemented

    def mark_survivor_saved(self, location):
        pass  # to be implemented

    def all_survivors_saved(self):
        pass  # to be implemented

    def notify_task_completed(self, location):
        """
        Notify the leader that a task has been completed.
        This method should be called by the agents when they finish their tasks.
        """
        pass
        # Implementation to be added later
