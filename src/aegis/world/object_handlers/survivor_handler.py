from typing import override

from aegis.common.world.objects import Survivor, WorldObject
from aegis.parsers.helper.world_file_type import Arguments
from aegis.world.object_handlers.object_handler import ObjectHandler


class SurvivorHandler(ObjectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.sv_map: dict[int, Survivor] = {}
        self.alive = 0
        self.dead = 0

    @override
    def get_keys(self) -> list[str]:
        return ["SV", "Survivor"]

    @override
    def create_world_object(self, params: dict[Arguments, int]) -> WorldObject | None:
        if len(params) < 4:
            print(
                "WARRNING: SurvivorHandler: incorrect Parameter setting: missing energy_level, damage_factor, body_mass and/or mental_state"
            )
            return None

        energy_level = params["energy_level"]
        damage_factor = params["damage_factor"]
        body_mass = params["body_mass"]
        mental_state = params["mental_state"]

        survivor = Survivor(
            self.world_object_count,
            energy_level,
            damage_factor,
            body_mass,
            mental_state,
        )

        self.sv_map[self.world_object_count] = survivor
        self.world_object_count += 1
        if survivor.get_energy_level() > 0:
            self.alive += 1
        else:
            self.dead += 1
        return survivor

    @override
    def reset(self) -> None:
        self.sv_map.clear()
        self.alive = 0
        self.dead = 0
