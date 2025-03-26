from dataclasses import dataclass

from aegis.parsers.helper.cell_info_settings import CellInfoSettings
from aegis.parsers.helper.cell_type_info import CellTypeInfo
from aegis.world.spawn_manager import SpawnZone


@dataclass
class AegisWorldFile:
    width: int
    height: int
    initial_agent_energy: int
    random_seed: int
    high_survivor_level: int
    mid_survivor_level: int
    low_survivor_level: int
    cell_stack_info: list[CellInfoSettings]
    cell_settings: list[CellTypeInfo]
    agent_spawn_locations: list[SpawnZone]
