from dataclasses import dataclass
from typing import override
from aegis.common import InternalLocation
from aegis.parsers.helper.world_file_type import StackContent


@dataclass
class CellInfoSettings:
    move_cost: int
    contents: list[StackContent]
    location: InternalLocation = InternalLocation(-1, -1)

    @override
    def __str__(self) -> str:
        return f"Cell ({self.location}, Move_Cost {self.move_cost}) {self.contents}"
