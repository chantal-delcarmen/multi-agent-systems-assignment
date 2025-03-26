from enum import Enum


class State(Enum):
    """Represents the state of the simulation."""

    IDLE = 1
    """The simulation is idle."""

    SHUT_DOWN = 2
    """The simulation is shutting down."""

    CONNECT_AGENTS = 3
    """Connecting agents to the simulation."""

    RUN_SIMULATION = 4
    """The simulation is running."""

    NONE = 5
    """No state."""
