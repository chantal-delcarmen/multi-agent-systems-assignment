"""
LeaderCoordinator: Used by the leader to assign tasks, track survivor
assignments, and coordinate completion.
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
        pass  # to be implemented

    def mark_survivor_saved(self, location):
        pass  # to be implemented

    def all_survivors_saved(self):
        pass  # to be implemented
