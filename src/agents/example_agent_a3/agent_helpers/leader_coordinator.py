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
from agents.example_agent_a3.agent_helpers.astar_pathfinder import AStarPathfinder


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

    def assign_agents_to_goals(self, agents, survivor_cells,world):
          # to be implemented
        if not self.should_lead():
            return

        self.survivors_remaining.update(survivor_cells)

        available_agents = list(agents)

        for cell in survivor_cells:
            if not available_agents:
                break
            closest_agent = self.find_closest_agent(available_agents, cell,world)
            if closest_agent is not None:
                self.assignments[closest_agent] = cell
                available_agents = [
                    agent for agent in available_agents
                    if agent.get_agent_id().id != closest_agent
                ]

    def find_closest_agent(self, agents, target_location, world):
        """
        Find the closest available agent to a target location.

        Args:
            agents: List of available agents.
            target_location: The location to find the closest agent to.

        :return: The ID of the closest agent, or None if no agents are available.
        """
        best_agent = None
        best_cost = float('inf')
        for agent in agents:
            start_cell = world.get_cell_at(agent.get_location())
            goal_cell = world.get_cell_at(target_location)
            
            pathfinder = AStarPathfinder(world, agent)
            path = pathfinder.find_path(start_cell, goal_cell)
            
            if path and goal_cell.location in pathfinder.cost_so_far:
                cost = pathfinder.cost_so_far[goal_cell.location]
                if cost < best_cost:
                    best_cost = cost
                    best_agent = agent
                    
        return best_agent if best_agent else None
                    
        
            
    def mark_survivor_saved(self, location):
        if location in self.survivors_remaining:
            self.survivors_remaining.remove(location)

    def all_survivors_saved(self):
        return len(self.survivors_remaining) == 0   # to be implemented

    def notify_task_completed(self, location):
        """
        Notify the leader that a task has been completed.
        This method should be called by the agents when they finish their tasks.
        """
        
        agents_ids_to_remove = [
            agent_id for agent_id, task in self.assignments.items() if task == location
        ]
        for agent_id in agents_ids_to_remove:
            del self.assignments[agent_id]
            
        # Mark the survivors as saved
        self.mark_survivor_saved(location)
        
        for manager in self.team_task_managers:
            if hasattr(manager, "notify_task_completed"):
                manager.notify_task_completed(location)