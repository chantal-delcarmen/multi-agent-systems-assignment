class Option:
    def __init__(self) -> None:
        self.name = ""
        self.value_type = 0
        self.value: int | str | bool | float | None = None
        self.is_required = False
        self.is_set = False
