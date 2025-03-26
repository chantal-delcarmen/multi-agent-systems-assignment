class AgentSocketException(Exception):
    def __init__(self, message: str = "Error with agent socket operation") -> None:
        super().__init__(message)
