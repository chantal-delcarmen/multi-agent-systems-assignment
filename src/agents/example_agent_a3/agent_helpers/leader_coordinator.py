"""
Class LeaderCoordinator: Used by the leader to assign tasks, track survivor
assignments, and coordinate completion.

Authors: 
Chantal del Carmen, Zainab Majid, Mohammad Akif Hasan, Vincent Iyegbuye

Course: CPSC 383 - Winter 2025 | T05
Assignment 3 - Multi-Agent Systems
Mar 30, 2025

"""

class LeaderCoordinator:
    def __init__(self, agent):
        self.agent = agent
        self.is_leader = agent.get_agent_id().id == 0
        self.assignments = {}
        self.survivors_remaining = set()

    def should_lead(self):
        return self.is_leader

    def assign_agents_to_goals(self, agents, survivor_cells):
        parsed_messages = []
        for agent in agents:
            if agent.get_agent_id().id == 0: # Skip the leader
                continue
            if not survivor_cells:
                break # No more survivors to assign
            survivor = survivor_cells.pop()
            self.assignments[agent.get_agent_id().id] = survivor
            self.survivors_remaining.add(survivor)
            self.agent.send_message(agent.get_agent_id(), self.generate_assignment_message(agent.get_agent_id().id, survivor))  # need to replace these methods with something esle. its a placeholder for now
        self.agent.log(f"Assignments made: {self.assignments}")
        parsed_messages.append({
            "type": "ASSIGN",
            "agentID": agent.get_agent_id().id,
            "location": survivor
        })
        return parsed_messages

    def mark_survivor_saved(self, location):
        pass  # to be implemented

    def all_survivors_saved(self):
        pass  # to be implemented
