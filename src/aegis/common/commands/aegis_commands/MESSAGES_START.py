from typing import override

from aegis.common.commands.aegis_command import AegisCommand


class MESSAGES_START(AegisCommand):
    """
    Represents the start of the message phase in AEGIS.

    Attributes:
        messages (int): The number of messages to forward.
    """

    def __init__(self, messages: int) -> None:
        """
        Initializes a MESSAGES_START instance.

        Args:
            messages: The number of messages to forward.
        """
        self.messages = messages

    @override
    def __str__(self) -> str:
        return f"{self.STR_MESSAGES_START} ( {self.messages} )"
