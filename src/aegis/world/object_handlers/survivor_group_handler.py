from typing import override

from aegis.common.world.objects import SurvivorGroup, WorldObject
from aegis.parsers.helper.world_file_type import Arguments
from aegis.world.object_handlers.object_handler import ObjectHandler


class SurvivorGroupHandler(ObjectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.svg_map: dict[int, SurvivorGroup] = {}
        self.alive = 0
        self.dead = 0

    @override
    def get_keys(self) -> list[str]:
        return ["SVG", "SurvivorGroup"]

    @override
    def create_world_object(self, params: dict[Arguments, int]) -> WorldObject | None:
        if len(params) < 2:
            print(
                "WARRNING: SurvivorHandler: incorrect Parameter setting: missing energy_level and/or number_of_survivors"
            )
            return None
        energy_level = params["energy_level"]
        number_of_survivors = params["number_of_survivors"]

        survivor_group = SurvivorGroup(
            self.world_object_count, energy_level, number_of_survivors
        )
        self.svg_map[self.world_object_count] = survivor_group
        self.world_object_count += 1
        if survivor_group.get_energy_level() > 0:
            self.alive += number_of_survivors
        else:
            self.dead += number_of_survivors
        return survivor_group

    @override
    def reset(self) -> None:
        self.svg_map.clear()
        self.alive = 0
        self.dead = 0
