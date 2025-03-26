import heapq

from aegis.api.location import create_location
from aegis.common.direction import Direction

class AStarPathfinder:
    def __init__(self, world, agent):
        self.world = world
        self.agent = agent
        self.frontier = []
        self.came_from = {}
        self.cost_so_far = {}
        self.start_cell = None
        self.goal_cell = None

    def heuristic(self, new_loc, end_loc):
        return max(abs(new_loc.x - end_loc.x), abs(new_loc.y - end_loc.y))

    def get_neighbours(self, current_cell):
        neighbour_list = []
        location = current_cell.location

        for direction in Direction:
            new_loc = create_location(location.x + direction.dx, location.y + direction.dy)
            new_cell = self.world.get_cell_at(new_loc)
            agent_energy = self.agent.get_energy_level()

            if new_cell and not new_cell.is_fire_cell() and not new_cell.is_killer_cell() and agent_energy > new_cell.move_cost:
                neighbour_list.append(new_cell)

        return neighbour_list

    def find_path(self, start_cell, goal_cell):
        self.frontier = []
        self.came_from = {}
        self.cost_so_far = {}

        heapq.heappush(self.frontier, (0, start_cell.location))
        self.came_from[start_cell.location] = None
        self.cost_so_far[start_cell.location] = 0

        while self.frontier:
            _, current_loc = heapq.heappop(self.frontier)
            current_cell = self.world.get_cell_at(current_loc)

            if current_cell == goal_cell:
                break

            for neighbour in self.get_neighbours(current_cell):
                new_cost = self.cost_so_far[current_cell.location] + neighbour.move_cost
                if neighbour.location not in self.cost_so_far or new_cost < self.cost_so_far[neighbour.location]:
                    self.cost_so_far[neighbour.location] = new_cost
                    priority = new_cost + self.heuristic(goal_cell.location, neighbour.location)
                    heapq.heappush(self.frontier, (priority, neighbour.location))
                    self.came_from[neighbour.location] = current_cell.location

        # Reconstruct path
        path = []
        current_cell = goal_cell
        while current_cell != start_cell:
            path.append(current_cell)
            current_cell = self.world.get_cell_at(self.came_from[current_cell.location])
        path.append(start_cell)
        path.reverse()
        return path
