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
from .astar_pathfinder import AStarPathfinder


class LeaderCoordinator:
    def __init__(self, agent, goal_planner):
        """
        Initialize the LeaderCoordinator.

        Args:
            agent: The agent instance that acts as the leader.
            goal_planner: An instance of GoalPlanner to manage goals.
        """
        self.agent = agent
        self.goal_planner = goal_planner
        self.assignments = {}
        self.agent_locations = {}
        self.survivors_remaining = []

    def should_lead(self) -> bool:
        """
        Determine if this agent should act as the leader.

        :return: True if this agent is the leader (ID 1), False otherwise.
        """
        return self.agent.get_agent_id().id == 1

    def update_agent_locations(self, world):
        """
        Update the locations of all agents in the world.

        Args:
            world: The current world instance.
        """
        grid = world.get_world_grid()
        if not grid:
            self.agent.log("ERROR: World grid is empty or invalid.")
            return

        for row in grid:
            for cell in row:
                if hasattr(cell, "agent_id_list") and cell.agent_id_list:
                    for agent_id in cell.agent_id_list:
                        self.agent_locations[agent_id] = cell.location

    def assign_agents_to_goals(self, agents, world):
        """
        Assign agents to survivor goals using the GoalPlanner.
        """
        self.update_agent_locations(world)
        survivor_goals = self.goal_planner.get_all_goals()

        available_agents = list(agents)
        for goal in survivor_goals:
            if not available_agents:
                break
            closest_agent = self.find_closest_agent(available_agents, goal.location, world)
            if closest_agent is not None:
                self.assignments[closest_agent.get_agent_id().id] = goal
                self.goal_planner.assign_goal_to_agent(closest_agent, goal)
                available_agents = [
                    agent for agent in available_agents
                    if agent.get_agent_id().id != closest_agent.get_agent_id().id
                ]

        # Assign remaining agents to unexplored areas
        for agent in available_agents:
            unexplored_direction = self.find_unexplored_direction(world, self.agent_locations[agent.get_agent_id().id])
            if unexplored_direction:
                self.agent.log(f"Assigning agent {agent.get_agent_id().id} to explore {unexplored_direction}.")
                self.assignments[agent.get_agent_id().id] = unexplored_direction

    def find_closest_agent(self, agents, target_location, world):
        """
        Find the closest available agent to a target location.

        Args:
            agents: List of available agents.
            target_location: The location to find the closest agent to.

        :return: The closest agent instance, or None if no agents are available.
        """
        best_agent = None
        best_cost = float('inf')
        for agent in agents:
            agent_location = self.agent_locations.get(agent.get_agent_id().id)
            if not agent_location:
                continue

            start_cell = world.get_cell_at(agent_location)
            goal_cell = world.get_cell_at(target_location)

            pathfinder = AStarPathfinder(world, agent)
            path = pathfinder.find_path(start_cell, goal_cell)

            # Convert goal_cell.location to a tuple before checking cost_so_far
            goal_location_tuple = (goal_cell.location.x, goal_cell.location.y)
            if path and goal_location_tuple in pathfinder.cost_so_far:
                cost = pathfinder.cost_so_far[goal_location_tuple]
                if cost < best_cost:
                    best_cost = cost
                    best_agent = agent
        return best_agent

    def mark_survivor_saved(self, location):
        """
        Mark a survivor as saved at the given location.

        Args:
            location: The location where the survivor was saved.
        """
        if location in self.survivors_remaining:
            self.survivors_remaining.remove(location)

    def all_survivors_saved(self):
        """
        Check if all survivors have been saved.

        :return: True if all survivors are saved, False otherwise.
        """
        return len(self.survivors_remaining) == 0

    def notify_task_completed(self, location):
        """
        Notify the leader that a task has been completed.

        Args:
            location: The location of the completed task.
        """
        agents_ids_to_remove = [
            agent_id for agent_id, task in self.assignments.items() if task.location == location
        ]
        for agent_id in agents_ids_to_remove:
            del self.assignments[agent_id]

        # Notify the GoalPlanner that the goal is completed
        self.goal_planner.remove_completed_goal(location)

        # Notify team task managers
        for manager in self.team_task_managers:
            if hasattr(manager, "notify_task_completed"):
                manager.notify_task_completed(location)