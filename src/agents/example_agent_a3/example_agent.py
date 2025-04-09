from typing import override
# import sys
# import os

# # Add the `src` directory to the Python path
# current_dir = os.path.dirname(os.path.abspath(__file__))
# src_dir = os.path.abspath(os.path.join(current_dir, "../src"))
# if src_dir not in sys.path:
#     sys.path.append(src_dir)


# If you need to import anything, add it to the import below.
from aegis import (
    AgentID,
    Location,
    SLEEP,
    END_TURN,
    SEND_MESSAGE_RESULT,
    MOVE,
    OBSERVE,
    OBSERVE_RESULT,
    PREDICT_RESULT,
    SAVE_SURV,
    SAVE_SURV_RESULT,
    SEND_MESSAGE,
    TEAM_DIG,
    AgentCommand,
    AgentIDList,
    Direction,
    Rubble,
    Survivor,
)
from a3.agent import BaseAgent, Brain, AgentController
from aegis.api.location import Location, create_location
from aegis.api.cell import Cell
from aegis.api.world import World
from aegis.common.direction import Direction

# Helper imports
from .agent_helpers.agent_memory import AgentMemory
from .agent_helpers.communication_manager import CommunicationManager
from .agent_helpers.energy_manager import EnergyManager
from .agent_helpers.astar_pathfinder import AStarPathfinder
from .agent_helpers.goal_planner import GoalPlanner
from .agent_helpers.leader_coordinator import LeaderCoordinator
from .agent_helpers.team_task_manager import TeamTaskManager

"""
Class ExampleAgent:
This class is responsible for implementing the agent's logic

Authors: 
Chantal del Carmen, Zainab Majid, Mohammad Akif Hasan, Vincent Iyegbuye

Course: CPSC 383 - Winter 2025 | T05
Assignment 3 - Multi-Agent Systems
Mar 30, 2025
"""

def get_direction_from_locations(start: Location, end: Location) -> Direction | None:
    """
    Calculate the direction from the start location to the end location.

    Args:
        start: The starting location (Location object).
        end: The ending location (Location object).

    Returns:
        The Direction from start to end, or None if no valid direction exists.
    """
    dx = end.x - start.x
    dy = end.y - start.y

    for direction in Direction:
        if direction.dx == dx and direction.dy == dy:
            return direction
    return None


class ExampleAgent(Brain):
    def __init__(self) -> None:
        super().__init__()
        self._agent: AgentController = BaseAgent.get_agent()
        self.memory = AgentMemory(self._agent)
        self.comms = CommunicationManager(self.memory, self._agent)
        self.energy_manager = EnergyManager(self.memory)
        self.goal_planner = GoalPlanner(self._agent)
        self.leader_coordinator = LeaderCoordinator(self._agent, self.goal_planner)
        self.team_task_manager = TeamTaskManager(self.leader_coordinator, self.comms)
        self.turn_counter = 0

    # Handle the result of sending a message
    @override
    def handle_send_message_result(self, smr: SEND_MESSAGE_RESULT) -> None:
        """
        Handle the result of sending a message.
        """
        # Log the raw SEND_MESSAGE_RESULT object for debugging
        if not smr.msg:
            self._agent.log("SEND_MESSAGE_RESULT contains no message. Skipping.")
            return

        # Parse the message using the CommunicationManager
        parsed_messages = self.comms.parse_messages([smr.msg])
        if not parsed_messages:
            self._agent.log("Parsed messages are empty or invalid. Skipping.")
            return

        # Delegate handling of parsed messages
        for message in parsed_messages:
            if message["type"] in ["TASK_COMPLETED", "MEET"]:
                # Delegate task-related messages to the TeamTaskManager
                self.team_task_manager.handle_task_message(message)
            else:
                # Handle other messages using CommunicationManager
                self.comms.handle_parsed_message(message, self._agent)

    # Handle the result of observing the world
    @override
    def handle_observe_result(self, ovr: OBSERVE_RESULT) -> None:
        """
        Handle the result of observing the world.
        """
        self._agent.log(f"OBSERVE_RESULT received: {ovr}")

        # Extract the observed cell information
        cell_info = ovr.cell_info
        life_signals = ovr.life_signals

        if cell_info:
            self._agent.log(f"Observed cell at location {cell_info.location}: {cell_info}")
        else:
            self._agent.log("No cell information available in OBSERVE_RESULT.")
            return

        # Check if the observed cell contains rubble
        if isinstance(cell_info.top_layer, Rubble):
            location = cell_info.location
            required_agents = cell_info.top_layer.remove_agents
            self.team_task_manager.add_task(location, required_agents, task_type="DIG")
            self._agent.log(f"Added rubble task at {location} requiring {required_agents} agents.")
        else:
            self._agent.log(f"No rubble detected at {cell_info.location}.")

        # Check if the observed cell contains life signals (e.g., survivors)
        if life_signals and life_signals.size() > 0:
            self._agent.log(f"Detected {life_signals.size()} life signals at {cell_info.location}.")
            for i in range(life_signals.size()):
                signal = life_signals.get(i)
                if signal > 0:  # Positive signals indicate survivors
                    self._agent.log(f"Survivor detected with energy level {signal} at {cell_info.location}.")
                    self.team_task_manager.add_task(cell_info.location, 1, task_type="SAVE")
                    self._agent.log(f"Added SAVE task for survivor at {cell_info.location}.")
        else:
            self._agent.log(f"No life signals detected at {cell_info.location}.")

    # Handle the result of saving a survivor
    @override
    def handle_save_surv_result(self, ssr: SAVE_SURV_RESULT) -> None:
        """
        Handle the result of saving a survivor.
        """
        self._agent.log(f"SAVE_SURV_RESULT received: {ssr}")
        if ssr.success:
            self._agent.log("Successfully saved a survivor!")
        else:
            self._agent.log("Failed to save a survivor.")

    # Handle the result of predicting the world
    @override
    def handle_predict_result(self, prd: PREDICT_RESULT) -> None:
        """
        Handle the result of predicting the world.
        """
        self._agent.log(f"PREDICT_RESULT received: {prd}")

    # Main decision-making function
    @override
    def think(self) -> None:
        """
        Main decision-making function for the agent.
        """
        self._agent.log("Thinking")

        # Retrieve the current state of the world.
        world = self.get_world()
        if world is None:
            self._agent.log("World is None. Moving to CENTER.")
            self.send_and_end_turn(MOVE(Direction.CENTER))
            return

        # Check the agent's current location and cell
        current_location = self._agent.get_location()
        cell = world.get_cell_at(current_location)

        if not cell:
            self._agent.log(f"No cell found at {current_location}. Moving to CENTER.")
            self.send_and_end_turn(MOVE(Direction.CENTER))
            return

        # If the agent is the leader, delegate leader-specific tasks
        if self.leader_coordinator.should_lead():
            self._agent.log("I am the leader. Delegating tasks.")
            agents = self.memory.get_all_agents()
            self.leader_coordinator.assign_agents_to_goals(agents, world)
            self.find_survivor(world)  # Search for survivors as part of leader tasks
        else:
            self._agent.log("I am not the leader. Performing assigned tasks.")
            self.perform_assigned_task()

        # Handle the top layer of the current cell
        top_layer = cell.get_top_layer()
        if top_layer is None:
            if not self.memory.is_cell_observed(current_location):
                self.memory.mark_cell_as_observed(current_location)
                self.send_and_end_turn(OBSERVE(current_location))
            else:
                unexplored_direction = self.find_unexplored_direction(world, cell)
                if unexplored_direction:
                    self.send_and_end_turn(MOVE(unexplored_direction))
                else:
                    self.send_and_end_turn(MOVE(Direction.CENTER))
            return

        # Handle specific objects in the top layer
        if isinstance(top_layer, Survivor):
            self._agent.log("Survivor detected. Sending SAVE_SURV command.")
            self.send_and_end_turn(SAVE_SURV())
            return

        if isinstance(top_layer, Rubble):
            location = (cell.location.x, cell.location.y)
            self._agent.log(f"Rubble detected at {location}. Coordinating TEAM_DIG.")
            self.team_task_manager.coordinate_team_dig(self._agent.get_agent_id(), location)
            self.send_and_end_turn(TEAM_DIG())
            return

        # Fallback exploration
        unexplored_direction = self.find_unexplored_direction(world, cell)
        if unexplored_direction:
            self.send_and_end_turn(MOVE(unexplored_direction))
        else:
            self.send_and_end_turn(MOVE(Direction.CENTER))

    # Send a command and end your turn
    def send_and_end_turn(self, command: AgentCommand):
        """
        Send a command and end your turn.
        """
        self._agent.log(f"SENDING {command}")
        self._agent.send(command)
        self.turn_counter += 1
        self.memory.set_turn_counter(self.turn_counter)
        self._agent.send(END_TURN())

    # Find an unexplored direction
    def find_unexplored_direction(self, world: World, current_cell: Cell):
        """
        Find an unexplored direction from the current cell, avoiding killer cells and fire cells.
        If the agent is in a dangerous cell, prioritize escaping to a safer cell.
        """
        current_location = current_cell.location

        # Check if the current cell is dangerous
        if current_cell.is_killer_cell() or current_cell.is_fire_cell():
            self._agent.log(f"Agent is in a dangerous cell at {current_location}. Attempting to escape.")
            for direction in Direction:
                neighbor_location = create_location(
                    current_location.x + direction.dx,
                    current_location.y + direction.dy
                )

                # Check if the neighbor location is within bounds
                if not (0 <= neighbor_location.x < world.width and 0 <= neighbor_location.y < world.height):
                    continue

                neighbor_cell = world.get_cell_at(neighbor_location)
                if neighbor_cell and not neighbor_cell.is_killer_cell() and not neighbor_cell.is_fire_cell():
                    self._agent.log(f"Escaping to safer cell at {neighbor_location}.")
                    return direction

        # If not in a dangerous cell, find an unexplored direction
        for direction in Direction:
            neighbor_location = create_location(
                current_location.x + direction.dx,
                current_location.y + direction.dy
            )

            # Check if the neighbor location is within bounds
            if not (0 <= neighbor_location.x < world.width and 0 <= neighbor_location.y < world.height):
                continue

            neighbor_cell = world.get_cell_at(neighbor_location)
            if neighbor_cell and not self.memory.is_cell_observed(neighbor_location):
                # Avoid killer cells and fire cells
                if neighbor_cell.is_killer_cell() or neighbor_cell.is_fire_cell():
                    self._agent.log(f"Avoiding dangerous cell at {neighbor_location} (KILLER_CELL or FIRE_CELL).")
                    continue
                return direction

        return None

    # Perform the assigned task
    def perform_assigned_task(self):
        """
        Perform the task assigned by the leader.
        """
        assigned_task = self.memory.get_assigned_task()
        world = self.get_world()
        current_location = self._agent.get_location()
        current_cell = world.get_cell_at(current_location)

        if not assigned_task:
            self._agent.log("No assigned task. Exploring the grid.")
            unexplored_direction = self.find_unexplored_direction(world, current_cell)
            if unexplored_direction:
                self.send_and_end_turn(MOVE(unexplored_direction))
            else:
                self.send_and_end_turn(MOVE(Direction.CENTER))
            return

        task_type = assigned_task["type"]
        task_location = assigned_task["location"]

        if task_type == "DIG":
            self._agent.log(f"Performing DIG task at {task_location}.")
            self.send_and_end_turn(TEAM_DIG())
        elif task_type == "SAVE":
            self._agent.log(f"Performing SAVE task at {task_location}.")
            self.send_and_end_turn(SAVE_SURV())
        elif task_type == "MOVE":
            self._agent.log(f"Moving to assigned location {task_location}.")
            goal_cell = world.get_cell_at(task_location)
            pathfinder = AStarPathfinder(world, self._agent)
            path = pathfinder.find_path(current_cell, goal_cell)
            if path:
                self.send_and_end_turn(MOVE(path[0].direction))
            else:
                self._agent.log("No valid path found. Exploring instead.")
                unexplored_direction = self.find_unexplored_direction(world, current_cell)
                if unexplored_direction:
                    self.send_and_end_turn(MOVE(unexplored_direction))
                else:
                    self.send_and_end_turn(MOVE(Direction.CENTER))
        else:
            self._agent.log(f"Unknown task type: {task_type}. Exploring instead.")
            unexplored_direction = self.find_unexplored_direction(world, current_cell)
            if unexplored_direction:
                self.send_and_end_turn(MOVE(unexplored_direction))
            else:
                self.send_and_end_turn(MOVE(Direction.CENTER))

    # Find survivor (goal cell) in the world
    def find_survivor(self, world: World):
        """
        Search for survivors in the world using GoalPlanner and execute tasks for them.
        """
        self._agent.log("Searching for survivors in the world using GoalPlanner.")
        current_location = self._agent.get_location()
        current_cell = world.get_cell_at(current_location)

        # Use GoalPlanner to find all survivor goals
        self.goal_planner.find_survivor_goals(world)

        # Log all survivors found
        all_goals = self.goal_planner.get_all_goals()
        if all_goals:
            self._agent.log(f"Survivors found at the following locations: {[goal.location for goal in all_goals]}")
        else:
            self._agent.log("No survivors found in the world.")

        # Get the next goal (survivor location) from the GoalPlanner
        next_goal = self.goal_planner.get_next_goal()

        if next_goal:
            self._agent.log(f"Next survivor goal found at {next_goal.location}. Calculating path.")
            path = self.goal_planner.find_path_to_goal(world, current_cell, next_goal)

            if path:
                # Add a SAVE task for the survivor
                self._agent.log(f"Path to survivor at {next_goal.location} found. Adding SAVE task.")
                self.team_task_manager.add_task(next_goal.location, 1)

                # Calculate the direction to the first step in the path
                first_step = path[0]
                direction = get_direction_from_locations(current_location, first_step.location)
                if direction:
                    self._agent.log(f"Moving towards survivor at {next_goal.location} in direction {direction}.")
                    self.send_and_end_turn(MOVE(direction))
                else:
                    self._agent.log("Failed to calculate direction for the first step in the path.")
                    self.send_and_end_turn(MOVE(Direction.CENTER))
            else:
                # If no path is found, log the issue and mark the goal as unreachable
                self._agent.log(f"No path to survivor at {next_goal.location}. Marking as unreachable.")
                self.goal_planner.mark_goal_unreachable(next_goal)
                self._agent.log(f"Replanning survivor goals after marking {next_goal.location} as unreachable.")
                self.goal_planner.replan_goals(world)
        else:
            # If no goals are available, fallback to exploration
            self._agent.log("No survivor goals available. Exploring the grid.")
            unexplored_direction = self.find_unexplored_direction(world, current_cell)
            if unexplored_direction:
                self.send_and_end_turn(MOVE(unexplored_direction))
            else:
                self.send_and_end_turn(MOVE(Direction.CENTER))
