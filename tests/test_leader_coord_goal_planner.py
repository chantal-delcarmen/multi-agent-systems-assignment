import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the `src` directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, "../src"))
if src_dir not in sys.path:
    sys.path.append(src_dir)

# Import GoalPlanner and LeaderCoordinator from their respective modules
from src.agents.example_agent_a3.agent_helpers.goal_planner import GoalPlanner
from src.agents.example_agent_a3.agent_helpers.leader_coordinator import LeaderCoordinator


class TestLeaderCoordinatorWithGoalPlanner(unittest.TestCase):
    @patch("src.agents.example_agent_a3.agent_helpers.leader_coordinator.AStarPathfinder")
    def test_leader_coordinator_with_goal_planner(self, MockPathfinder):
        # Mock agent and world
        mock_agent = MagicMock()
        mock_agent.get_agent_id.return_value.id = 1
        mock_agent.location = MagicMock(x=0, y=0)  # Agent's location with numeric x, y

        mock_world = MagicMock()
        mock_world.cells = [
            MagicMock(location=MagicMock(x=1, y=1), has_survivor=MagicMock(return_value=True)),
            MagicMock(location=MagicMock(x=2, y=2), has_survivor=MagicMock(return_value=True)),
        ]

        # Mock pathfinder behavior
        mock_pathfinder_instance = MockPathfinder.return_value

        # Mock find_path to return a valid path
        mock_pathfinder_instance.find_path.side_effect = lambda start, goal: [start, goal]

        # Mock cost_so_far to use tuples as keys
        mock_pathfinder_instance.cost_so_far = {
            (1, 1): 1,  # Cost for goal at (1, 1)
            (2, 2): 2,  # Cost for goal at (2, 2)
        }

        # Mock world.get_cell_at to return cells with numeric locations
        def mock_get_cell_at(location):
            cell = MagicMock()
            cell.location = location
            return cell

        mock_world.get_cell_at.side_effect = mock_get_cell_at

        # Initialize GoalPlanner and LeaderCoordinator
        goal_planner = GoalPlanner(mock_agent)
        leader_coordinator = LeaderCoordinator(mock_agent, goal_planner)

        # Find survivor goals
        goal_planner.find_survivor_goals(mock_world)

        # Assign agents to goals
        mock_agents = [
            MagicMock(get_agent_id=MagicMock(return_value=MagicMock(id=1)), get_location=MagicMock(return_value=(0, 0))),
            MagicMock(get_agent_id=MagicMock(return_value=MagicMock(id=2)), get_location=MagicMock(return_value=(3, 3))),
        ]
        leader_coordinator.assign_agents_to_goals(mock_agents, mock_world)

        # Verify assignments
        self.assertEqual(len(leader_coordinator.assignments), 2)
        self.assertEqual(len(goal_planner._survivor_goals), 0)  # All goals should be assigned

        # Verify that the correct agents were assigned to the correct goals
        assigned_goals = [
            (assignment.location.x, assignment.location.y) for assignment in leader_coordinator.assignments.values()
        ]
        expected_goals = [(1, 1), (2, 2)]
        self.assertCountEqual(assigned_goals, expected_goals)


if __name__ == "__main__":
    unittest.main()