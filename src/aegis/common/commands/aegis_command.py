from abc import ABC

from aegis.common.commands.command import Command


class AegisCommand(Command, ABC):
    """The base class that represents all commands coming from AEGIS."""

    pass
