"""
Class GoalPlanner: For leader agents. Finds survivor locations in the world
and supports goal assignment and chaining.

Authors: 
Chantal del Carmen, Zainab Majid, Mohammad Akif Hasan, Vincent Iyegbuye

Course: CPSC 383 - Winter 2025 | T05
Assignment 3 - Multi-Agent Systems
Mar 30, 2025

"""


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
        them in an internal list (self._survivor_goals), sorted by Manhattan
        distance from the agent's current location.

        Args:
            world: The world instance that provides access to cells.
        """
        survivor_goals = []
        agent_location = self.agent.location

        try:
            # Ensure world.cells is iterable
            for cell in world.cells:
                # Ensure cell has the method has_survivor()
                if hasattr(cell, "has_survivor") and callable(cell.has_survivor):
                    if cell.has_survivor():
                        survivor_goals.append(cell)
                else:
                    self.agent.log(f"Cell {cell} does not have a valid has_survivor() method.")
        except AttributeError:
            self.agent.log("Error: world.cells is not iterable or invalid.")
            return

        # Sort by Manhattan distance for a simple "closest-first" approach.
        survivor_goals.sort(
            key=lambda c: abs(c.location.x - agent_location.x)
                          + abs(c.location.y - agent_location.y)
        )

        # Store the sorted goals
        self._survivor_goals = survivor_goals
        self._current_goal_index = 0  # Reset to start with the first goal
        self.agent.log(f"Found {len(self._survivor_goals)} survivor goals.")

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
        self._unreachable_goals.add(goal_cell)
        # Remove it if it's still in the _survivor_goals list
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
            index = self._survivor_goals.index(goal_cell)
            self._survivor_goals.remove(goal_cell)
            # Adjust current goal index if needed
            if index < self._current_goal_index:
                self._current_goal_index -= 1