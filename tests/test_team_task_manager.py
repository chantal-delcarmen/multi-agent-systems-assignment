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