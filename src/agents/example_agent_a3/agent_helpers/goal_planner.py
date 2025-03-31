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
        self.agent = agent
        self.goal = None

    def find_survivor_goals(self, world):
        """
        Return a list of cells that contain survivors.
        In your example, you are simply scanning the entire grid in find_survivor().
        You could do it here instead and store them as potential goals.
        """
        goals = []
        for row in world.get_world_grid():
            for cell in row:
                if cell.has_survivors:
                    goals.append(cell)
        return goals

