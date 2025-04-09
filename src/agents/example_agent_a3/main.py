import sys
import os

# # Add the `src` directory to the Python path
# current_dir = os.path.dirname(os.path.abspath(__file__))
# src_dir = os.path.abspath(os.path.join(current_dir, "../.."))  # Adjust path to point to `src`
# if src_dir not in sys.path:
#     sys.path.append(src_dir)

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