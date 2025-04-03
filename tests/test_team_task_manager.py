import pytest
from unittest.mock import MagicMock
from src.agents.example_agent_a3.agent_helpers.team_task_manager import TeamTaskManager

@pytest.fixture
def setup_manager():
    # Mock the LeaderCoordinator and CommunicationManager
    mock_leader_coordinator = MagicMock()
    mock_comms = MagicMock()

    # Initialize the TeamTaskManager with mocks
    manager = TeamTaskManager(leader_coordinator=mock_leader_coordinator, comms=mock_comms)
    return manager, mock_leader_coordinator, mock_comms

def test_add_task(setup_manager):
    manager, mock_leader_coordinator, mock_comms = setup_manager
    location = (3, 4)
    required_agents = 2

    manager.add_task(location, required_agents)

    assert location in manager.team_dig_tasks
    task = manager.team_dig_tasks[location]
    assert task["required_agents"] == required_agents
    assert task["completed"] is False
    assert len(task["assigned_agents"]) == 0
    assert task["dig_count"] == 0

    # Verify that agents were notified
    mock_comms.send_message_to_all.assert_called_once_with(f"TASK {location[0]} {location[1]} {required_agents}")
    mock_leader_coordinator.agent.log.assert_called_once_with(
        f"Notified agents about task at {location} requiring {required_agents} agents."
    )

def test_call_agents_to_meet(setup_manager):
    manager, mock_leader_coordinator, mock_comms = setup_manager
    location = (5, 6)

    manager.call_agents_to_meet(location)

    # Verify that agents were notified to meet
    mock_comms.send_message_to_all.assert_called_once_with(f"MEET {location[0]} {location[1]}")
    mock_leader_coordinator.agent.log.assert_called_once_with(f"Called agents to meet at {location}.")

def test_mark_task_completed(setup_manager):
    manager, mock_leader_coordinator, mock_comms = setup_manager
    location = (7, 8)
    required_agents = 2

    manager.add_task(location, required_agents)
    manager.mark_task_completed(location)

    # Verify that the task is marked as completed
    assert manager.team_dig_tasks[location]["completed"] is True

    # Verify that the LeaderCoordinator and agents were notified
    mock_leader_coordinator.notify_task_completed.assert_called_once_with(location)

    # Verify that send_message_to_all was called twice: once for TASK and once for TASK_COMPLETED
    mock_comms.send_message_to_all.assert_any_call(f"TASK {location[0]} {location[1]} {required_agents}")
    mock_comms.send_message_to_all.assert_any_call(f"TASK_COMPLETED {location[0]} {location[1]}")

    # Verify the total number of calls to send_message_to_all
    assert mock_comms.send_message_to_all.call_count == 2

def test_coordinate_team_dig(setup_manager):
    manager, mock_leader_coordinator, mock_comms = setup_manager
    location = (9, 10)
    required_agents = 2

    manager.add_task(location, required_agents)

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

    # Verify that agents were called to meet
    mock_comms.send_message_to_all.assert_any_call(f"MEET {location[0]} {location[1]}")

    # Verify that the task was marked as completed
    mock_comms.send_message_to_all.assert_any_call(f"TASK_COMPLETED {location[0]} {location[1]}")
    mock_leader_coordinator.notify_task_completed.assert_called_once_with(location)

def test_handle_task_message(setup_manager):
    manager, mock_leader_coordinator, mock_comms = setup_manager
    location = (11, 12)
    required_agents = 2

    manager.add_task(location, required_agents)

    # Handle a TASK_COMPLETED message
    message = {"type": "TASK_COMPLETED", "location": location}
    manager.handle_task_message(message)

    # Verify that the task was marked as completed
    assert manager.team_dig_tasks[location]["completed"] is True
    mock_leader_coordinator.notify_task_completed.assert_called_once_with(location)

    # Handle a MEET message
    message = {"type": "MEET", "location": location}
    manager.handle_task_message(message)
    mock_leader_coordinator.agent.log.assert_called_with(f"Received MEET message for location {location}.")

def test_is_enough_agents(setup_manager):
    manager, _, _ = setup_manager
    location = (13, 14)
    required_agents = 2

    manager.add_task(location, required_agents)

    # Initially, not enough agents
    assert manager.is_enough_agents(location) is False

    # Add agents
    manager.team_dig_tasks[location]["assigned_agents"].add("Agent1")
    assert manager.is_enough_agents(location) is False

    manager.team_dig_tasks[location]["assigned_agents"].add("Agent2")
    assert manager.is_enough_agents(location) is True

def test_notify_agents_about_task(setup_manager):
    manager, mock_leader_coordinator, mock_comms = setup_manager
    location = (3, 4)
    required_agents = 2

    # Call the method
    manager.notify_agents_about_task(location, required_agents)

    # Verify that the correct message was sent to all agents
    mock_comms.send_message_to_all.assert_called_once_with(f"TASK {location[0]} {location[1]} {required_agents}")

    # Verify that the correct log message was created
    mock_leader_coordinator.agent.log.assert_called_once_with(
        f"Notified agents about task at {location} requiring {required_agents} agents."
    )