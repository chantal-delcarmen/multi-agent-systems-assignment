from typing import override


class LifeSignals:
    """
    Represents a collection of life signals, where a survivor's life signal
    represents their energy level, and rubble is represented as 0. The deeper
    the layer, the more distorted the signal becomes.

    Attributes:
        life_signals (list[int]): A list of life signals.
    """

    def __init__(self, life_signals: list[int] | None = None) -> None:
        """
        Initializes a LifeSignals instance.

        Args:
            life_signals: An optional list of life signals.
        """
        self.life_signals: list[int] = life_signals or []

    def size(self) -> int:
        """Returns the number of life signals."""
        return len(self.life_signals)

    def get(self, index: int) -> int:
        """
        Retrieves the life signal at the specified index.

        Args:
            index: The index of the life signal to retrieve.
        """
        return self.life_signals[index]

    @override
    def __str__(self) -> str:
        return f"( {' , '.join(str(signal) for signal in self.life_signals)} )"

    @override
    def __repr__(self) -> str:
        return self.__str__()
