from enum import Enum


class AgentStates(Enum):
    """Enum representing the different states of an agent."""

    IDLE = 1
    """The agent is idle."""

    READ_MAIL = 2
    """The agent is reading incoming messages."""

    GET_CMD_RESULT = 3
    """The agent is receiving the results from the last command sent to AEGIS."""

    THINK = 4
    """The agent is performing computations for a new round."""

    SHUTTING_DOWN = 5
    """The agent is in the process of shutting down."""

    CONNECTING = 6
    """The agent is attempting to establish a connection with AEGIS."""

    CONNECTED = 7
    """The agent has successfully established a connection with AEGIS."""
