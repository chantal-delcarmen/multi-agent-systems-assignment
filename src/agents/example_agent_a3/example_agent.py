from typing import override

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
from aegis.api.location import create_location 

# Helper imports
from .agent_helpers.agent_memory import AgentMemory
from .agent_helpers.communication_manager import CommunicationManager
from .agent_helpers.energy_manager import EnergyManager
from .agent_helpers.astar_pathfinder import AStarPathfinder
from .agent_helpers.goal_planner import GoalPlanner
from .agent_helpers.leader_coordinator import LeaderCoordinator
from .agent_helpers.communication_manager import CommunicationManager
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
class ExampleAgent(Brain):
    def __init__(self) -> None:
        super().__init__()
        self._agent: AgentController = BaseAgent.get_agent()
        self.memory = AgentMemory(self._agent)
        self.comms = CommunicationManager(self.memory)
        self.energy_manager = EnergyManager(self.memory)
        self.goal_planner = GoalPlanner(self._agent)
        self.leader = LeaderCoordinator(self._agent)
        self.team_task_manager = TeamTaskManager(self.leader, self.comms)  # Initialize TeamTaskManager
        self.turn_counter = 0   # Keep track of number of turns

    # Handle functions:
    # You need to implement these functions
    # TODO: connect helper classes to this one 
    
    # Handle the result of sending a message
    @override
    def handle_send_message_result(self, smr: SEND_MESSAGE_RESULT) -> None:
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
        # Log the observation result for debugging
        self._agent.log(f"OBSERVE_RESULT: {ovr}")
        self._agent.log(f"{ovr}")

        # Extract the observed cell information
        cell_info = ovr.cell_info
        life_signals = ovr.life_signals

        # Check if the observed cell contains rubble
        if isinstance(cell_info.top_layer, Rubble):
            location = (cell_info.location.x, cell_info.location.y)

            # Use the remove_agents attribute to determine the number of required agents
            required_agents = cell_info.top_layer.remove_agents

            # Add the task to the TeamTaskManager
            self.team_task_manager.add_task(location, required_agents)
            self._agent.log(f"Added rubble task at {location} requiring {required_agents} agents.")

        # Check if the observed cell contains life signals (e.g., survivors)
        if life_signals.size() > 0:
            self._agent.log(f"Detected {life_signals.size()} life signals at {cell_info.location}.")
            # Optionally, prioritize this cell for rescue
            for i in range(life_signals.size()):
                signal = life_signals.get(i)
                if signal > 0:  # Positive signals indicate survivors
                    self._agent.log(f"Survivor detected with energy level {signal} at {cell_info.location}.")

    # Handle the result of saving a survivor
    @override
    def handle_save_surv_result(self, ssr: SAVE_SURV_RESULT) -> None:
        self._agent.log(f"SAVE_SURV_RESULT: {ssr}")
        self._agent.log(f"{ssr}")
        print("#--- You need to implement handle_save_surv_result function! ---#")

    # Handle the result of predicting the world
    @override
    def handle_predict_result(self, prd: PREDICT_RESULT) -> None:
        self._agent.log(f"PREDICT_RESULT: {prd}")
        self._agent.log(f"{prd}")

    # Think function
    @override
    def think(self) -> None:
        self._agent.log("Thinking")

        # Retrieve the current state of the world.
        world = self.get_world()
        if world is None:
            self._agent.log("World is None. Moving to CENTER.")
            self.send_and_end_turn(MOVE(Direction.CENTER))
            return

        # Fetch the cell at the agent’s current location.
        cell = world.get_cell_at(self._agent.get_location())
        self._agent.log(f"Cell at current location: {cell}")

        if cell is None:
            self._agent.log("No cell found at the agent's current location.")
            self.send_and_end_turn(MOVE(Direction.CENTER))
            return

        # Get the top layer at the agent’s current location.
        top_layer = cell.get_top_layer()
        self._agent.log(f"Top layer at current location: {top_layer}")

        # If the top layer is None, observe the surroundings.
        if top_layer is None:
            self._agent.log("Top layer is None. Observing surroundings.")
            current_location = self._agent.get_location()
            self.send_and_end_turn(OBSERVE(current_location))
            return

        # If a survivor is present, save it and end the turn.
        if isinstance(top_layer, Survivor):
            self.send_and_end_turn(SAVE_SURV())
            return

        # If rubble is present, coordinate a TEAM_DIG task.
        if isinstance(top_layer, Rubble):
            location = (cell.location.x, cell.location.y)
            self._agent.log(f"Checking rubble at location {location}.")

            # Use the remove_agents attribute to determine the number of required agents
            required_agents = top_layer.remove_agents

            if not self.team_task_manager.coordinate_team_dig(self._agent.get_id(), location):
                self._agent.log("Not enough agents for TEAM_DIG. Moving to CENTER.")
                self.send_and_end_turn(MOVE(Direction.CENTER))
            else:
                self._agent.log(f"Enough agents available. Sending TEAM_DIG command with {required_agents} agents.")
                self.send_and_end_turn(TEAM_DIG())
            return

        # Find a goal (survivor location)
        goal_cell = self.find_survivor(world)
        if goal_cell is not None:
            start_cell = cell
            pathfinder = AStarPathfinder(world, self._agent)
            path = pathfinder.find_path(start_cell, goal_cell)

            if len(path) > 1:
                next_move = path[1]
                direction = start_cell.location.direction_to(next_move.location)
                self.send_and_end_turn(MOVE(direction))
                return
            else:
                # If the path is empty, stay in place
                self.send_and_end_turn(MOVE(Direction.CENTER))
                return

    # Send a command and end your turn
    def send_and_end_turn(self, command: AgentCommand):
        """Send a command and end your turn."""
        self._agent.log(f"SENDING {command}")
        self._agent.send(command)
        self.turn_counter += 1   # Increment the agent's turn number
        self.memory.set_turn_counter(self.turn_counter) # Update the agent's turn number in memory
        self._agent.send(END_TURN())

    # Find survivor (goal cell) in the world
    def find_survivor(self, world):
        # Iterate over all cells in the world grid
        for row in world.get_world_grid():
            for cell in row:
                # If the cell has not been observed, observe it
                if not self.memory.is_cell_observed(cell.location):
                    self._agent.log(f"Observing cell at {cell.location}")
                    self.send_and_end_turn(OBSERVE(cell.location))
                    return None  # Wait for the observation result

                # Check if the cell has survivors
                if cell.has_survivors:
                    return cell

                # If the cell has rubble, observe it to detect life signals
                if isinstance(cell.top_layer, Rubble):
                    self._agent.log(f"Rubble detected at {cell.location}. Observing for life signals.")
                    self.send_and_end_turn(OBSERVE(cell.location))
                    return None  # Wait for the observation result
        return None
