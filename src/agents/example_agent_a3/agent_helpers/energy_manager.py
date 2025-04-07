"""
Class EnergyManager: Handles energy tracking and decisions like when to SLEEP.

Authors: 
Chantal del Carmen, Zainab Majid, Mohammad Akif Hasan, Vincent Iyegbuye

Course: CPSC 383 - Winter 2025 | T05
Assignment 3 - Multi-Agent Systems
Mar 30, 2025

"""

class EnergyManager:
    def __init__(self, memory, world, agent):
        self.memory = memory
        self.world = world
        self.agent = agent

    def should_rest(self, threshold=15):

        ## Decide whether the agent should rest based on current energy and charging tile.

        current_energy = self.memory.energy
        current_loc = self.memory.get_location()
        if current_energy < threshold:
            cell = self.world.get_cell_at_location(current_loc)
            if cell and cell.is_charging_cell():
                self.agent.log(f"Low energy ({current_energy}). On charging cell at {current_loc}. Should rest.")
                return True
            else:
                self.agent.log(f"Low energy ({current_energy}). Not on charging cell at {current_loc}.")
        return False

    def update_energy(self, new_energy):

        ## Update the energy in AgentMemory based on feedback from AEGIS.

        self.memory.energy = new_energy
        self.agent.log(f"Energy updated to {new_energy}.")

    def find_nearest_charging_station(self):

        ## Searches the map for the nearest charging cell (ignores pathfinding, uses Manhattan distance).

        current_loc = self.memory.get_location()
        min_dist = float('inf')
        best_loc = None

        for row in self.world.get_world_grid():
            for cell in row:
                if cell.is_charging_cell():
                    dist = abs(current_loc[0] - cell.location.x) + abs(current_loc[1] - cell.location.y)
                    if dist < min_dist:
                        min_dist = dist
                        best_loc = (cell.location.x, cell.location.y)

        self.agent.log(f"Nearest charging cell found at {best_loc} (distance {min_dist}).")
        return best_loc

    def avoid_dangerous_cell(self, cell):

        ## Determine if a cell is dangerous (fire or killer).

        if cell.is_fire_cell() or cell.is_killer_cell():
            self.agent.log(f"Avoiding dangerous cell at {cell.location}.")
            return True
        return False

    def is_high_cost_cell(self, cell, energy_threshold=5):

        ## Determine if a cell's move cost is too high for current energy.

        if cell.move_cost > energy_threshold:
            self.agent.log(f"High cost cell at {cell.location} (cost: {cell.move_cost}).")
            return True
        return False
