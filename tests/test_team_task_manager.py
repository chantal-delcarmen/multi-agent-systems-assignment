import pytest
from src.agents.example_agent_a3.agent_helpers.team_task_manager import TeamTaskManager

def test_add_task():
    manager = TeamTaskManager()
    location = "A1"
    current_turn = 5
    estimated_travel_time = 3

    manager.add_task(location, current_turn, estimated_travel_time)

    assert location in manager.team_dig_tasks
    task = manager.team_dig_tasks[location]
    assert task["required_agents"] == 2
    assert task["completed"] is False

    # Check if the task is planned for the correct turn
    print(f"Planned turn: {task['planned_turn']}, Expected: {current_turn + estimated_travel_time + 2}")
    assert task["planned_turn"] == current_turn + estimated_travel_time + 2

def test_is_team_dig_needed():
    manager = TeamTaskManager()
    location = "B2"
    current_turn = 5
    estimated_travel_time = 3

    manager.add_task(location, current_turn, estimated_travel_time)

    assert manager.is_team_dig_needed(location) is True

    # Mark the task as completed and check again
    manager.team_dig_tasks[location]["completed"] = True
    assert manager.is_team_dig_needed(location) is False

def test_coordinate_team_dig():
    manager = TeamTaskManager()
    location = "C3"
    current_turn = 5
    estimated_travel_time = 3

    manager.add_task(location, current_turn, estimated_travel_time)

    # Test if team dig is needed
    assert manager.is_team_dig_needed(location) is True

    # Assign the first agent
    result_1 = manager.coordinate_team_dig("Agent1", location)
    task = manager.team_dig_tasks[location]
    assert "Agent1" in task["assigned_agents"]
    assert task["dig_count"] == 1
    assert result_1 is False  # Not enough agents yet

    # Assign the second agent
    result_2 = manager.coordinate_team_dig("Agent2", location)
    task = manager.team_dig_tasks[location]
    assert "Agent2" in task["assigned_agents"]
    assert task["dig_count"] == 2
    assert result_2 is True  # Now team dig can proceed

def test_assign_to_completed_task():
    manager = TeamTaskManager()
    location = "D4"
    current_turn = 5
    estimated_travel_time = 3

    manager.add_task(location, current_turn, estimated_travel_time)

    # Mark the task as completed
    manager.team_dig_tasks[location]["completed"] = True

    # Try to assign an agent
    result = manager.coordinate_team_dig("Agent1", location)
    assert result is False  # Assignment should fail
    task = manager.team_dig_tasks[location]
    assert len(task["assigned_agents"]) == 0  # No agents should be assigned

def test_duplicate_agent_assignment():
    manager = TeamTaskManager()
    location = "E5"
    current_turn = 5
    estimated_travel_time = 3

    manager.add_task(location, current_turn, estimated_travel_time)

    # Assign the same agent twice
    manager.coordinate_team_dig("Agent1", location)
    manager.coordinate_team_dig("Agent1", location)

    task = manager.team_dig_tasks[location]
    assert len(task["assigned_agents"]) == 1  # Only one unique agent
    assert task["dig_count"] == 1  # Dig count should not increase for duplicate assignments

def test_task_does_not_exist():
    manager = TeamTaskManager()
    location = "F6"

    # Try to assign an agent to a non-existent task
    result = manager.coordinate_team_dig("Agent1", location)
    assert result is False  # Task does not exist, so assignment should fail

def test_remove_completed_tasks():
    manager = TeamTaskManager()
    location = "G7"
    current_turn = 5
    estimated_travel_time = 3

    manager.add_task(location, current_turn, estimated_travel_time)
    manager.team_dig_tasks[location]["completed"] = True

    # Remove completed tasks
    manager.remove_completed_task(location)

    # Ensure the task is removed
    assert location not in manager.team_dig_tasks

def test_call_agents_to_meet():
    manager = TeamTaskManager()
    location = "H8"
    current_turn = 5
    estimated_travel_time = 3

    # Add a task and assign agents
    manager.add_task(location, current_turn, estimated_travel_time)
    manager.coordinate_team_dig("Agent1", location)
    manager.coordinate_team_dig("Agent2", location)

    # Call agents to meet at the location
    notifications = manager.call_agents_to_meet(location)

    # Verify the notifications
    assert len(notifications) == 2
    assert "Notify Agent1 to meet at H8 for TEAM_DIG." in notifications
    assert "Notify Agent2 to meet at H8 for TEAM_DIG." in notifications

