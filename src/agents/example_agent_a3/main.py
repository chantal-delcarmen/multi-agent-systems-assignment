# import sys

# from a3.agent import BaseAgent
# from agents.example_agent_a3.example_agent import ExampleAgent


# def main() -> None:
#     if len(sys.argv) == 1:
#         BaseAgent.get_agent().start_test(ExampleAgent())
#     elif len(sys.argv) == 2:
#         BaseAgent.get_agent().start_with_group_name(sys.argv[1], ExampleAgent())
#     else:
#         print("Agent: Usage: python3 agents/example_agent/main.py <groupname>")


# if __name__ == "__main__":
#     main()

""" 
The following code is a test script for the TeamTaskManager class.
Commented out code above is original agent code that is not needed for this test.
"""
from agent_helpers.team_task_manager import TeamTaskManager

def main():
    manager = TeamTaskManager()
    location = "A1"
    current_turn = 5
    estimated_travel_time = 3

    # Add a task
    manager.add_task(location, current_turn, estimated_travel_time)
    print(f"Task added: {manager.team_dig_tasks}")

    # Check if TEAM_DIG is needed
    print(f"Is TEAM_DIG needed at {location}? {manager.is_team_dig_needed(location)}")

    # Coordinate agents
    print("Coordinating agents for TEAM_DIG at location A1:")

    # Assign Agent 1
    agent_1_result = manager.coordinate_team_dig('agent_1', location)
    print(f"Agent 1 assigned to task: {'Success' if agent_1_result else 'Waiting for more agents'}")

    # Assign Agent 2
    agent_2_result = manager.coordinate_team_dig('agent_2', location)
    print(f"Agent 2 assigned to task: {'Success' if agent_2_result else 'Waiting for more agents'}")

    # Display the current task status
    if manager.current_task:
        print(f"TEAM_DIG is ready to proceed at location: {manager.current_task}")
    else:
        print("TEAM_DIG is not ready yet. More agents may be needed.")

if __name__ == "__main__":
    main()