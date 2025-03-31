"""
Class LeaderCoordinator: Used by the leader to assign tasks, track survivor
assignments, and coordinate completion.

Authors: 
Chantal del Carmen, Zainab Majid, Mohammad Akif Hasan, Vincent Iyegbuye

Course: CPSC 383 - Winter 2025 | T05
Assignment 3 - Multi-Agent Systems
Mar 30, 2025

"""
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



class LeaderCoordinator:
    def __init__(self, agent:AgentController):
        self.agent = agent
        self.is_leader = agent.get_agent_id().id == 1
        # assignments: dict[AgentID -> (survivor_x, survivor_y)]
        self.assignments = {}
        # survivors_remaining: set of (survivor_x, survivor_y) that are unsaved
        self.survivors_remaining = set()

    def should_lead(self) -> bool:
        """
        Returns True if this agent is the leader.
        By convention, we pick agent 0 as the leader.
        """
        return self.is_leader

    def assign_agents_to_goals(self, agents, survivor_cells):
        """
        For each survivor cell, choose which agent should go there.
        We do a naive assignment, e.g., the first free agent gets the survivor.

        :param agents: a list of agent controllers, e.g., [AgentController(agent_id=0), ...]
        :param survivor_cells: a list of cell objects or (x, y) coordinates for survivors
        """
        # 1. update self.survivors_remaining with all the new survivors
        for cell in survivor_cells:
            self.survivors_remaining.add(cell.location)

        # 2. for each survivor location, if it’s not already assigned, assign an agent
        for survivor_loc in self.survivors_remaining:
            already_assigned = any(
                assigned_loc == survivor_loc
                for assigned_loc in self.assignments.values()
            )
            if already_assigned:
                # skip if it’s already assigned
                continue

            # If not assigned, pick an agent (naive approach: pick first with no current assignment)
            for ag in agents:
                if ag.get_agent_id().id not in self.assignments:
                    # assign agent to this survivor
                    self.assignments[ag.get_agent_id().id] = survivor_loc
                    break
                else:
                    # If already assigned, check if agent reached or completed old assignment
                    pass
        # The dictionary self.assignments now has a mapping of agentID -> (x,y) for survivors.

    def mark_survivor_saved(self, location):
        """
        Remove the saved survivor from survivors_remaining and remove from assignments
        for any agent that had that location assigned.
        """
        if isinstance(location, tuple):
            loc_tuple = location
        else:
            loc_tuple = (location.x, location.y)

        # Remove from the survivors_remaining
        if loc_tuple in self.survivors_remaining:
            self.survivors_remaining.remove(loc_tuple)

        # Remove from any agent's assignment
        for agent_id, assigned_loc in list(self.assignments.items()):
            if assigned_loc == loc_tuple:
                del self.assignments[agent_id]

    def all_survivors_saved(self) -> bool:
        """
        Returns True if no survivors remain to be saved.
        """
        return len(self.survivors_remaining) == 0
