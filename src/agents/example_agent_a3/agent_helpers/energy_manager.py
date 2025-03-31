"""
Class EnergyManager: Handles energy tracking and decisions like when to SLEEP.

Authors: 
Chantal del Carmen, Zainab Majid, Mohammad Akif Hasan, Vincent Iyegbuye

Course: CPSC 383 - Winter 2025 | T05
Assignment 3 - Multi-Agent Systems
Mar 30, 2025

"""

class EnergyManager:
    def __init__(self, memory):
        self.memory = memory

    def should_rest(self, threshold=15) -> bool:
        """
        Return True if the agent's energy level is below a threshold.
        Then the agent might want to SLEEP if it's on a charging cell.
        """
        return self.memory.energy < threshold

    def update_energy(self, amount: int):
        """
        Add or subtract from the agent's energy. If it hits zero or negative,
        the agent is considered 'out'.
        """
        new_val = self.memory.energy + amount
        if new_val < 0:
            new_val = 0
        self.memory.energy = new_val
