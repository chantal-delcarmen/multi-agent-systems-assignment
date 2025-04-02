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
        self.is_leader = agent.get_agent_id().id == 1
        self.assignments = {}
        self.survivors_remaining = set()

    def should_lead(self):
        return self.is_leader

    def assign_agents_to_goals(self, agents, survivor_cells):
        """
        Assign idle agents to survivor goals if possible.
        :param agents: Dict or list with agent states, e.g. { agent_id: { 'loc':..., 'energy':..., 'task':... } }
        :param survivor_cells: A set or list of survivor locations not yet assigned or rescued.
        """
        # 1. Filter out survivors that are already assigned or saved
        #    If you are storing them in self.survivors_remaining, you can skip param "survivor_cells"
        unassigned_survivors = [sv for sv in survivor_cells if sv not in self.assignments.values()]

        # 2. Find idle agents (i.e. agent['task'] is None or 'IDLE')
        idle_agents = [aid for aid, ainfo in agents.items() if ainfo.get('task') is None]

        
        for svloc in unassigned_survivors:
            if not idle_agents:
                break
            # pick next idle agent (pop from front)
            agent_id = idle_agents.pop(0)

            # record that agent is assigned to this survivor
            self.assignments[agent_id] = svloc


        # Optional: log or debug info
        self.agent.log(f"[LeaderCoordinator] Assigned {len(survivor_cells)} survivors among agents.")

    def mark_survivor_saved(self, location):
        pass  # to be implemented

    def all_survivors_saved(self):
        """
        Returns True if we have no more survivors_remaining, 
        otherwise False.
        """
        return len(self.survivors_remaining) == 0

