import sys

from a3.agent import BaseAgent
from agents.example_agent_a3.example_agent import ExampleAgent


def main() -> None:
    if len(sys.argv) == 1:
        BaseAgent.get_agent().start_test(ExampleAgent())
    elif len(sys.argv) == 2:
        BaseAgent.get_agent().start_with_group_name(sys.argv[1], ExampleAgent())
    else:
        print("Agent: Usage: python3 agents/example_agent/main.py <groupname>")


if __name__ == "__main__":
    main()
