class AgentCrashedException(Exception):
    def __init__(self, message: str = "Agent has crashed"):
        super().__init__(message)
