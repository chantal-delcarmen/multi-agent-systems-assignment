import unittest
from unittest.mock import MagicMock

# Import the GoalPlanner class
from src.agents.example_agent_a3.agent_helpers.goal_planner import GoalPlanner


class TestGoalPlanner(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment with a mock agent and world.
        """
        # Mock agent with a location and logging
        self.mock_agent = MagicMock()
        self.mock_agent.location = MagicMock(x=0, y=0)
        self.mock_agent.log = MagicMock()

        # Mock world with cells
        self.mock_world = MagicMock()
        self.mock_world.cells = [
            MagicMock(location=MagicMock(x=1, y=1), has_survivor=MagicMock(return_value=True)),
            MagicMock(location=MagicMock(x=2, y=2), has_survivor=MagicMock(return_value=True)),
            MagicMock(location=MagicMock(x=3, y=3), has_survivor=MagicMock(return_value=False)),
        ]

        # Initialize GoalPlanner
        self.goal_planner = GoalPlanner(self.mock_agent)

    def test_find_survivor_goals(self):
        """
        Test that find_survivor_goals correctly identifies and sorts survivor goals.
        """
        self.goal_planner.find_survivor_goals(self.mock_world)

        # Verify that only cells with survivors are added
        self.assertEqual(len(self.goal_planner._survivor_goals), 2)
        self.assertEqual(self.goal_planner._survivor_goals[0].location.x, 1)
        self.assertEqual(self.goal_planner._survivor_goals[0].location.y, 1)

        # Verify logging
        self.mock_agent.log.assert_any_call("Found 2 survivor goals.")
        self.mock_agent.log.assert_any_call("Added 2 survivor goals.")

    def test_get_next_goal(self):
        """
        Test that get_next_goal returns goals in the correct order.
        """
        self.goal_planner.find_survivor_goals(self.mock_world)

        # Get the first goal
        goal = self.goal_planner.get_next_goal()
        self.assertIsNotNone(goal)
        self.assertEqual(goal.location.x, 1)
        self.assertEqual(goal.location.y, 1)

        # Get the second goal
        goal = self.goal_planner.get_next_goal()
        self.assertIsNotNone(goal)
        self.assertEqual(goal.location.x, 2)
        self.assertEqual(goal.location.y, 2)

        # No more goals should be available
        goal = self.goal_planner.get_next_goal()
        self.assertIsNone(goal)

    def test_mark_goal_unreachable(self):
        """
        Test that mark_goal_unreachable removes the goal from the list and adds it to the unreachable set.
        """
        self.goal_planner.find_survivor_goals(self.mock_world)
        unreachable_goal = self.goal_planner._survivor_goals[0]

        self.goal_planner.mark_goal_unreachable(unreachable_goal)

        # Verify the goal is removed from the survivor goals
        self.assertNotIn(unreachable_goal, self.goal_planner._survivor_goals)

        # Verify the goal is added to the unreachable goals
        self.assertIn(unreachable_goal, self.goal_planner._unreachable_goals)

        # Verify logging
        self.mock_agent.log.assert_any_call(f"Marking goal at {unreachable_goal.location} as unreachable.")

    def test_remove_completed_goal(self):
        """
        Test that remove_completed_goal removes the goal and adjusts the index correctly.
        """
        self.goal_planner.find_survivor_goals(self.mock_world)
        completed_goal = self.goal_planner._survivor_goals[0]

        self.goal_planner.remove_completed_goal(completed_goal)

        # Verify the goal is removed
        self.assertNotIn(completed_goal, self.goal_planner._survivor_goals)

        # Verify logging
        self.mock_agent.log.assert_any_call(f"Removing completed goal at {completed_goal.location}.")

    def test_detect_and_replan_goals(self):
        """
        Test that detect_and_replan_goals triggers replanning when a significant change is detected.
        """
        self.goal_planner.detect_and_replan_goals(self.mock_world, significant_change_detected=True)

        # Verify that replan_goals was called
        self.assertEqual(len(self.goal_planner._survivor_goals), 2)
        self.mock_agent.log.assert_any_call("Significant change detected. Replanning goals.")

    def test_assign_goal_to_agent(self):
        """
        Test that assign_goal_to_agent assigns a goal to another agent and removes it from the list.
        """
        self.goal_planner.find_survivor_goals(self.mock_world)
        goal_to_assign = self.goal_planner._survivor_goals[0]

        # Assign the goal to an agent
        self.goal_planner.assign_goal_to_agent("agent_1", goal_to_assign)

        # Verify the goal is removed from the survivor goals
        self.assertNotIn(goal_to_assign, self.goal_planner._survivor_goals)

        # Verify logging
        self.mock_agent.log.assert_any_call(f"Assigned goal at {goal_to_assign.location} to agent agent_1.")

        # Verify message was sent
        self.mock_agent.comms.send_message.assert_called_with("agent_1", f"GOAL {goal_to_assign.location}")


if __name__ == "__main__":
    unittest.main()