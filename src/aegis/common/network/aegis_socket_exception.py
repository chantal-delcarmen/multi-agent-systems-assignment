class AegisSocketException(Exception):
    """
    Custom exception for errors related to AegisSocket operations.

    Attributes:
        message: A string message that describes the error.
    """

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message)
