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
        # Log the observation result for debugging
        self._agent.log(f"OBSERVE_RESULT received: {ovr}")

        # Extract the observed cell information
        cell_info = ovr.cell_info
        life_signals = ovr.life_signals

        # Log the cell information
        if cell_info:
            self._agent.log(f"Observed cell at location {cell_info.location}: {cell_info}")
        else:
            self._agent.log("No cell information available in OBSERVE_RESULT.")
            return

        # Check if the observed cell contains rubble
        if isinstance(cell_info.top_layer, Rubble):
            location = cell_info.location

            # Use the remove_agents attribute to determine the number of required agents
            required_agents = cell_info.top_layer.remove_agents

            # Add the task to the TeamTaskManager
            self.team_task_manager.add_task(location, required_agents, task_type="DIG")
            self._agent.log(f"Added rubble task at {location} requiring {required_agents} agents.")
        else:
            self._agent.log(f"No rubble detected at {cell_info.location}.")

        # Check if the observed cell contains life signals (e.g., survivors)
        if life_signals and life_signals.size() > 0:
            self._agent.log(f"Detected {life_signals.size()} life signals at {cell_info.location}.")
            # Log each life signal for debugging
            for i in range(life_signals.size()):
                signal = life_signals.get(i)
                self._agent.log(f"Life signal {i}: {signal}")

                if signal > 0:  # Positive signals indicate survivors
                    self._agent.log(f"Survivor detected with energy level {signal} at {cell_info.location}.")
                    # Add a task to save the survivor
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

    # Think function
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
            self.team_task_manager.coordinate_team_dig(self._agent.get_id(), location)
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
    def find_unexplored_direction(self, world, current_cell):
        """
        Find an unexplored direction from the current cell.
        """
        current_location = current_cell.location
        for direction in Direction:
            neighbor_location = create_location(
                current_location.x + direction.dx,
                current_location.y + direction.dy
            )
            neighbor_cell = world.get_cell_at(neighbor_location)
            if neighbor_cell and not self.memory.is_cell_observed(neighbor_location):
                return direction
        return None

    # Perform the assigned task
    def perform_assigned_task(self):
        """
        Perform the task assigned by the leader.
        """
        assigned_task = self.memory.get_assigned_task()
        if not assigned_task:
            world = self.get_world()
            current_location = self._agent.get_location()
            current_cell = world.get_cell_at(current_location)

            if current_cell is None:
                self.send_and_end_turn(MOVE(Direction.CENTER))
                return

            unexplored_direction = self.find_unexplored_direction(world, current_cell)
            if unexplored_direction:
                self.send_and_end_turn(MOVE(unexplored_direction))
            else:
                self.send_and_end_turn(MOVE(Direction.CENTER))
            return

        task_type = assigned_task["type"]
        task_location = assigned_task["location"]

        if task_type == "DIG":
            self.send_and_end_turn(TEAM_DIG())
        elif task_type == "SAVE":
            self.send_and_end_turn(SAVE_SURV())
        elif task_type == "MOVE":
            current_location = self._agent.get_location()
            direction = current_location.direction_to(task_location)
            self.send_and_end_turn(MOVE(direction))
        else:
            unexplored_direction = self.find_unexplored_direction(world, current_cell)
            if unexplored_direction:
                self.send_and_end_turn(MOVE(unexplored_direction))
            else:
                self.send_and_end_turn(MOVE(Direction.CENTER))

    # Find survivor (goal cell) in the world
    def find_survivor(self, world):
        """
        Search for a survivor in the world grid.
        """
        self._agent.log("Searching for survivors in the world.")
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
                    self._agent.log(f"Survivor found at {cell.location}")
                    return cell

                # If the cell has rubble, observe it to detect life signals
                if isinstance(cell.top_layer, Rubble):
                    self._agent.log(f"Rubble detected at {cell.location}. Observing for life signals.")
                    self.send_and_end_turn(OBSERVE(cell.location))
                    return None  # Wait for the observation result

        self._agent.log("No survivors found in the world.")
        return None
