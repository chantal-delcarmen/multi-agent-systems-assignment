from typing import override

# If you need to import anything, add it to the import below.
from aegis import (
    AgentID,
    Location,
    SLEEP,
    END_TURN,
    SEND_MESSAGE_RESULT,
    MOVE,
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
        self.turn_counter = 0   # Keep track of number of turns

    # Handle functions:
    # You need to implement these functions
    # TODO: connect helper classes to this one 
    
    # Handle the result of sending a message
    # todo:zainab

    @override
    def handle_send_message_result(self, smr: SEND_MESSAGE_RESULT) -> None:
        # Log the raw SEND_MESSAGE_RESULT object for debugging
        self._agent.log(f"SEND_MESSAGE_RESULT: {smr}")
        self._agent.log(f"Raw message from SEND_MESSAGE_RESULT: {smr.msg}")

        # Check if the message is valid
        if not smr.msg:
            self._agent.log("SEND_MESSAGE_RESULT contains no message. Skipping.")
            return

        # Parse the message using the CommunicationManager
        parsed_messages = self.comms.parse_messages([smr.msg])
        if not parsed_messages:
            self._agent.log("Parsed messages are empty or invalid. Skipping.")
            return

        # Iterate through the parsed messages and handle them based on their type
        for message in parsed_messages:
            message_type = message.get("type")
            if message_type == "FOUND":
                # Handle a "FOUND" message (e.g., a location of interest was found)
                x, y = message["location"]
                self._agent.log(f"FOUND message received: Location ({x}, {y})")
                self.memory.add_found_location(x, y)
            elif message_type == "DONE":
                # Handle a "DONE" message (e.g., a task was completed)
                x, y = message["location"]
                self._agent.log(f"DONE message received: Location ({x}, {y})")
                self.memory.add_done_location(x, y)
            elif message_type == "ASSIGN":
                # Handle an "ASSIGN" message (e.g., a task was assigned to an agent)
                agent_id = message["agent_id"]
                x, y = message["location"]
                self._agent.log(f"ASSIGN message received: Agent {agent_id} assigned to ({x}, {y})")
                self.memory.add_assignment(agent_id, x, y)
            else:
                # Handle unknown message types
                self._agent.log(f"Unknown message type: {message_type}")

    # Handle the result of observing the world
    @override
    def handle_observe_result(self, ovr: OBSERVE_RESULT) -> None:
        self._agent.log(f"OBSERVE_RESULT: {ovr}")
        self._agent.log(f"{ovr}")
        print("#--- You need to implement handle_observe_result function! ---#")

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
            self.send_and_end_turn(MOVE(Direction.CENTER))
            return

        # Fetch the cell at the agent’s current location. If the location is outside the world’s bounds,
        # return a default move action and end the turn.
        cell = world.get_cell_at(self._agent.get_location())
        if cell is None:
            self.send_and_end_turn(MOVE(Direction.CENTER))
            return

        # Get the top layer at the agent’s current location.
        top_layer = cell.get_top_layer()

        # If a survivor is present, save it and end the turn.
        if isinstance(top_layer, Survivor):
            self.send_and_end_turn(SAVE_SURV())
            return

        # If rubble is present, clear it and end the turn.
        if isinstance(top_layer, Rubble):
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
        for row in world.get_world_grid():
            for cell in row:
                if cell.has_survivors:
                    return cell
        return None
