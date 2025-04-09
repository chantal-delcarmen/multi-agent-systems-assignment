"""
Class GoalPlanner: For leader agents. Finds survivor locations in the world
and supports goal assignment and chaining.

Authors: 
Chantal del Carmen, Zainab Majid, Mohammad Akif Hasan, Vincent Iyegbuye

Course: CPSC 383 - Winter 2025 | T05
Assignment 3 - Multi-Agent Systems
Mar 30, 2025
"""

from .astar_pathfinder import AStarPathfinder

class GoalPlanner:
    def __init__(self, agent):
        """
        Initializes the GoalPlanner with a reference to the agent.

        Args:
            agent: The leader agent using this GoalPlanner.
        """
        self.agent = agent
        self._survivor_goals = []
        self._unreachable_goals = set()  # Track goals found to be unreachable
        self._current_goal_index = 0

    def find_survivor_goals(self, world):
        """
        Scans the world to find all cells that contain survivors and stores
        them in an internal list (self._survivor_goals), sorted by path length
        using A* pathfinding.

        Args:
            world: The world instance that provides access to cells.
        """
        survivor_goals = []
        agent_location = self.agent.get_location()
        current_cell = world.get_cell_at(agent_location)

        self.agent.log(f"DEBUG: Agent location: {agent_location}")

        try:
            # Iterate over the 2D grid of cells
            for row in world.get_world_grid():
                for cell in row:
                    # Check if the cell has survivors
                    if getattr(cell, "has_survivors", False):
                        # Use A* to check if the goal is reachable
                        path = self.find_path_to_goal(world, current_cell, cell)
                        if path:
                            survivor_goals.append((cell, path))
        except AttributeError:
            self.agent.log("Error: world.get_world_grid() is not iterable or invalid.")
            return

        # Log the total number of survivor goals found
        self.agent.log(f"Found {len(survivor_goals)} reachable cells with survivors.")

        # Sort by path length for a "closest-first" approach
        survivor_goals.sort(key=lambda item: len(item[1]))

        # Store the sorted goals
        self._survivor_goals = [goal[0] for goal in survivor_goals]
        self._current_goal_index = 0  # Reset to start with the first goal
        self.agent.log(f"Added {len(self._survivor_goals)} survivor goals.")

    def find_path_to_goal(self, world, start_cell, goal_cell):
        """
        Finds the shortest path from the start cell to the goal cell using A*.

        Args:
            world: The world instance.
            start_cell: The starting cell (agent's current location).
            goal_cell: The goal cell (e.g., survivor location).

        Returns:
            A list of cells representing the path, or an empty list if no path is found.
        """
        self.agent.log(f"Calculating path from {start_cell.location} to {goal_cell.location}.")
        pathfinder = AStarPathfinder(world, self.agent)
        path = pathfinder.find_path(start_cell, goal_cell)

        if path:
            self.agent.log(f"Path to {goal_cell.location} found with {len(path)} steps.")
        else:
            self.agent.log(f"No path to {goal_cell.location} found.")
        return path

    def get_next_goal(self):
        """
        Returns the next available survivor goal in the list, or None if
        there are no remaining goals or we've reached the end of the list.

        Returns:
            The next survivor cell or None if no more goals exist.
        """
        if self._current_goal_index < len(self._survivor_goals):
            goal = self._survivor_goals[self._current_goal_index]
            self._current_goal_index += 1
            return goal
        return None

    def get_all_goals(self):
        """
        Returns a list of all currently known survivor goals.
        Useful for batch assignment or overview of pending rescues.

        Returns:
            A list of survivor goal cells.
        """
        return list(self._survivor_goals)

    def mark_goal_unreachable(self, goal_cell):
        """
        Marks a particular goal as unreachable, for example, if pathfinding fails
        or hazards prevent access. This can help the planner avoid repeatedly
        attempting to assign impossible goals.

        Args:
            goal_cell: The cell representing the unreachable goal.
        """
        self.agent.log(f"Marking goal at {goal_cell.location} as unreachable.")
        self._unreachable_goals.add(goal_cell)
        if goal_cell in self._survivor_goals:
            self._survivor_goals.remove(goal_cell)

    def reset_goals(self):
        """
        Clears all known goals, typically used when the environment changes
        drastically (new map, updated world state) and you want to recalculate.
        """
        self._survivor_goals.clear()
        self._unreachable_goals.clear()
        self._current_goal_index = 0

    def replan_goals(self, world):
        """
        Re-checks the world for current survivor locations and recalculates
        a fresh list of goals. You might call this if the environment has
        changed significantly or new survivors were discovered.

        Args:
            world: The current world instance.
        """
        self.reset_goals()
        self.find_survivor_goals(world)

    def has_remaining_goals(self):
        """
        Checks if there are still valid goals not yet assigned or pursued.

        Returns:
            True if there are remaining goals; False otherwise.
        """
        return self._current_goal_index < len(self._survivor_goals)

    def remove_completed_goal(self, goal_cell):
        """
        Removes a completed goal from the internal list and adjusts the index
        accordingly. This is useful when an agent successfully rescues a survivor
        so the planner no longer sees that goal as pending.

        Args:
            goal_cell: The cell representing the goal that was completed.
        """
        if goal_cell in self._survivor_goals:
            self.agent.log(f"Removing completed goal at {goal_cell.location}.")
            index = self._survivor_goals.index(goal_cell)
            self._survivor_goals.remove(goal_cell)
            if index < self._current_goal_index:
                self._current_goal_index -= 1

    def detect_and_replan_goals(self, world, significant_change_detected):
        """
        Detects significant changes in the environment and triggers replanning
        if necessary.

        Args:
            world: The current world instance.
            significant_change_detected: A boolean indicating if the environment
                                         has changed significantly.
        """
        if significant_change_detected:
            self.agent.log("Significant change detected. Replanning goals.")
            self.replan_goals(world)

    def assign_goal_to_agent(self, agent_id, goal_cell):
        """
        Assigns a specific goal to another agent.

        Args:
            agent_id: The ID of the agent to assign the goal to.
            goal_cell: The cell representing the goal to assign.
        """
        if goal_cell in self._survivor_goals:
            self.agent.comms.send_message(agent_id, f"GOAL {goal_cell.location}")
            self.agent.log(f"Assigned goal at {goal_cell.location} to agent {agent_id}.")
            self.remove_completed_goal(goal_cell)
        else:
            self.agent.log(f"Goal at {goal_cell.location} is not in the current goal list.")